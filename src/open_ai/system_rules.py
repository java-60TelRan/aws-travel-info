BASE_ASSERT = """You are a helpful assistant."""
COMMON_RULES = """"
All fields of JSON from the rule #1 MUST be placed as specified on that rule
Your JSON MUSTN'T contain any assumptions, typos, comments, and suggestions
currency_code_from" and "currency_code_to" MUST be ISO 4217 three-letter codes.
DO NOT output currency symbols such as $, €, £, ¥.
Only output codes like USD, EUR, ILS, RUB, GBP, etc."""
RULES: dict = {
    "countryTo": BASE_ASSERT + """
    
   1. User's request contains from <country name> to <country name>. Response ONLY one JSON with no additional services and comments
    {
        "country_from":"<country_from name>"
        "country_to":"<country_to name>"
        "capital_to":"<capital of country_to>
        "currency_name_from": "<currency name of the country from>" 
        "currency_name_to": "<currency name of the country to>"
        "currency_code_from": "<currency code (three letters like USD, ILS, etc.) of the country from>" 
        "currency_code_to": "<currency code (three letters, like USD, ILS, etc.) of the country to>"
        
    }

    """ + COMMON_RULES,
    "cityTo": BASE_ASSERT + """
    1. User's request contains from <country_from> to <city_to>. Find country_to matching city_to and response ONLY one JSON with no additional services and comments
    {
        "country_from":"<country_from name>"
        "country_to":"<country_to name>"
        "city_to": "<city_to name>"
        "capital_to":"<capital of country_to>"
        "currency_name_from": "<currency name of the country from>" 
        "currency_name_to": "<currency name of the country to>"
        "currency_code_from": "<currency code (three letters like USD, ILS, etc.) of the country from>" 
        "currency_code_to": "<currency code (three letters, like USD, ILS, etc.) of the country to>"
        
    }
    """ + COMMON_RULES
}
