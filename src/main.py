from fastapi import Depends, FastAPI
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError

from auth.authorization import authorization
from auth.authentication import authentication
from exceptions.handlers import registerExceptionHandlers
from models.travel_request import TravelRequest
from models.travel_response import TravelResponse
from service.travel_info_service import travel_info
from logger import logger
app = FastAPI()
registerExceptionHandlers(app)

@app.get("/travel/info/health")
async def health():
    return {"status":"running"}
@app.get("/travel/info", response_model=TravelResponse)
async def travelInfoGetHandler(countryFrom: str, countryTo: str | None = None,
                               cityTo: str | None = None, user_info = Depends(authorization)):
    try:
        travelRequest = TravelRequest(countryFrom=countryFrom, countryTo=countryTo, cityTo=cityTo,
                                      iscapital=True, iscurrency=True, isweather=True)
        
    except ValidationError as e:
        raise RequestValidationError(e.errors())
    logger.debug("API GET endpoint travel/info: countryFrom: %s, %s", countryFrom,
                 f"countryTo: {countryTo}" if countryTo else f"cityTo: {cityTo}")
    logger.debug(f"API GET endpoint travel/info: username={user_info[0]}, groups={user_info[1]}")
    return travel_info(travelRequest)


@app.post("/travel/info", response_model=TravelResponse)
async def travelInfoPostHandler(travelRequest: TravelRequest, claims=Depends(authentication)):
    logger.debug("API POST endpoint travel/info: request: %s", travelRequest)
    logger.debug(f"token in Authorization header has been verified with claims {claims}")
    return travel_info(travelRequest)
