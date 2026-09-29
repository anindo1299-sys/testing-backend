from fastapi import Depends
from core.httpx_client import get_httpx_client
from core.config import get_settings, Setting
import httpx

async def fetch_weather_data(
        city_name: str,
        settings: Setting = Depends(get_httpx_client),
        client: httpx.AsyncClient = Depends(get_httpx_client)
):
    Base_url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 52.52,
        "longitude": 13.41,
        "current_weather": True
    }

    headers = {
        "X-API-KEY": settings.API_AUTH_KEY,
        "User-Agent": "FastAPI-WeatherApp/1.0"
    }

    response = await client.get(Base_url, params=params, headers=headers)
    response.raise_for_status()

    return response.json()