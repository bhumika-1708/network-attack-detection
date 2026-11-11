import streamlit as st
import pandas as pd
import joblib
import gdown
import os

# Page configuration
st.set_page_config(
    page_title="Network Attack Detection",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ Network Attack Detection System")

st.markdown("""
### Machine Learning Based Network Security

Upload network traffic data and let our trained
Random Forest classifier identify potential attacks.
""")

st.divider()

# Model download and loading
MODEL_PATH = "rf_classifier.joblib"
FILE_ID = "1GGrw9k5lufchnAK5YHPPJJ71z8GL788T"

@st.cache_resource
def load_model():
    if not os.path.exists(MODEL_PATH):
        gdown.download(
            id=FILE_ID,
            output=MODEL_PATH,
            quiet=False
        )

    artifacts = joblib.load(MODEL_PATH)
    return artifacts

try:
    artifacts = load_model()

    model = artifacts["model"]
    encoder = artifacts["encoder"]
    scaler = artifacts["scaler"]
    feature_cols = artifacts["feature_cols"]
    cat_cols = artifacts["cat_cols"]

    st.success("Random Forest model loaded successfully!")

except Exception as e:
    st.error(f"Model loading failed: {e}")
    st.stop()

st.divider()

# CSV upload
st.subheader("📂 Upload Network Traffic Data")

uploaded_file = st.file_uploader(
    "Upload your CSV file",
    type=["csv"]
)

if uploaded_file is not None:

    data = pd.read_csv(uploaded_file)

    st.write("### Uploaded Data")
    st.dataframe(data.head())

    missing_cols = [
        col for col in feature_cols
        if col not in data.columns
    ]

    if missing_cols:
        st.error(f"Missing columns: {missing_cols}")

    else:

        if st.button("🔍 Predict Attack Category"):

            try:
                X = data[feature_cols].copy()

                # Convert categorical columns
                X[cat_cols] = encoder.transform(X[cat_cols])

                # Scale features
                X_scaled = scaler.transform(X)

                # Prediction
                predictions = model.predict(X_scaled)

                # Results
                results = data.copy()
                results["Predicted Attack"] = predictions

                st.success("Prediction completed!")

                st.subheader("📊 Prediction Results")
                st.dataframe(results)

                # Download results
                csv = results.to_csv(index=False).encode("utf-8")

                st.download_button(
                    label="⬇️ Download Results",
                    data=csv,
                    file_name="attack_predictions.csv",
                    mime="text/csv"
                )

            except Exception as e:
                st.error(f"Prediction failed: {e}")

st.divider()

st.caption("Network Attack Detection | Random Forest Classifier")
