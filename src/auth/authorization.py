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


