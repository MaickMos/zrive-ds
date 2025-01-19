import openmeteo_requests
import requests
import pandas as pd
import matplotlib.pyplot as plt
#the Libraries were taken from  https://open-meteo.com/en/docs



def graphic(weather,variables_to_graph,frequency):
    subtitle = {"temperature_2m_mean": "Average Temperature",
                "precipitation_sum":"Sum of precipitation",
                "wind_speed_10m_max":"Wind speed"}
    
    weather["date"] = pd.to_datetime(weather["date"])  
    print(weather)

    for city, data_by_city in weather.groupby("city"):

        fig, ax = plt.subplots(1,len(variables_to_graph),)

        average_month = data_by_city.groupby(data_by_city["date"].dt.to_period(frequency))[variables_to_graph].mean()
        average_month.reset_index(inplace=True)
        average_month["date"] = average_month["date"].dt.to_timestamp()

        for i in range(len(variables_to_graph)):
            if len(variables_to_graph) == 1:
                ax.set_ylabel(subtitle[variables_to_graph[i]])
                ax.plot(average_month["date"], average_month[variables_to_graph[i]], marker = "o", label = subtitle[variables_to_graph[i]])
                ax.legend()
                ax.grid(True)
            else:
                ax[i].set_ylabel(subtitle[variables_to_graph[i]])
                ax[i].plot(average_month["date"], average_month[variables_to_graph[i]], marker = "o", label = subtitle[variables_to_graph[i]])
                ax[i].legend()
                ax[i].grid(True)
        print(city)  
        print(average_month)
        fig.suptitle(city)
            
    plt.show()

def call_api_requests(url, params):

    #Do the request to the client
    response = requests.get(url, params=params, headers=None, timeout=10)

    #veriicate the state of request
    #if is 200 is correct, get the data

    if response.status_code == 200:
        daily = response.Daily()
        print("Get the data correctly")
        return daily
    else:
        print("Error not code 200")


def call_api_openmeteo_requests(url, params):
    try:
        #Do the request to the client with the library
        request_API_meteo = openmeteo_requests.Client()
        response = request_API_meteo.weather_api(url, params=params)
        #this request get a list of object WeatherApiResponse
        #request = response[0]
        #veriicate the state of request
        #if is 200 is correct, get the data
        

        
        if response[0].__getstate__ == 200:
            daily = response[0].Daily()
            print("Get the data correctly")
            return daily
        else:
            print("Error not code 200")

        #while fix how to get a status code
        daily = response[0].Daily()
        return daily

    except Exception as e:
        print("Error in :", e)
        

def get_data_meteo_api(cities,start_date,end_date):
    #From initial code:
    API_URL = "https://archive-api.open-meteo.com/v1/archive?"
    COORDINATES = {
    "Madrid": {"latitude": 40.416775, "longitude": -3.703790},
    "London": {"latitude": 51.507351, "longitude": -0.127758},
    "Rio": {"latitude": -22.906847, "longitude": -43.172896},}
    VARIABLES = ["temperature_2m_min","temperature_2m_max", "precipitation_sum", "wind_speed_10m_max"]
    
    cities_list_dataframe = []
    #Parameters for the request to the API
    for city in cities:
        params = {
            "latitude" :COORDINATES[city]["latitude"],
            "longitude":COORDINATES[city]["longitude"],
            "start_date": start_date,
            "end_date": end_date,
            "daily": VARIABLES}

        daily = call_api_openmeteo_requests(API_URL,params)

        #print(f"City: {city}, Coordinates {response[0].Latitude()}°N {response[0].Longitude()}°E")
        daily_data = {"date" : pd.date_range(
        start = pd.to_datetime(daily.Time(), unit="s", utc=True),
        end = pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
        freq= pd.Timedelta(seconds = daily.Interval()),inclusive="left").date}

        daily_data["city"] = city
        daily_data[VARIABLES[0]] = daily.Variables(0).ValuesAsNumpy()
        daily_data[VARIABLES[1]] = daily.Variables(1).ValuesAsNumpy()
        daily_data[VARIABLES[2]] = daily.Variables(2).ValuesAsNumpy()
        daily_data[VARIABLES[3]] = daily.Variables(3).ValuesAsNumpy()
        
        daily_dataframe = pd.DataFrame(data = daily_data)
        cities_list_dataframe.append(daily_dataframe)
        #print(daily_dataframe)
    weather  = pd.concat(cities_list_dataframe)
    weather["temperature_2m_mean"] = (weather["temperature_2m_min"]+weather["temperature_2m_max"])/2
    return weather    


def main():
    cities = ["Madrid","London","Rio"]
    start_date = "2010-01-01"
    end_date = "2020-12-31"
    variables_to_graph  = ["temperature_2m_mean", "precipitation_sum", "wind_speed_10m_max"]
    frequency = "A"

    data = get_data_meteo_api(cities,start_date,end_date)
    graphic(data,variables_to_graph,frequency)

if __name__ == "__main__":
    main()