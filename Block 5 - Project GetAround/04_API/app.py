import mlflow 
import uvicorn
import pandas as pd 
from pydantic import BaseModel, validator
from typing import Literal, List, Union, Optional
from fastapi import FastAPI, File, UploadFile, HTTPException
import joblib
import requests

description = """
Welcome to this car prediction rental price API. 
It uses the model developed to predict the rental price of a car based on its characteristics.

## Machine Learning

This is a Machine Learning endpoint that predicts the rental price of a car.

Check out documentation below 👇 for more information on each endpoint. 
"""

tags_metadata = [
    {
        "name": "Introduction Endpoints",
        "description": "Basic endpoints for API information."
    },
    {
        "name": "Machine Learning",
        "description": "Prediction Endpoint for car rental price."
    }
]

app = FastAPI(
    title="Car Rental Price Prediction",
    description=description,
    version="0.1",
    contact={
        "name": "Louis Le Pogam",
        "mail": "l.lepogam@gmail.com",
    },
    openapi_tags=tags_metadata
)

# Define valid options for categorical fields
VALID_MODEL_KEYS = ['Citroën', 'Peugeot', 'PGO', 'Renault', 'Audi', 'BMW', 'Ford', 
                    'Mercedes', 'Opel', 'Porsche', 'Volkswagen', 'Others', 'Ferrari', 
                    'Maserati', 'Mitsubishi', 'Nissan', 'SEAT', 'Subaru', 'Suzuki', 'Toyota']

VALID_FUEL_TYPES = ['diesel', 'petrol', 'hybrid_petrol', 'electro']

VALID_PAINT_COLORS = ['black', 'grey', 'white', 'red', 'silver', 'blue', 
                      'orange', 'beige', 'brown', 'green']

VALID_CAR_TYPES = ['convertible', 'coupe', 'estate', 'hatchback', 
                   'sedan', 'subcompact', 'suv', 'van']

class CarRentalFeatures(BaseModel):
    """
    Features required for car rental price prediction.
    All fields are required as per the model schema.
    """
    model_key: str
    mileage: int
    engine_power: int
    fuel: str
    paint_color: str
    car_type: str
    private_parking_available: bool
    has_gps: bool
    has_air_conditioning: bool
    automatic_car: bool
    has_getaround_connect: bool
    has_speed_regulator: bool
    winter_tires: bool
    
    # Validators for categorical fields
    @validator('model_key')
    def validate_model_key(cls, v):
        if v not in VALID_MODEL_KEYS:
            return 'Others'
        return v
    
    @validator('fuel')
    def validate_fuel(cls, v):
        if v not in VALID_FUEL_TYPES:
            raise ValueError(f"Invalid fuel type. Must be one of: {', '.join(VALID_FUEL_TYPES)}")
        return v
    
    @validator('paint_color')
    def validate_paint_color(cls, v):
        if v not in VALID_PAINT_COLORS:
            raise ValueError(f"Invalid paint color. Must be one of: {', '.join(VALID_PAINT_COLORS)}")
        return v
    
    @validator('car_type')
    def validate_car_type(cls, v):
        # Convert to lowercase for case-insensitive comparison
        v_lower = v.lower()
        if v_lower not in VALID_CAR_TYPES:
            raise ValueError(f"Invalid car type. Must be one of: {', '.join(VALID_CAR_TYPES)}")
        # Return the lowercase version to ensure consistency
        return v_lower
    
    # Validators for boolean fields to ensure correct conversion
    @validator('private_parking_available', 'has_gps', 'has_air_conditioning', 
               'automatic_car', 'has_getaround_connect', 'has_speed_regulator', 
               'winter_tires', pre=True)
    def convert_to_bool(cls, v):
        if isinstance(v, bool):
            return v
        if isinstance(v, str):
            if v.lower() in ('true', 't', 'yes', 'y', '1'):
                return True
            elif v.lower() in ('false', 'f', 'no', 'n', '0'):
                return False
        elif isinstance(v, int):
            return bool(v)
        
        raise ValueError("Boolean value expected")

@app.get("/", tags=["Introduction Endpoints"])
async def index():
    """
    Simply returns a welcome message!
    """
    message = "Welcome to the Car Rental Price Prediction API. If you want to learn more, check out documentation of the api at `/docs`"
    return message

@app.post("/predict", tags=["Machine Learning"])
async def predict(features: CarRentalFeatures):
    """
    Predicts the rental price of a car based on its characteristics.

    ### Input
    - `features` (CarRentalFeatures): An object containing all required car characteristics.

    ### Required Fields:
    - `model_key` (string): The model of the car. 
      - Accepted values: 'Citroën', 'Peugeot', 'PGO', 'Renault', 'Audi', 'BMW', 'Ford', 'Mercedes', 'Opel', 'Porsche', 'Volkswagen', 'Ferrari', 'Maserati', 'Mitsubishi', 'Nissan', 'SEAT', 'Subaru', 'Suzuki', 'Toyota', 'Others'
      - Note: If a value not in this list is provided, it will be automatically converted to 'Others'
    - `mileage` (integer): The mileage of the car in kilometers
      - Example: 150000
    - `engine_power` (integer): The engine power in horsepower
      - Example: 110
    - `fuel` (string): The fuel type
      - Accepted values: 'diesel', 'petrol', 'hybrid_petrol', 'electro'
    - `paint_color` (string): The color of the car
      - Accepted values: 'black', 'grey', 'white', 'red', 'silver', 'blue', 'orange', 'beige', 'brown', 'green'
    - `car_type` (string): The type of car
      - Accepted values: 'convertible', 'coupe', 'estate', 'hatchback', 'sedan', 'subcompact', 'suv', 'van'
      - Note: Case-insensitive, will be converted to lowercase
    - `private_parking_available` (boolean): Whether private parking is available
    - `has_gps` (boolean): Whether the car has GPS
    - `has_air_conditioning` (boolean): Whether the car has air conditioning
    - `automatic_car` (boolean): Whether the car has automatic transmission
    - `has_getaround_connect` (boolean): Whether the car has Getaround Connect feature
    - `has_speed_regulator` (boolean): Whether the car has speed regulator/cruise control
    - `winter_tires` (boolean): Whether the car has winter tires

    ### Output
    Returns a dictionary with the following keys:
    - `predicted_price` (float): The predicted rental price per day in the local currency
    - `model_version` (string): The version of the model used for prediction

    ### Example Usage
    To use this endpoint, send a POST request as follows:

    ```python
    import requests

    url = "https://llepogam-getaround-price-prediction.hf.space/predict"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }

    data = {
        "model_key": "Citroën",
        "mileage": 150000,
        "engine_power": 110,
        "fuel": "diesel",
        "paint_color": "black",
        "car_type": "sedan",
        "private_parking_available": True,
        "has_gps": True,
        "has_air_conditioning": True,
        "automatic_car": True,
        "has_getaround_connect": True,
        "has_speed_regulator": True,
        "winter_tires": True
    }

    response = requests.post(url, headers=headers, json=data)
    print(response.json())
    ```
    """
    # Convert the Pydantic model to a dictionary
    features_dict = features.dict()
    
    # Create a pandas DataFrame with a single row for the prediction
    df = pd.DataFrame([features_dict])
    
    # Load model from MLflow
    logged_model = 'runs:/04a2f87761b844b1ab079f789c8c0cef/pipeline_model'
    loaded_model = mlflow.pyfunc.load_model(logged_model)
    
    # Perform prediction
    prediction = loaded_model.predict(df)
    
    # Format and return the response
    result = {
        "predicted_price": float(prediction[0]),
        "model_version": "04a2f87761b844b1ab079f789c8c0cef"
    }
    
    return result