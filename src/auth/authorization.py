from fastapi import Depends, HTTPException
from auth.authentication import authentication
from logger import logger
async def authorization (claims=Depends(authentication)) -> tuple[str, str]:
  
   username = claims.get("username","")
   groups = claims.get("cognito:groups", [])
   logger.debug(f"from authorization dependent: username is {username}, groups is {groups}")
   if "admin" not in groups:
       raise HTTPException(403, "Access Denied")
   return username, ",".join(groups)


