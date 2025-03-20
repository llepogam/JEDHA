import mlflow 
import uvicorn
import pandas as pd 
from pydantic import BaseModel
from typing import Literal, List, Union
from fastapi import FastAPI, File, UploadFile
import joblib
import requests

description = """
Welcome to this offensive speech detection API. 
It uses the model developped to detect if a tweet has hate speech or not

## Machine Learning

This is a Machine Learning endpoint that predict if a text is a hate speech or not with a certain degree of certainity. Here is the endpoint:

* `/predict` that accepts string value
* `/preprocess` that accepts string value


Check out documentation below 👇 for more information on each endpoint. 
"""

tags_metadata = [

    {
        "name": "Machine Learning",
        "description": "Prediction Endpoint."
    }
]

app = FastAPI(
    title="Offensive speech detection",
    description=description,
    version="0.1",
    contact={
        "name": "Louis Le Pogam",
        "mail": "l.lepogam@gmail.com",
    },
    openapi_tags=tags_metadata
)



class PredictionFeatures(BaseModel):
    Text: str

class PreprocessingFeatures(BaseModel):
    tweet: str


@app.get("/", tags=["Introduction Endpoints"])
async def index():
    """
    Simply returns a welcome message!
    """
    message ="If you want to learn more, check out documentation of the api at `/docs`"
    return message







@app.post("/predict", tags=["Machine Learning"])
async def predict(predictionFeatures: PredictionFeatures):
    """
    Predict whether the provided text contains hate speech.

    ### Input
    - `predictionFeatures` (PredictionFeatures): An object containing the text to be analyzed.
      - `predictionFeatures` is a dictionnary with 'Text' as only key
      - The input text is provided as a string as a value of the 'Text' key

    ### Output
    Returns a dictionary with the following keys:
    - `prediction` (str): Indicates whether the text is "offensive" or "not offensive".
    - `probability` (float): A value between 0 and 1, representing the likelihood of hate speech.
      - Texts with a probability >= 0.5 are classified as "offensive".

    ### Example Usage
    To use this endpoint, send a POST request as follows:

    ```python
    import requests

    url = "https://llepogam-hate-speech-detection-api.hf.space/predict"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }

    data = {
        "Text": "your text here"
    }

    response = requests.post(url, headers=headers, json=data)
    print(response.json())
    ```
    """

    # Copy the preprocess method to avoid issue
    list_text_for_preprocessing = [predictionFeatures.Text]

    # Load model from MLflow
    logged_model = 'runs:/89b183556cf34460858d94125f8df98d/text_preprocessor'
    loaded_model = mlflow.pyfunc.load_model(logged_model)

    df = pd.DataFrame(list_text_for_preprocessing,columns=['tweet'])

    # Perform prediction
    preprocessed_result = loaded_model.predict(pd.DataFrame(df))

    df_preprocessed = pd.DataFrame(preprocessed_result)

    list_text = [df_preprocessed.loc[0,"text_clean"]]

    # Load model from MLflow
    logged_model = 'runs:/227d2f8e431d40d6b5231add3a00d048/hate_speech_detection'
    loaded_model = mlflow.pyfunc.load_model(logged_model)

    df = pd.DataFrame(list_text)

    # Perform prediction
    test_pred_prod = loaded_model.predict(df)
    test_pred = (test_pred_prod > 0.5).astype(int)
    test_pred_final = ["offensive" if pred == 1 else "not offensive" for pred in test_pred]


    result = {
        "prediction": test_pred_final[0],
        "probability": float(test_pred_prod[0][0])
    }

    # Format and return the response
    return result



@app.post("/preprocess", tags=["Machine Learning"])
async def preprocess_text(preprocessingFeatures: PreprocessingFeatures):
    """
    This method will preprocess a raw tweet.This intermediate method is used as the preprocessing cannot be simply included in the prediction model
 
    ### Input
    - `preprocessingFeatures` (PreprocessingFeatures): An object containing the tweet to be preprocessed.
      - `predictionFeatures` is a dictionnary with 'tweet' as only key
      - The input text is provided as a string as a value of the 'tweet' key

    ### Output
    Returns a dictionary with the following keys:
    - `tweet` (str): Initial tweet.
    - `text_clean` (str): Preprocessed tweets after removal of punctation and stop words and text lemmatization.

    ### Example Usage
    To use this endpoint, send a POST request as follows:

    ```python
    import requests

    url = "https://llepogam-hate-speech-detection-api.hf.space/preprocess"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }

    data = {
        "tweet": "@user this is the tweet which i want to preprocess ! #machinelearning #prediction"
    }

    response = requests.post(url, headers=headers, json=data)
    print(response.json())
    ```
    

    """

    # Convert input into a DataFrame
    list_text = [preprocessingFeatures.tweet]

    # Load model from MLflow
    logged_model = 'runs:/89b183556cf34460858d94125f8df98d/text_preprocessor'
    loaded_model = mlflow.pyfunc.load_model(logged_model)

    df = pd.DataFrame(list_text,columns=['tweet'])

    # Perform prediction
    preprocessed_result = loaded_model.predict(pd.DataFrame(df))

    # Format and return the response
    return preprocessed_result
