from fastapi import APIRouter, HTTPException
from src.handlers.logger_config import logger_metrics
from src.handlers import data_models

from collections import defaultdict

metrics = defaultdict(lambda: {"count": 0, "total_time": 0})

router = APIRouter()


def track_request(endpoint_name: str, duration: float):
    metrics[endpoint_name]["count"] += 1
    metrics[endpoint_name]["total_time"] += duration


def calculate_metrics() -> dict:
    resultado = {}

    for endpoint in metrics:
        data = metrics[endpoint]
        count = data["count"]
        total_time = data["total_time"]

        if count > 0:
            promedio = total_time / count
        else:
            promedio = 0

        resultado[endpoint] = data_models.MetricItem(
            requests=count, average_time=promedio
        )

    return resultado


@router.get(
    "/metrics",
    response_model=data_models.MetricsResponse,
    responses={
        200: {"model": data_models.MetricsResponse},
        500: {"description": "Internal Server Error"},
    },
)
async def get_metrics():
    try:
        logger_metrics.info("A request was received to /metrics")
        return data_models.MetricsResponse(metrics = calculate_metrics())
    except Exception as e:
        logger_metrics.error(f"Error in /metrics: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
