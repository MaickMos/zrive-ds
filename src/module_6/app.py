import uvicorn
from fastapi import FastAPI
import time

from src.basket_model import feature_store
from src.basket_model import basket_model

# Create an instance of FastAPI
app = FastAPI()

# Define a route for the root URL ("/")
@app.get("/status")
def get_status():
    return {"status": "200"}

@app.post("/predict")
def predict(user_id: int):
    start_time = time.time()

    try:
        user_feature = feature_store.get_features(user_id)
        prediction = basket_model.model.predict(user_feature)[0]

        response_time = time.time() - start_time
        print(f"log time response:{response_time}")

        return {"user_id": user_id, "predicted_price": prediction}


    except Exception as e:
        print("error")
    

# This block allows you to run the application using Uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)