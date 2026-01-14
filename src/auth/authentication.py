import os
from fastapi import Header, HTTPException
import requests
from jose import jwt
from jose.exceptions import JWTError, ExpiredSignatureError
from logger import logger
def getToken(authorization: str):
    token: str =  authorization.split()[1]
    logger.debug(f"first 20 character of token are {token[:20]}")
    return token

def getEnv(envVar:str):
    value = os.getenv(envVar)
    if not value:
        raise ValueError(f"{envVar} missing and no default value is specified")
    logger.debug(f"{envVar} has value {value}")
    return value
    
async def authentication(authorization: str | None = Header(default=None, alias="Authorization")):
    if not authorization:
        raise HTTPException(401, "No token")
    return verify_cognito_access_token(token=getToken(authorization), region=getEnv("REGION"), 
                               user_pool_id=getEnv("USER_POOL_ID"), app_client_id=getEnv("APP_CLIENT_ID"))

def verify_cognito_access_token(
    *,
    token: str,
    region: str,
    user_pool_id: str,
    app_client_id: str,
) -> dict:
    """
    Verifies an Amazon Cognito ACCESS token only.
    ID tokens are rejected.
    """

    issuer = f"https://cognito-idp.{region}.amazonaws.com/{user_pool_id}"
    jwks_url = f"{issuer}/.well-known/jwks.json"

    # 1. Read JWT header (unverified) → kid only
    unverified_header = jwt.get_unverified_header(token)
    kid = unverified_header.get("kid")

    if not kid:
        raise HTTPException(401, "JWT header missing 'kid'")

    # 2. Fetch JWKS (NO CACHE, NO TIMEOUT)
    resp = requests.get(jwks_url)
    resp.raise_for_status()
    jwks = resp.json()

# 3. Find matching public key
    public_key = next(
        (key for key in jwks.get("keys", []) if key.get("kid") == kid),
        None,
    )

    if public_key is None:
        raise HTTPException(401, f"Public key not found for kid={kid}")

    # 4. Verify signature + standard claims (STRICT time)
    try:
        claims = jwt.decode(
            token,
            public_key,
            algorithms=["RS256"],
            issuer=issuer,
            options={
                "verify_signature": True,
                "verify_iss": True,
                "verify_exp": True,
                "verify_nbf": True,
                "verify_aud": False,  # Cognito access tokens don't use aud
                "leeway": 0,
            },
        )
    except ExpiredSignatureError:
        logger.error("token expired")
        raise HTTPException(401, "token expired")
    except JWTError as e:
        logger.error(f"JWTError {str(e)}")
        raise HTTPException(401, "Invalid token")

    # 5. ACCESS TOKEN ONLY checks
    if claims.get("token_use") != "access":
        raise ValueError("Only access tokens are allowed")

    # Access token must match app client
    client_id = claims.get("client_id")
    if client_id != app_client_id:
        raise ValueError(
            f"Invalid client_id={client_id}, expected {app_client_id}"
        )

    return claims
