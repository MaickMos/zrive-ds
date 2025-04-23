# API Design - Module #6

In this module, an API was designed to predict the price of a user's shopping basket using a previously trained model. The goal was to apply good structure and best practices for proper functionality and standardization.

## Endpoints
The available endpoints are:

### `GET /status`
- Description: Checks if the API is active.
#### Successful Response:
```json
{"status": "200"}
```
#### Failed Response:
status_code: 500
```json
{"detail":"Internal server error."}
```

---

### `POST /predict`
- Description: Predicts the total price of the basket for a specific user.
- Parameters: user_id (String)
#### Successful Response:
```json
{
  "user_id": "ABCDEF",
  "predicted_price": 17.25
}
```
#### Failed Response:
status_code: 500
```json
{"detail":"Internal server error."}
```

---

### `GET /metrics`
- Description: Returns basic metrics such as number of calls and average response time for each endpoint.
#### Successful Response:
```json
{
  "metrics": {
    "/predict": {
      "requests": 15,
      "average_time": 0.235
    },
    "/metrics": {
      "requests": 5,
      "average_time": 0.011
    }
  }
}
```
#### Failed Response:
status_code: 500
```json
{"detail":"Internal server error."}
```

---

## Project Structure:
```
project/
├── bin/
│   ├── model.joblib           # Trained machine learning model
├── logs/
│   ├── api.logs               # Log history
├── src/
│   ├── handlers/
│   │   ├── logger_config.py   # Logging configuration
│   │   ├── data_models.py     # Pydantic models
│   │   ├── predict.py         # /predict endpoint logic
│   │   ├── metrics.py         # /metrics endpoint logic
│   │   └── status.py          # /status endpoint logic
│   ├── basket_model/
│   │   ├── basket_model.py    # Model loading and prediction logic
│   │   ├── feature_store.py   # Feature extraction logic
│   │   └── utils/
│   │       ├── feature.py     # Feature extraction utilities
│   │       └── loaders.py     # Model and dataset loading utilities
├── app.py                     # Main server entry point
├── simple_request.py          # Script to send simple requests
├── README.md / Pull-request.md
```

---

## Logging System

The API includes a modular logging system using Python’s `logging`, allowing independent tracking of each endpoint’s activity.

### Features:
- Per-module loggers: Each functionality (`/predict`, `/status`, `/metrics`) has its own logger to distinguish logs by module.
- Log levels:
  - `INFO`: General operations
  - `ERROR`: Exceptions or errors
- Storage: Logs are saved in the `logs/` folder, with the format: timestamp + level + logger name + message.

Example log output:
```
2025-04-23 03:11:00,135 - INFO - status_logger - Request to /status received.
2025-04-23 03:11:06,372 - INFO - predict_logger - request to /predict
2025-04-23 03:11:47,001 - INFO - predict_logger - time total: 20.62
```

---

## Metrics

An internal system was implemented to track usage and performance of the endpoints.

### Features:
- Tracks the number of requests per endpoint.
- Calculates average response time.
- Stores data in memory using `defaultdict`.
- Accessible via the `/metrics` endpoint.
