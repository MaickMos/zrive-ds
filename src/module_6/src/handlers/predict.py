import time
from src.handlers.logger_config import logger_predict
from src.handlers import data_models
from src.basket_model import feature_store
from src.basket_model import basket_model
from fastapi import APIRouter, HTTPException, Request
from src.handlers import metrics

router = APIRouter()

@router.post(
        "/predict",
        response_model=data_models.predictionresponse,
    responses={
        200: {"model": data_models.predictionresponse},
        500: {"description": "Internal Server Error"},
    },
        )
def process_predict(user_id: str):
    start_time = time.time()
    logger_predict.info("request to /predict")

    try:
        fs = feature_store.FeatureStore()
        user_feature = fs.get_features(user_id)


        bs = basket_model.BasketModel()
        user_feature = user_feature.values.reshape(1, -1)
        prediction = bs.model.predict(user_feature)[0]

        response_time = time.time() - start_time

        metrics.track_request("predict", response_time)
        logger_predict.info(f"time total:{response_time}")
        
        #return {"user_id": user_id, "predicted_price": prediction}
        return data_models.predictionresponse(user_id=user_id, predicted_price=prediction)


    except Exception as e:
        logger_predict.info(f"error in request to /predict: {e}")
        raise HTTPException(status_code=500, detail="Internal server error.")