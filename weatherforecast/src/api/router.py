from fastapi import APIRouter, Request, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse

from src.utils.geo_service import GeoService
from src.utils.weather import OpenMeteo

router = APIRouter(prefix='', tags=['API'])
templates = Jinja2Templates(directory='src/templates')


geo_service = GeoService()
weather_provider = OpenMeteo(geo_service)

@router.get('/')
async def get_main_page(request: Request):
    last_city = request.cookies.get("last_city", "")

    return templates.TemplateResponse(name='index.html', context={"request": request, "last_city": last_city})


@router.post('/weather')
async def get_weather(request: Request, response: Response):
    data = await request.json()

    city = country = lat = lon = None
    list_info = data.get("city").split(",")

    if len(list_info) == 4:
        city, country, lat, lon = map(str.strip, list_info)
    else:
        city = list_info[0]

    try:
        weather = await weather_provider.get_weather(city=city, lat=lat, lon=lon)
    except ValueError as e:
        return JSONResponse(status_code=400, content={"text": str(e)})

    response.set_cookie(key="last_city", value=city, max_age=60*60*24*2)

    return weather


@router.post("/suggest_city")
async def suggest_city(request: Request):
    data = await request.json()

    city = data.get("city")

    return await geo_service.suggest_city(city=city, count=15)
