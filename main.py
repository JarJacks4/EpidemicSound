import os
import requests
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import logging

logging.basicConfig(level=logging.INFO)
app = FastAPI()

# Read credentials from env vars
CLIENT_ID = os.environ.get("EPIDEMIC_CLIENT_ID")
CLIENT_SECRET = os.environ.get("EPIDEMIC_CLIENT_SECRET")

@app.get("/partner-token")
def partner_token():
    if not CLIENT_ID or not CLIENT_SECRET:
        return JSONResponse(status_code=500, content={"error": "Client ID or Secret not set"})

    url = "https://api.epidemicsound.com/v1/partner/token"
    data = {"grant_type": "client_credentials", "client_id": CLIENT_ID, "client_secret": CLIENT_SECRET}

    try:
        resp = requests.post(url, data=data, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Partner token request failed: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})

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
