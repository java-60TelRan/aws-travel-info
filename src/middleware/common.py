import json
from fastapi import Response


async def extractResponseBody(resp: Response):
    body = b""
    async for chunk in resp.body_iterator:
        body += chunk

    # 4. Try JSON parse
    try:
        json_body = json.loads(body)
    except Exception:
        json_body = None
    return body, json_body
def rebuildResponse(resp, body):
    return Response(
        content=body,
        status_code=resp.status_code,
        headers=dict(resp.headers),
        media_type=resp.media_type,
    )
