import openmeteo_requests
import requests
import pandas as pd
import matplotlib.pyplot as plt
#the Libraries were taken from  https://open-meteo.com/en/docs



def graphic(weather,variables_to_graph,frequency):

    """
    Graph a dataframe in temporal series


    Parameters:
    - weather: dataframe in temporal series
    - variables_to_graph: List of the header of the column in the dataframe to graph
      ["temperature_2m_min","temperature_2m_max", "precipitation_sum", "wind_speed_10m_max"]
    - frequency: caracter to indicates the frecuency: "Y", "M", "D" 

    Return:
    -A graph with subplot for each variable, let various cities 
    """

    subtitle = {"temperature_2m_mean": "Average Temperature",
                "precipitation_sum":"Sum of precipitation",
                "wind_speed_10m_max":"Wind speed"}
    
    #convert the column data in data format
    weather["date"] = pd.to_datetime(weather["date"])  
    
    #do the cycle for each city in the dataframe 
    for city, data_by_city in weather.groupby("city"):

        #create a subplot for the number varaible in the list
        fig, ax = plt.subplots(1,len(variables_to_graph),)

        #obtain the mean  agroup by the frecuency
        average_data = data_by_city.groupby(data_by_city["date"].dt.to_period(frequency))[variables_to_graph].mean()
        average_data.reset_index(inplace=True)
        average_data["date"] = average_data["date"].dt.to_timestamp()

        #Do the cycle for each varaible
        for i in range(len(variables_to_graph)):
            #if there is just a plot
            if len(variables_to_graph) == 1:
                ax.set_ylabel(subtitle[variables_to_graph[i]])
                ax.plot(average_data["date"], average_data[variables_to_graph[i]], marker = "o", label = subtitle[variables_to_graph[i]])
                ax.legend()
                ax.grid(True)
            else:
                #if there are more than one plot
                ax[i].set_ylabel(subtitle[variables_to_graph[i]])
                ax[i].plot(average_data["date"], average_data[variables_to_graph[i]], marker = "o", label = subtitle[variables_to_graph[i]])
                ax[i].legend()
                ax[i].grid(True)
        print(city)  
        print(average_data)
        fig.suptitle(city)
            
    plt.show()

def call_api_requests(url, params):
    """
    Request to the API with library request

    Parámetros:
    - url: the string url
    - params: parameters for the API openmeteorequest 
        Example:
            params = {
                "latitude" :C 40.416775,
                "longitude":-3.70379,
                "start_date": "01/01/2010",
                "end_date": "01/01/2010",
                "daily": ["temperature_2m_min","temperature_2m_max", "precipitation_sum", "wind_speed_10m_max"]}

    Retorna:
    a type object response
    """

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

    """
    Request to the API with library openmeteo_requests

    Parámetros:
    - url: the string url
    - params: parameters for the API openmeteorequest 
        Example:
            params = {
                "latitude" :C 40.416775,
                "longitude":-3.70379,
                "start_date": "01/01/2010",
                "end_date": "01/01/2010",
                "daily": ["temperature_2m_min","temperature_2m_max", "precipitation_sum", "wind_speed_10m_max"]}

    return:
    a type object WeatherApiResponse
    """

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
            print("Get the data from API, but error not code 200")

        #the object WeatherApiResponse doesn't have the atribute getstate (i found __getstate__ but doesn't work)
        #so for now im not do the status code and just return the object

        daily = response[0].Daily()
        return daily

    except Exception as e:
        print("Error in :", e)
        

def get_data_meteo_api(cities,start_date,end_date):
    
    """
    Get the meteorology data from API openmeteo_requests

    Parámetros:
    - cities: list of the list to get data
    - start_date: date initial to get the data
        "2010-01-01"
    - end_date: date final to get the data
        "2020-12-31"
    
    Retorna:
    A dataframe of the cities and variables
    """

    #From initial code:
    API_URL = "https://archive-api.open-meteo.com/v1/archive?"
    COORDINATES = {
    "Madrid": {"latitude": 40.416775, "longitude": -3.703790},
    "London": {"latitude": 51.507351, "longitude": -0.127758},
    "Rio": {"latitude": -22.906847, "longitude": -43.172896},}
    VARIABLES = ["temperature_2m_min","temperature_2m_max", "precipitation_sum", "wind_speed_10m_max"]
    
    cities_list_dataframe = []
        #Do the cicle for each city in list cities
    for city in cities:
        #Parameters for the request to the API
        params = {
            "latitude" :COORDINATES[city]["latitude"],
            "longitude":COORDINATES[city]["longitude"],
            "start_date": start_date,
            "end_date": end_date,
            "daily": VARIABLES}

        #Call the api with the library
        daily = call_api_openmeteo_requests(API_URL,params)

        #Create the column of the date since start date to final date with the frecuency dairy
        daily_data = {"date" : pd.date_range(
        start = pd.to_datetime(daily.Time(), unit="s", utc=True),
        end = pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
        freq= pd.Timedelta(seconds = daily.Interval()),inclusive="left").date}

        #create a column with the city
        daily_data["city"] = city
        #set the variables in the respective column
        for i, variable in enumerate(VARIABLES):
            daily_data[variable] = daily.Variables(i).ValuesAsNumpy()
        
        #Create a dataframe and save in a list of dataframe then concat
        daily_dataframe = pd.DataFrame(data = daily_data)
        cities_list_dataframe.append(daily_dataframe)
        
    #join the dataframe in the same dataframe
    weather  = pd.concat(cities_list_dataframe)
    #check  if exists the two varaibles of temperature to calculate the mean
    if "temperature_2m_min" and "temperature_2m_max" in VARIABLES:
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
