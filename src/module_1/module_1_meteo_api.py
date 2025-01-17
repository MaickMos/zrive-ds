import openmeteo_requests
import requests_cache
import pandas as pd
#the Libraries were taken from  https://open-meteo.com/en/docs

#From initial code:
API_URL = "https://archive-api.open-meteo.com/v1/archive?"
COORDINATES = {
 "Madrid": {"latitude": 40.416775, "longitude": -3.703790},
 "London": {"latitude": 51.507351, "longitude": -0.127758},
 "Rio": {"latitude": -22.906847, "longitude": -43.172896},}
VARIABLES = ["temperature_2m_mean", "precipitation_sum", "wind_speed_10m_max"]


def main():

    params = {
        "latitude" :40.416775,
        "longitude":-3.703790,
        "start_date": "2025-01-01",
	    "end_date": "2025-01-15",
        "daitly": ["temperature_2m_min"]
    }

    request_API_meteo = openmeteo_requests.Client()
    data = request_API_meteo.weather_api(API_URL, params=params)
    reponse= data[0]
    daily = reponse.Daily()

    print(f"Coordinates {reponse.Latitude()}°N {reponse.Longitude()}°E")
    daily_data = {"date" : pd.date_range(
    start = pd.to_datetime(daily.Time),
    end = pd.to_datetime(daily.TimeEnd),
    freq= pd.Timedelta(seconds = daily.Interval()))}

    daily_data["temperature_2m_min"] = daily.Variables(0).ValuesAsNumpy()

    daily_dataframe = pd.DataFrame(data = daily_data)
    print(daily_dataframe)


if __name__ == "__main__":
 main()