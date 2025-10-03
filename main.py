from fastapi import FastAPI, Request
import httpx
import os

app = FastAPI()

EPIDEMIC_CLIENT_ID = os.getenv("EPIDEMIC_CLIENT_ID")
EPIDEMIC_CLIENT_SECRET = os.getenv("EPIDEMIC_CLIENT_SECRET")
BASE_URL = "https://partner-content-api.epidemicsound.com"

@app.post("/")
async def proxy(request: Request):
    body = await request.json()
    endpoint = body.get("endpoint")
    params = body.get("params", {})

    if not endpoint:
        return {"error": "Missing 'endpoint'"}

url = f"{BASE_URL}/{endpoint}"  # e.g., .../tracks
async with httpx.AsyncClient() as client:
    response = await client.get(
        url,
        params=params,  # params becomes query string
        auth=(EPIDEMIC_CLIENT_ID, EPIDEMIC_CLIENT_SECRET),
    )
    return response.json()

@app.get("/tracks/{track_id}")
def get_track(track_id: str):
    token_resp = partner_token()
    if "access_token" not in token_resp:
        return JSONResponse(status_code=500, content={"error": "Failed to get partner token"})

    headers = {"Authorization": f"Bearer {token_resp['access_token']}"}
    try:
        resp = requests.get(f"https://api.epidemicsound.com/v1/tracks/{track_id}", headers=headers, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Track request failed: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})
