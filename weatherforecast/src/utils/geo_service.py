import httpx

class GeoService:
    async def get_coordinates(self, city):
        url = "https://geocoding-api.open-meteo.com/v1/search"

        async with httpx.AsyncClient() as client:
            response = await client.get(url, params={"name": city, "count": 1})
            data = response.json()

            if not data.get("results"):
                raise ValueError(f"City '{city}' not found")

            coordinates = data["results"][0]

            return coordinates["latitude"], coordinates["longitude"]

    async def suggest_city(self, city, count=10):

        url = "https://geocoding-api.open-meteo.com/v1/search"

        params = {
            "name": city,
            "count": count
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()

        results = []
        for place in data.get("results", []):
            results.append({
                "name": place["name"],
                "country": place.get("country", ""),
                "lat": place.get("latitude"),
                "lon": place.get("longitude")
            })

        return results