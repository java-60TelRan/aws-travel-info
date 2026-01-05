from fastapi import Depends, FastAPI
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError

from exceptions.handlers import registerExceptionHandlers
from middleware.validation import validation_middleware
from models.travel_request import TravelRequest
from models.travel_response import TravelResponse
from service.travel_info_service import travel_info
from logger import logger
app = FastAPI()
app.middleware("http")(validation_middleware)
registerExceptionHandlers(app)


@app.get("/travel/info", response_model=TravelResponse)
async def travelInfoGetHandler(countryFrom: str, countryTo: str | None = None,
                               cityTo: str | None = None):
    try:
        travelRequest = TravelRequest(countryFrom=countryFrom, countryTo=countryTo, cityTo=cityTo,
                                      iscapital=True, iscurrency=True, isweather=True)
    except ValidationError as e:
        raise RequestValidationError(e.errors())
    logger.debug("API GET endpoint travel/info: countryFrom: %s, %s", countryFrom,
                 f"countryTo: {countryTo}" if countryTo else f"cityTo: {cityTo}")
    return travel_info(travelRequest)


@app.post("/travel/info", response_model=TravelResponse)
async def travelInfoPostHandler(travelRequest: TravelRequest):
    logger.debug("API POST endpoint travel/info: request: %s", travelRequest)
    return travel_info(travelRequest)
