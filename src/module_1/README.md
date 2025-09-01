# Module 1 Submission

## Results
The requested data was obtained and plotted in subplots that vary depending on the number of requested variables. The cities called depend on the coordinates provided in the initial dictionary. Example: Madrid plot with three variables per year:  
![plots](https://github.com/user-attachments/assets/d225a42e-7528-48f8-b7ca-ab686dbcb5b6)

The plot frequency is controlled using the _Frequency_ parameter from the _pandas_ library, which can be set to daily "D", monthly "ME", or yearly "A".

## API Calls
The initial requirements were met. Initially, the implementation followed the documentation available at [Open-meteo](https://open-meteo.com/en/docs) using the `openmeteo_requests` library, which can be installed with:

'''
pip install openmeteo-requests
poetry add openmeteo-requests
'''

Most of the practice was done using this library, but issues arose when creating a generic function for connecting to the API, since it lacked a  

.statuscode or raise_for_status()


Later, data retrieval was done using the `requests` library, so part of the code was rewritten.

Therefore, there are two main functions for obtaining data:

get_data_meteo_api()
get_data_meteo_api_openmeteo_requests()

Each method has its own function to call the API.

## Tests
Since I had no prior experience with unit testing, I used ChatGPT for guidance and explanations. The tests validate:

- `HTTPError` exception from API requests
- Functionality of the plotting function
- Correct response from the `requests` function
- Correct response from the `openmeteo_requests` function

Code reviewer: @sergiorozada12
