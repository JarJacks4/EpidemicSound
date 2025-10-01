import os
import requests
from fastapi import FastAPI

app = FastAPI()

CLIENT_ID = os.environ.get("EPIDEMIC_CLIENT_ID")
CLIENT_SECRET = os.environ.get("EPIDEMIC_CLIENT_SECRET")

@app.get("/partner-token")
def get_partner_token():
    url = "https://api.epidemicsound.com/v1/partner/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    resp = requests.post(url, data=data)
    if resp.status_code != 200:
        return {"error": resp.json()}
    return resp.json()


@app.get("/tracks/{track_id}")
def get_track(track_id: str):
    token_resp = get_partner_token()
    if "access_token" not in token_resp:
        return {"error": "Auth failed"}
    
    headers = {"Authorization": f"Bearer {token_resp['access_token']}"}
    url = f"https://api.epidemicsound.com/v1/tracks/{track_id}"
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        return {"error": resp.json()}
    return resp.json()
