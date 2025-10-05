from fastapi import FastAPI, Request
import httpx
import os

app = FastAPI()

# Load your Epidemic Partner credentials from environment variables
EPIDEMIC_CLIENT_ID = os.getenv("EPIDEMIC_CLIENT_ID")
EPIDEMIC_CLIENT_SECRET = os.getenv("EPIDEMIC_CLIENT_SECRET")

# Partner Content API base
BASE_URL = "https://partner-content-api.epidemicsound.com"

@app.post("/")
async def proxy(request: Request):
    body = await request.json()
    endpoint = body.get("endpoint")  # e.g., "tracks"
    params = body.get("params", {})  # e.g., {"per_page":5,"query":"jazz"}

    if not endpoint:
        return {"error": "Missing 'endpoint' in body"}

    url = f"{BASE_URL}/{endpoint}"

    try:
        async with httpx.AsyncClient() as client:
            # Send GET request to Epidemic with basic auth
            response = await client.get(
                url,
                params=params,  # passes as query string
                auth=(EPIDEMIC_CLIENT_ID, EPIDEMIC_CLIENT_SECRET)
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        return {
            "status": e.response.status_code,
            "detail": e.response.text
        }
    except Exception as e:
        return {"error": str(e)}
