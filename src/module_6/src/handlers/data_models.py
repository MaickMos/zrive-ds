from pydantic import BaseModel
from typing import Dict


class statusresponse(BaseModel):
    status: str


class predictionresponse(BaseModel):
    user_id: str
    predicted_price: float


class MetricItem(BaseModel):
    requests: int
    average_time: float


class MetricsResponse(BaseModel):
    metrics: Dict[str, MetricItem]
