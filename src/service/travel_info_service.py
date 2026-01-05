from fastapi import HTTPException
from api_services.exchange_rate_api import getExchangeRate
from api_services.weather_api import getWeather
from models.travel_request import TravelRequest
from models.travel_response import TravelResponse
from open_ai.chat_request import chatRequest
from open_ai.system_rules import RULES
from logger import logger
from utils.functions import extractJSON


def openAiAccess(countryFrom: str, countryTo: str | None = None, cityTo: str | None = None):
    messages: list[dict] = [
        {"role": "system",
            "content": RULES["countryTo" if countryTo else "cityTo"]},
        {"role": "user", "content": f"from {countryFrom} to {countryTo if countryTo else cityTo}"}
    ]
    resp = chatRequest(messages)
    logger.debug("response from open-ai is %s", resp)
    respDict = extractJSON(resp, ["country_from", "country_to"])
    if not respDict:
        raise HTTPException(
            status_code=500,
            detail=f"Wrong response from OpenAI {resp}"
        )
    logger.debug("response converted to dict is %s", respDict)
    return respDict


def getResponse(travelRequest: TravelRequest, respDict: dict) -> TravelResponse:
    cityTo = respDict.get("city_to")
    return TravelResponse(countryFrom=respDict["country_from"],
                          countryTo=respDict["country_to"],
                          cityTo=cityTo,
                          capitalTo=respDict["capital_to"] if travelRequest.iscapital else None,
                          currencyCodeFrom=respDict["currency_code_from"] if travelRequest.iscurrency else None,
                          currencyCodeTo=respDict["currency_code_to"] if travelRequest.iscurrency else None,
                          currencyNameFrom=respDict["currency_name_from"] if travelRequest.iscurrency else None,
                          currencyNameTo=respDict["currency_name_to"] if travelRequest.iscurrency else None,
                          weatherTo=getWeather(
                              cityTo if cityTo else respDict["capital_to"])if travelRequest.isweather else None,
                          exchangeRate=getExchangeRate(respDict["currency_code_from"],
                                                       respDict["currency_code_to"]) if travelRequest.iscurrency else None)


def travel_info(travelRequest: TravelRequest):
    respDict = openAiAccess(travelRequest.countryFrom,
                            travelRequest.countryTo, travelRequest.cityTo)
    return getResponse(travelRequest, respDict)
