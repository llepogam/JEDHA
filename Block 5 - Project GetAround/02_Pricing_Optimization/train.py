import pandas as pd
import numpy as np

import time

import mlflow
from mlflow.models.signature import infer_signature

import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import  OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import Ridge, Lasso, LinearRegression
from sklearn.model_selection import cross_val_score, GridSearchCV
from sklearn.metrics import r2_score, root_mean_squared_error

from catboost import CatBoostClassifier,CatBoostRegressor



#------------------ Let's build the function that will be used in the training------------------

def get_clean_dataset():
    # Read the dataset
    df = pd.read_csv('get_around_pricing_project.csv')
    df = df[df.columns[1:]]
    
    # Create mapping for model categories
    model_counts = df.groupby('model_key')['car_type'].count().reset_index()
    model_counts['model_key_category'] = model_counts['model_key']
    model_counts.loc[model_counts['car_type'] < 5, 'model_key_category'] = 'Others'
    
    # Create a dictionary for mapping
    category_mapping = dict(zip(model_counts['model_key'], model_counts['model_key_category']))
    
    # Add the new categorized column to the main dataframe
    df['model_key'] = df['model_key'].map(category_mapping)
    
    return df

def split_dataset(df,target_variable='rental_price_per_day'):
    features_list = list(df.columns[:-1])


    X = df.loc[:, features_list]
    Y = df.loc[:, target_variable]
       
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.2, random_state = 0)
    return X,Y,X_train, X_test, Y_train, Y_test


def get_preprocessor(X):

    numeric_features = []
    categorical_features = []
    for i,t in X.dtypes.items():
        if ('float' in str(t)) or ('int' in str(t)) :
            numeric_features.append(i)
        else :
            categorical_features.append(i)



    print('Found numeric features ', numeric_features)
    print('Found categorical features ', categorical_features)

        # Create pipeline for numeric features
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='mean')), # missing values will be replaced by columns' mean
        ('scaler', StandardScaler())

    ])

    # Create pipeline for categorical features
    categorical_transformer = Pipeline(
        steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')), # missing values will be replaced by most frequent value
        ('encoder', OneHotEncoder(drop='first')) # first column will be dropped to avoid creating correlations between features
        ])

    # Use ColumnTransformer to make a preprocessor object that describes all the treatments to be done
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
    ])

    return preprocessor


def build_model(preprocessor):
    
    catboost_params = {
    "iterations": 1000,
    "learning_rate": 0.03,
    "depth": 6,
    "loss_function": "RMSE",
    "random_seed": 42
    }
    
    model = Pipeline(
        steps=[
            ("Preprocessing", preprocessor),
            (
                "Regressor",
               CatBoostRegressor(**catboost_params, verbose=100),
            ),
        ],
        verbose=True,
    )
    
    
    return model, catboost_params




#------------------ Let's here write the flow of the MLFlow run------------------

if __name__ == "__main__":

    experiment_name = "getarround_pricing_prediction"
    mlflow.set_experiment(experiment_name)



    with mlflow.start_run():

        start_time = time.time()

        print("gettting dataset...")
        df = get_clean_dataset()
        print("... dataset ok")

        print("splitting dataset...")
        X,Y,X_train, X_test, Y_train, Y_test = split_dataset(df,'rental_price_per_day')
        print('...dataset split')

        print("...gettting preprocess")
        preprocessor = get_preprocessor(X)
        print("...preprocessor ok")

        print("building model..")
        model, catboost_params = build_model(preprocessor)
        print("...model built")

        model.fit(X_train, Y_train)
        # Make predictions
        y_pred = model.predict(X_test)
        predictions = model.predict(X_train)

        # Calculate metrics
        rmse = root_mean_squared_error(Y_test, y_pred)

        # Log metrics
        mlflow.log_metric("rmse", rmse)


        # Then modify the model logging:
        mlflow.sklearn.log_model(
            model,
            "pipeline_model",
            signature=infer_signature(X_train, predictions),
)
        mlflow.log_params(catboost_params)


        mlflow.log_metric("R2_train",  model.score(X_train, Y_train))
        mlflow.log_metric("R2_test", model.score(X_test, Y_test))  

        print("R2 score on training set : ", model.score(X_train, Y_train))
        print("R2 score on test set : ", model.score(X_test, Y_test))     



        print(f"---Total training time: {time.time()-start_time}")




    print("...Done!")