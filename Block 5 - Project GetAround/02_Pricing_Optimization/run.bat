@echo off

:: Run the Docker command
docker run -it ^
    -v "%cd%:/home/app" ^
    -e AWS_ACCESS_KEY_ID=%AWS_ACCESS_KEY_ID% ^
    -e AWS_SECRET_ACCESS_KEY=%AWS_SECRET_ACCESS_KEY% ^
    -e BACKEND_STORE_URI=%BACKEND_STORE_URI% ^
    -e ARTIFACT_ROOT=%ARTIFACT_ROOT% ^
    -e MLFLOW_TRACKING_URI=%MLFLOW_TRACKING_URI% ^
    -e PORT=%PORT% ^
    getaround-pricing_image python train.py 