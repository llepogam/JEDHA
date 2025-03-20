import streamlit as st
import pandas as pd
import plotly.express as px 
import plotly.graph_objects as go
import numpy as np
import requests
from datetime import datetime
import time
import os
import boto3


### Config
st.set_page_config(
    page_title="Offensive Speech Recognition",
    page_icon="⚠️",
    layout="wide"
)



# Initialize AWS session with credentials from Hugging Face secrets
session = boto3.Session(
    aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
)

# Initialize S3 resource
s3 = session.resource("s3")
bucket_name = 'llepogam-app-history'
bucket = s3.Bucket(bucket_name)


# File path for history
HISTORY_FILE = "https://llepogam-app-history.s3.eu-north-1.amazonaws.com/history.csv"

   

def save_history():
    """Save history to S3"""
    try:
        history_df = pd.DataFrame(st.session_state.history)
        # Save to temporary file first
        history_df.to_csv("/tmp/temp_history.csv", index=False)
        # Upload to S3
        bucket.upload_file("/tmp/temp_history.csv", "history.csv")
        # Clean up temp file
        os.remove("/tmp/temp_history.csv")
    except Exception as e:
        st.error(f"Error saving history to S3: {str(e)}")

def load_history():
    """Load history from S3"""
    try:
        # Download from S3 to temporary file
        bucket.download_file("history.csv", "/tmp/temp_history.csv")
        # Read the CSV
        history_df = pd.read_csv("/tmp/temp_history.csv")
        # Clean up temp file
        os.remove("/tmp/temp_history.csv")
        return history_df.to_dict('records')
    except Exception as e:
        st.error(f"Error loading history from S3: {str(e)}")
        return []
    
if 'history' not in st.session_state:
    st.session_state.history = load_history()

# Custom CSS
st.markdown("""
    <style>
    .prediction-box {
        padding: 20px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .high-severity {
        background-color: rgba(255, 0, 0, 0.1);
        border: 1px solid red;
    }
    .medium-severity {
        background-color: rgba(255, 165, 0, 0.1);
        border: 1px solid orange;
    }
    .low-severity {
        background-color: rgba(0, 255, 0, 0.1);
        border: 1px solid green;
    }
    </style>
""", unsafe_allow_html=True)


def hate_speech_detection(text):
    """Make API call with error handling"""
    url = "https://llepogam-hate-speech-detection-api.hf.space/predict"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(
            url, 
            headers=headers, 
            json={"Text": text},
            timeout=200
        )
        response.raise_for_status()
        return response.json(), None
    except requests.exceptions.Timeout:
        return None, "API request timed out. Please try again."
    except requests.exceptions.RequestException as e:
        return None, f"API error: {str(e)}"
    except Exception as e:
        return None, f"Unexpected error: {str(e)}"

def get_severity_class(probability):
    """Determine severity class based on probability"""
    if probability > 0.7:
        return "high-severity"
    elif probability > 0.4:
        return "medium-severity"
    return "low-severity"

# Header Section
st.title("🚫 Offensive Speech Detection")
st.markdown("""
This application helps identify potentially offensive content in text provided by an user. 

It uses a trained neural network to analyze text and determine if it contains offensive speech. 


**How it works:**
1. Enter your text in the input box below
2. The model will analyze the content and provide a prediction based on the model
3. Results show both the classification and value predicted by the model
4. The results is saved in the prediction history
""")


# FAQ Section
with st.expander("❓ Frequently Asked Questions"):
    st.markdown("""
    **Q: What is considered offensive speech?**
    - A: The model is using a dataset of tweets, which were tagged as offensive or not. More information on the dataset can be found here : https://huggingface.co/datasets/christophsonntag/OLID

    **Q: What type of model it is?**
    - A: It is a neural network with an initial preprocessing, a vectorization, an embedding layers and GRU layers 
                
    **Q: How is the prediction done?**
    - A: The model predicts a value between 1 and 0. The closer it is to 1, the more offensive is the prediction.  When the prediction is higher than 0.5, the text is considered as offensive

    **Q: How accurate is the detection?**
    - A: The model created has an accuracy of 73.1%, which means than prediction are correct almost 3 times out of four. When the targeted values is below 0.3 or higher than 0.7, it means than there is a high level of confidence in the prediction 

    """)


# Clear button - must come BEFORE the text_area widget
if st.button("Clear Input", key="clear_button"):
    st.session_state.user_input = ""

# Text Input Section
max_chars = 500 
user_input = st.text_area(
    "Enter text to analyze:",
    height=100,
    key="user_input",
    help="Enter the text you want to analyze for offensive content. Maximum 500 characters.",
    max_chars=max_chars
)

# Character counter
chars_remaining = max_chars - len(user_input)
st.caption(f"Characters remaining: {chars_remaining}")



# Process input
if user_input:
    if len(user_input.strip()) == 0:
        st.warning("Please enter some text to analyze.")
    else:
        with st.spinner("Analyzing text..."):
            result, error = hate_speech_detection(user_input)
            
            if error:
                st.error(f"Error: {error}")
            else:
                # Format probability as percentage
                probability = result['probability']
                
                # Create prediction box with appropriate severity class
                severity_class = get_severity_class(result['probability'])
                
                if result['prediction'] == 'offensive':
                    final_prediction = "Offensive"
                else : 
                    final_prediction = "Not Offensive"

                st.markdown(f"""
                <div class="prediction-box {severity_class}">
                    <h3>Analysis Results</h3>
                    <p><strong>Prediction:</strong> {final_prediction}</p>
                    <p><strong>Prediction Value:</strong> {probability:.2f}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Confidence meter using Plotly
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = probability,
                    title = {'text': "Confidence Level"},
                    number = {'valueformat': '.2f'}, 
                    gauge = {
                        'axis': {'range': [0, 1]},
                        'bar': {'color': "darkblue"},
                        'steps': [
                            {'range': [0, 0.3], 'color': "lightgreen"},
                            {'range': [0.3, 0.7], 'color': "orange"},
                            {'range': [0.7, 1], 'color': "red"}
                        ]
                    }
                ))
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True)
                
                # Add to history
                st.session_state.history.append({
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'text': user_input,
                    'prediction': final_prediction,
                    'prediction_value': probability
                })
                save_history()

# History Section
if st.session_state.history:
    with st.expander("📜 Analysis History"):
        history_df = pd.DataFrame(st.session_state.history)
        history_df_output = (history_df
                     .sort_values('timestamp', ascending=False)
                     .head(20))
        st.dataframe(
            history_df_output,
            column_config={
                "timestamp": "Time",
                "text": "Input Text",
                "prediction": "Prediction",
                "prediction_value": st.column_config.NumberColumn(
                    "Prediction Value",
                    format="%.2f"
                )
            },
            hide_index=True
        )
        


# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center'>
        <p>Developed with ❤️ by Louis Le Pogam</p>
    </div>
""", unsafe_allow_html=True)

