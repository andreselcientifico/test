from typing import Tuple
import requests
from urllib.parse import quote

async def geocode_address(api_key: str, address: str) -> Tuple[float, float]:
    base_url = "https://maps.googleapis.com/maps/api/geocode/json?"
    params = {"key": api_key, "address": quote(address)}

    response = requests.get(base_url, params=params).json()
    response.keys()

    if response['status'] == 'OK':
        location = response["results"][0]["geometry"]
        return location['location']['lat'] , location['location']['lng']
    else:
        print(response['text'])
        raise Exception("Error in geocoding request")

# Utiliza la función de geocodificación en tu ruta de FastAPI
from fastapi import FastAPI

app = FastAPI()

API_KEY = "AIzaSyD0txU5n7xlPZ3zkEsEjW09yVHmmEVjU4o"

@app.get("/geocode/{address}")
async def geocode(address: str):
    try:
        result = await geocode_address(API_KEY, address)
        return {"latitude": result[0], "longitude": result[1]}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)