import unittest
from unittest.mock import patch, Mock
import requests
import pandas as pd
from src.module_1.module_1_meteo_api import (
    graphic,
    call_api_requests,
    call_api_openmeteo_requests,
    get_data_meteo_api,
)

# This unittest was powered by chatgpt, because I have never done an unittest before
# however I tried to understand what is doing and searched every that I didn't understand


# Declarate a class because unittest use class to organice the test
class test_module_1_meteo_functions(unittest.TestCase):
    # patch for "reemplace" the orginal function for the test
    @patch("src.module_1.module_1_meteo_api.requests.get")
    def test_call_api_requests_HTTPError(self, mock_get):
        # Create the object mock, it's going to do the simulation of external factors
        mock_response = Mock()
        # indicate whats will be the answer
        mock_response.raise_for_status = Mock(
            side_effect=requests.exceptions.HTTPError("404")
        )

        # define what the mock have to get for a correct test
        mock_get.return_value = mock_response
        with self.assertRaises(requests.exceptions.HTTPError):
            call_api_requests("url", {"noting": "none"})

    # Self To reference the same object
    def test_graphic(self):
        # define the data for test
        weather = pd.DataFrame(
            {
                "date": pd.date_range("2020-01-01", "2020-12-31", freq="ME"),
                "city": ["Madrid"] * 12,
                "temperature_2m_mean": range(12),
                "precipitation_sum": range(10, 22),
                "wind_speed_10m_max": range(5, 17),
            }
        )
        variables_to_graph = ["temperature_2m_mean", "precipitation_sum"]
        frequency = "M"

        # Test that the function runs without errors
        try:
            # Call the function
            graphic(weather, variables_to_graph, frequency)
        except Exception as e:
            self.fail(f"graphic() raised an exception: {e}")

    @patch("src.module_1.module_1_meteo_api.requests.get")
    def test_call_api_requests(self, mock_get):
        # Mocking API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": "mocked_data"}
        mock_get.return_value = mock_response

        # Test
        url = "https://example.com/api"
        params = {"param1": "value1"}
        # For a correct answer
        result = call_api_requests(url, params)
        self.assertEqual(result.status_code, 200)

        # verific the answer be a json
        self.assertEqual(result.json(), {"data": "mocked_data"})
        mock_get.assert_called_once_with(url, params=params)

    @patch("src.module_1.module_1_meteo_api.openmeteo_requests.Client")
    def test_call_api_openmeteo_requests(self, mock_client):
        # Mocking API response
        mock_api_response = Mock()
        mock_api_response.__getstate__ = Mock(return_value=200)
        mock_api_response.Daily.return_value = {"data": "mocked_data"}
        mock_client_instance = Mock()
        mock_client_instance.weather_api.return_value = [mock_api_response]
        mock_client.return_value = mock_client_instance

        # Test
        url = "https://example.com/api"
        params = {"param1": "value1"}

        result = call_api_openmeteo_requests(url, params)
        self.assertEqual(result, {"data": "mocked_data"})
        mock_client_instance.weather_api.assert_called_once_with(url, params=params)


if __name__ == "__main__":
    unittest.main()
