from fastapi import HTTPException, Header, logger
from jose import jwt 


async def authorization (authorization = Header(..., alias="Authorization")) -> tuple[str, str]:
   token = authorization.split()[1]
   claims = jwt.get_unverified_claims(token)
   username = claims.get("username","")
   groups = claims.get("cognito:groups", [])
   logger.debug(f"from authorization dependent: username is {username}, groups is {groups}")
   if "admin" not in groups:
       raise HTTPException(403, "Access Denied")
   return username, ",".join(groups)


# import requests
# from jose import jwt
# from jose.exceptions import JWTError, ExpiredSignatureError


# def verify_cognito_access_token(
#     *,
#     token: str,
#     region: str,
#     user_pool_id: str,
#     app_client_id: str,
# ) -> dict:
#     """
#     Verifies an Amazon Cognito ACCESS token only.
#     ID tokens are rejected.
#     """

#     issuer = f"https://cognito-idp.{region}.amazonaws.com/{user_pool_id}"
#     jwks_url = f"{issuer}/.well-known/jwks.json"

#     # 1. Read JWT header (unverified) → kid only
#     unverified_header = jwt.get_unverified_header(token)
#     kid = unverified_header.get("kid")

#     if not kid:
#         raise ValueError("JWT header missing 'kid'")

#     # 2. Fetch JWKS (NO CACHE, NO TIMEOUT)
#     resp = requests.get(jwks_url)
#     resp.raise_for_status()
#     jwks = resp.json()

#     # 3. Find matching public key
#     public_key = next(
#     (key for key in jwks.get("keys", []) if key.get("kid") == kid),
#     None,
# )

# if public_key is None:
#     raise ValueError(f"Public key not found for kid={kid}")


#     if public_key is None:
#         raise ValueError(f"Public key not found for kid={kid}")

#     # 4. Verify signature + standard claims (STRICT time)
#     try:
#         claims = jwt.decode(
#             token,
#             public_key,
#             algorithms=["RS256"],
#             issuer=issuer,
#             options={
#                 "verify_signature": True,
#                 "verify_iss": True,
#                 "verify_exp": True,
#                 "verify_nbf": True,
#                 "verify_aud": False,  # Cognito access tokens don't use aud
#                 "leeway": 0,
#             },
#         )
#     except ExpiredSignatureError:
#         raise
#     except JWTError:
#         raise

#     # 5. ACCESS TOKEN ONLY checks
#     if claims.get("token_use") != "access":
#         raise ValueError("Only access tokens are allowed")

#     # Access token must match app client
#     client_id = claims.get("client_id")
#     if client_id != app_client_id:
#         raise ValueError(
#             f"Invalid client_id={client_id}, expected {app_client_id}"
#         )

#     return claims
