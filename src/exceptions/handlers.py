
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError


async def requestValidationHandler(req: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={"detail":str(exc)}
    )

async def errorFromServer(req: Request, exc: ValidationError) :
    return JSONResponse(
        status_code=500,
        content={
            "detail": str(exc)
        }
        
    )  
def registerExceptionHandlers(app) :
    app.add_exception_handler(RequestValidationError, requestValidationHandler)
    app.add_exception_handler(ValidationError, errorFromServer)   
