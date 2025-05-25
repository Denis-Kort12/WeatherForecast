from abc import ABC, abstractmethod
import httpx

class WeatherProvider(ABC):

    @abstractmethod
    def get_weather(self, city):
        pass


class OpenMeteo(WeatherProvider):

    def __init__(self, geo_service):
        self.geo_service = geo_service

    async def get_weather(self, city, lat=None, lon=None):

        url = "https://api.open-meteo.com/v1/forecast"
        async with httpx.AsyncClient() as client:

            if lat is None or lon is None:
                lat, lon = await self.geo_service.get_coordinates(city)

            response = await client.get(url, params={"latitude": lat, "longitude": lon, "current_weather": True})
            data_info = response.json()

            if not data_info.get("current_weather"):
                raise ValueError(f"City '{city}' not found")

            result = {
                "City": city,
                "Current_weather": data_info.get("current_weather").get("temperature"),
                "Current_weather_units": data_info.get("current_weather_units").get("temperature")

            }

            return result
