import requests

from app.serializers import \
    LocationSerializer,\
    LocationDetailsSerializer, \
    ParameterSerializer, \
    ParameterValuesSerializer


def fetch_weather_forcast_for_24_hours():
    url = "https://weatherbit-v1-mashape.p.rapidapi.com/forecast/hourly"

    headers = {
        "X-RapidAPI-Host": "weatherbit-v1-mashape.p.rapidapi.com",
        "X-RapidAPI-Key": "2360ee35bcmsh0ae8e460a3ecd61p15fc6fjsn23fcf3f06fbd"
    }

    querystring = {"lat": "38.5", "lon": "-78.5", "hours": "24"}

    responses = requests.request("GET", url, headers=headers, params=querystring)

    return responses


# def populate_db():
responses = fetch_weather_forcast_for_24_hours()

loc_serializer = LocationSerializer(data='')
if loc_serializer.is_valid():
    loc_serializer.save()

loc_details_serializer = LocationDetailsSerializer(data={k: v for k, v in responses if k != 'data'})
loc_details_serializer.location = loc_serializer
loc_details_serializer.save()

parameter = [{'name': 'atmospheric_pressure', 'measurements': 'bar'},
             {'name': 'solar_radiation', 'measurements': ''},
             {'name': 'ozone', 'measurements': ''},
             {'name': 'precipitations', 'measurements': 'l/m2'},
             {'name': 'wind_speed', 'measurements': 'km/s'},
             {'name': 'uv', 'measurements': ''},
             {'name': 'temperature', 'measurements': 'C'}]
parameter_serializer = ParameterSerializer(data=parameter)
parameter_serializer.location = loc_serializer
parameter_serializer.save()


parameter_value_data = []
for rsp in responses.json()['data']:
    parameter_value_data.append(
        {'atmospheric_pressure': rsp['pres'],
         'solar_radiation': rsp['solar_rad'],
         'ozone': rsp['ozone'],
         'precipitations': rsp['precip'],
         'wind_speed': rsp['wind_spd'],
         'uv': rsp['uv'],
         'temperature': rsp['temp']}
    )

parameter_values_serializer = ParameterValuesSerializer(data=parameter_value_data, many=True)
parameter_values_serializer.parameter = parameter_serializer
parameter_values_serializer.save()
