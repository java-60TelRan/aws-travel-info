import requests
URL = "https://data.fixer.io/api/latest"
ACCESS_KEY = "b2d71961ebe71a300a02e73d03b6ebc8"
def getExchangeRate(codeFrom:str, codeTo:str)->float:
    resp = requests.get(URL, params={"access_key":ACCESS_KEY})
    resp.raise_for_status()
    rates = resp.json()["rates"]
    rateFrom = rates[codeFrom]
    rateTo = rates[codeTo]
    return round(rateTo / rateFrom, 2)