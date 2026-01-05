import json
from fastapi import Request
from fastapi.responses import JSONResponse
from logger import logger
from middleware.common import extractResponseBody, rebuildResponse


def isMatch(travelRequest: dict, travelResponse: dict) -> bool:
    isCurrencyRequest = travelRequest["iscurrency"]
    isCapitalRequest = travelRequest["iscapital"]
    isWeatherRequest = travelRequest["isweather"]
    hasCurrencyResponse = travelResponse.get("exchangeRate") is not None
    hasCapitalResponse = travelResponse.get("capitalTo") is not None
    hasWeatherResponse = travelResponse.get("weatherTo") is not None
    return isCapitalRequest == hasCapitalResponse and isCurrencyRequest == hasCurrencyResponse and isWeatherRequest == hasWeatherResponse


async def validation_middleware(request: Request, call_next):
    if "info" not in request.url.path:
        return await call_next(request)
    travelRequest: dict = {
        "isweather": True,
        "iscurrency": True,
        "iscapital": True
    }
    if request.method == "POST":
        requestBody = await request.body() if request.method == "POST" else None
        travelRequest = json.loads(requestBody)

        async def receive():
            return {"type": "http.request", "body": requestBody}

        request = Request(request.scope, receive)
        logger.debug(
            "validation middleware received dictionary %s", travelRequest)
    resp = await call_next(request)
    response_raw_body, response_body = await extractResponseBody(resp)
    if "detail" not in response_body and not isMatch(travelRequest, response_body):
        errMessage = f"request {travelRequest} doesn't match with response {response_body}"
        logger.error(errMessage)
        return JSONResponse(
            status_code=500,
            content={"detail": errMessage}
        )

    logger.debug("validation middleware got response %s", response_body)
    return rebuildResponse(resp, response_raw_body)
