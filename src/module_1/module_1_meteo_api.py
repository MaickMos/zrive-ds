import openmeteo_requests
import requests_cache
import pandas as pd
import matplotlib.pyplot as plt
#the Libraries were taken from  https://open-meteo.com/en/docs

#From initial code:
API_URL = "https://archive-api.open-meteo.com/v1/archive?"
COORDINATES = {
 "Madrid": {"latitude": 40.416775, "longitude": -3.703790},
 "London": {"latitude": 51.507351, "longitude": -0.127758},
 "Rio": {"latitude": -22.906847, "longitude": -43.172896},}
VARIABLES = ["temperature_2m_min", "precipitation_sum", "wind_speed_10m_max"]

def graphic(city_string,dataframe,VARIABLES):
        fig, ax = plt.subplots(1,3,)

        for city, weather in dataframe.groupby("city"):

            ax[0].set_ylabel(VARIABLES[0])
            ax[0].plot(weather["date"], weather[VARIABLES[0]], label = city)

            ax[1].set_ylabel(VARIABLES[1])
            ax[1].plot(weather["date"], weather[VARIABLES[1]], label = city)

            ax[2].set_ylabel(VARIABLES[2])
            ax[2].plot(weather["date"], weather[VARIABLES[2]], label = city)
            
        fig.suptitle(city_string)
        plt.xlabel("Date")
        plt.show()

def main():
    cities = []
    #Parameters for the request to the API
    for city in COORDINATES:
        params = {
            "latitude" :COORDINATES[city]["latitude"],
            "longitude":COORDINATES[city]["longitude"],
            "start_date": "2025-01-01",
            "end_date": "2025-01-15",
            "daily": VARIABLES}

        #do the request to the client
        request_API_meteo = openmeteo_requests.Client()
        response = request_API_meteo.weather_api(API_URL, params=params)

        daily = response[0].Daily()

        #print(f"City: {city}, Coordinates {response[0].Latitude()}°N {response[0].Longitude()}°E")
        daily_data = {"date" : pd.date_range(
        start = pd.to_datetime(daily.Time(), unit="s", utc=True),
        end = pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
        freq= pd.Timedelta(seconds = daily.Interval()),inclusive="left").date}

        daily_data["city"] = city
        daily_data[VARIABLES[0]] = daily.Variables(0).ValuesAsNumpy()
        daily_data[VARIABLES[1]] = daily.Variables(1).ValuesAsNumpy()
        daily_data[VARIABLES[2]] = daily.Variables(2).ValuesAsNumpy()
        daily_dataframe = pd.DataFrame(data = daily_data)
        cities.append(daily_dataframe)
        #print(daily_dataframe)
    clima  = pd.concat(cities)
    graphic("Madrid",clima,VARIABLES)
    #print(clima)
    #graphic(city_string,dataframe,list_variables,time)

if __name__ == "__main__":
    main()