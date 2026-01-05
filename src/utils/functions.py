import json
import re


def extractJSON(text: str, properties: list[str]) -> dict | None:
    propsInRe = '.' + '.'.join(f"*{w}" for w in properties)
    regex:str = fr"\{{{propsInRe}.*\}}"
    match: re.Match = re.search(regex, text, re.DOTALL)
    res = None
    if match:
        try:
            res = json.loads(match.group())
        except Exception:
            pass    
    return res        