from pydantic import BaseModel, model_validator
class TravelRequest(BaseModel):
    countryFrom: str 
    cityTo: str | None = None
    countryTo: str | None = None
    iscapital: bool
    isweather: bool
    iscurrency: bool
    @model_validator(mode="after")
    def cityToXorCountryTo(self):
        if bool(self.cityTo) == bool(self.countryTo):
            raise ValueError("There must be exactly one field that is either cityTo or countryTo")
        return self