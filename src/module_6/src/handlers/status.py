from fastapi import APIRouter, HTTPException
from src.handlers.logger_config import logger_status
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from src.handlers import data_models

router = APIRouter()


@router.get(
    "/status",
    response_model=data_models.statusresponse,
    responses={
        200: {"model": data_models.statusresponse},
        500: {"description": "Internal Server Error"},
    },
)
async def get_status() -> data_models.statusresponse:
    try:
        logger_status.info("Request to /status received.")
        return data_models.statusresponse(status="200")
    except Exception as e:
        logger_status.error(f"Error in request to /status: {e}")
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error."
        )
