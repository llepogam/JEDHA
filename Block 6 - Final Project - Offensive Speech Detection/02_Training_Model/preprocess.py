import mlflow
import spacy
import pandas as pd
from spacy.lang.en.stop_words import STOP_WORDS
from mlflow.models.signature import ModelSignature
from mlflow.types.schema import Schema, ColSpec
from mlflow.pyfunc import PythonModel, PythonModelContext
import re


class TextPreprocessor(PythonModel):
    def __init__(self, spacy_model="en_core_web_sm", additional_stop_words=None):
        """Initialize the text preprocessor with configurable parameters."""
        self.spacy_model = spacy_model
        self.additional_stop_words = additional_stop_words or ["user", "url"]
        
    def load_context(self, context: PythonModelContext):
        """Load the spacy model when the MLflow model is loaded."""
        self.nlp = spacy.load(self.spacy_model)
        
        # Add additional stop words
        for word in self.additional_stop_words:
            self.nlp.Defaults.stop_words.add(word)
    

    def preprocess_text(self, text):
        """Preprocess a single text string."""
        # Clean special characters
        text_clean = ''.join(ch for ch in text if ch.isalnum() or ch==" ")
        
        # Normalize spacing and case
        text_clean = re.sub(r'\s+', ' ', text_clean).lower().strip()
        
        # Lemmatization and stop word removal
        doc = self.nlp(text_clean)
        text_clean = " ".join([token.lemma_ for token in doc 
                            if not token.is_stop]).strip()
        
        return text_clean
        
    def predict(self, context, model_input):
        """MLflow PythonModel required predict method."""
        if isinstance(model_input, pd.DataFrame):
            df = model_input.copy()
            text_column = "tweet"  # or get this from context
            df["text_clean"] = df[text_column].apply(self.preprocess_text)
            return df
        else:
            raise TypeError("Input must be a pandas DataFrame")

def save_preprocessor_to_mlflow():
    # Set MLflow tracking URI if needed
    # mlflow.set_tracking_uri("your_mlflow_server_uri")
    
    # Create or set the experiment
    mlflow.set_experiment("text_preprocessing")
    
    # Start an MLflow run
    with mlflow.start_run() as run:
        # Initialize preprocessor
        preprocessor = TextPreprocessor()
        
        # Log parameters
        mlflow.log_params({
            "spacy_model": preprocessor.spacy_model,
            "additional_stop_words": preprocessor.additional_stop_words
        })
        
        # Define model signature
        input_schema = Schema([
            ColSpec("string", "tweet")
        ])
        output_schema = Schema([
            ColSpec("string", "tweet"),
            ColSpec("string", "text_clean")
        ])
        signature = ModelSignature(inputs=input_schema, outputs=output_schema)
        
        # Log the model
        mlflow.pyfunc.log_model(
            artifact_path="text_preprocessor",
            python_model=preprocessor,
            signature=signature,
            input_example=pd.DataFrame({"tweet": ["This is a sample tweet! #AI @user"]}),
            registered_model_name="text_preprocessor"
        )
        
        print(f"Model saved with run ID: {run.info.run_id}")
        return run.info.run_id

if __name__ == "__main__":
    run_id = save_preprocessor_to_mlflow()