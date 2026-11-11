import streamlit as st
import pandas as pd
import joblib
import gdown
import os

# ---------------- PAGE CONFIGURATION ----------------

st.set_page_config(
    page_title="CyberShield | Network Security",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>

.stApp {
    background-color: #080F1E;
    color: #E5EAF5;
}

[data-testid="stSidebar"] {
    background-color: #101A2D;
    border-right: 1px solid #243550;
}

h1, h2, h3 {
    color: #F1F5FF;
}

p {
    color: #AAB8D0;
}

.hero {
    background: linear-gradient(120deg, #142B4D, #10213A, #123C54);
    padding: 35px;
    border-radius: 18px;
    border: 1px solid #245477;
    margin-bottom: 25px;
}

.hero h1 {
    font-size: 38px;
    margin-bottom: 10px;
}

.hero p {
    font-size: 16px;
    color: #B9D3E8;
}

.card {
    background-color: #111E33;
    padding: 22px;
    border-radius: 15px;
    border: 1px solid #263D5B;
    margin-bottom: 15px;
}

.card h3 {
    color: #39C6F4;
}

.small-text {
    color: #91A5C4;
    font-size: 14px;
}

div.stButton > button {
    background-color: #087EA4;
    color: white;
    border-radius: 9px;
    border: none;
    padding: 10px 22px;
    font-weight: bold;
}

div.stButton > button:hover {
    background-color: #09A6D5;
    color: white;
}

div[data-testid="stMetric"] {
    background-color: #111E33;
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #263D5B;
}

hr {
    border-color: #263D5B;
}

</style>
""", unsafe_allow_html=True)


# ---------------- MODEL LOADING ----------------

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

    return joblib.load(MODEL_PATH)


try:
    artifacts = load_model()

    model = artifacts["model"]
    encoder = artifacts["encoder"]
    scaler = artifacts["scaler"]
    feature_cols = artifacts["feature_cols"]
    cat_cols = artifacts["cat_cols"]

    model_loaded = True

except Exception as e:
    model_loaded = False
    st.error(f"Model loading failed: {e}")
    st.stop()


# ---------------- SIDEBAR ----------------

st.sidebar.markdown("# 🛡️ CyberShield")
st.sidebar.caption("NETWORK SECURITY INTELLIGENCE")

st.sidebar.divider()

page = st.sidebar.radio(
    "NAVIGATION",
    [
        "🏠 Overview",
        "🔍 Detection Centre",
        "📊 Analytics",
        "🧠 Model Information",
        "ℹ️ About Project"
    ]
)

st.sidebar.divider()

st.sidebar.markdown("### SYSTEM STATUS")

st.sidebar.success("● Model Online")

st.sidebar.markdown(
    "<p class='small-text'>Powered by Machine Learning<br>"
    "Random Forest Classifier</p>",
    unsafe_allow_html=True
)

st.sidebar.markdown("---")
st.sidebar.caption("CyberShield | 2026")


# ---------------- OVERVIEW ----------------

if page == "🏠 Overview":

    st.markdown("""
    <div class="hero">
        <h1>🛡️ CyberShield</h1>
        <h3>Intelligent Network Attack Detection System</h3>
        <p>
        Monitor network traffic, identify suspicious patterns,
        and classify potential cyber threats using Machine Learning.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.success("System is operational. Random Forest model loaded successfully.")

    st.markdown("## Platform Overview")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("ML Algorithm", "Random Forest")

    with col2:
        st.metric("Input Features", "42")

    with col3:
        st.metric("Attack Categories", "10")

    st.markdown("---")

    st.markdown("## What can CyberShield do?")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="card">
            <h3>🔍 Network Traffic Analysis</h3>
            <p>Upload network traffic datasets in CSV format
            for automated analysis.</p>
        </div>

        <div class="card">
            <h3>🧠 Machine Learning Detection</h3>
            <p>Use a trained Random Forest classifier to
            categorize network traffic.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card">
            <h3>📊 Interactive Analytics</h3>
            <p>Explore prediction summaries and visual
            representations of detected categories.</p>
        </div>

        <div class="card">
            <h3>📥 Export Results</h3>
            <p>Download prediction results as a CSV file
            for further analysis.</p>
        </div>
        """, unsafe_allow_html=True)

    st.info("Navigate to Detection Centre to start analysing network traffic.")


# ---------------- DETECTION CENTRE ----------------

elif page == "🔍 Detection Centre":

    st.title("🔍 Network Detection Centre")

    st.write(
        "Upload your network traffic CSV file to identify "
        "potential attack categories."
    )

    st.divider()

    uploaded_file = st.file_uploader(
        "Choose a network traffic CSV file",
        type=["csv"]
    )

    if uploaded_file is not None:

        try:
            data = pd.read_csv(uploaded_file)

            st.markdown("### Uploaded Dataset")

            col1, col2 = st.columns(2)

            col1.metric("Total Records", len(data))
            col2.metric("Available Columns", len(data.columns))

            st.dataframe(
                data.head(10),
                use_container_width=True
            )

            missing_cols = [
                col for col in feature_cols
                if col not in data.columns
            ]

            if missing_cols:

                st.error(
                    f"Missing required columns: {missing_cols}"
                )

            else:

                st.info(
                    "Dataset validation successful. "
                    "Ready to perform prediction."
                )

                if st.button("🚀 Analyse Network Traffic"):

                    with st.spinner("Analysing network traffic..."):

                        X = data[feature_cols].copy()

                        X[cat_cols] = encoder.transform(
                            X[cat_cols]
                        )

                        X_scaled = scaler.transform(X)

                        predictions = model.predict(X_scaled)

                        results = data.copy()

                        results["Predicted Attack"] = predictions

                        st.session_state["results"] = results

                        st.session_state["predictions"] = predictions

                    st.success("Analysis completed successfully!")

        except Exception as e:

            st.error(f"Prediction failed: {e}")

    if "results" in st.session_state:

        results = st.session_state["results"]

        st.markdown("---")
        st.markdown("## Prediction Results")

        counts = results["Predicted Attack"].value_counts()

        col1, col2 = st.columns(2)

        col1.metric("Records Analysed", len(results))

        normal_count = counts.get("Normal", 0)

        col2.metric(
            "Non-Normal Predictions",
            len(results) - normal_count
        )

        st.dataframe(
            results,
            use_container_width=True
        )

        csv = results.to_csv(index=False).encode("utf-8")

        st.download_button(
            "⬇️ Download Prediction Report",
            data=csv,
            file_name="network_attack_predictions.csv",
            mime="text/csv"
        )


# ---------------- ANALYTICS ----------------

elif page == "📊 Analytics":

    st.title("📊 Network Traffic Analytics")

    st.write(
        "Visualise the distribution of predicted network traffic categories."
    )

    if "results" not in st.session_state:

        st.info(
            "No prediction data available yet. "
            "Visit Detection Centre and analyse a CSV file first."
        )

    else:

        results = st.session_state["results"]

        counts = results["Predicted Attack"].value_counts()

        col1, col2, col3 = st.columns(3)

        col1.metric("Total Records", len(results))

        col2.metric("Categories Found", len(counts))

        col3.metric(
            "Most Common Category",
            counts.idxmax()
        )

        st.markdown("---")

        st.subheader("Prediction Distribution")

        st.bar_chart(counts)

        st.subheader("Category-wise Summary")

        summary = pd.DataFrame({
            "Attack Category": counts.index,
            "Number of Records": counts.values,
            "Percentage": (
                counts.values / len(results) * 100
            ).round(2)
        })

        st.dataframe(
            summary,
            use_container_width=True
        )


# ---------------- MODEL INFORMATION ----------------

elif page == "🧠 Model Information":

    st.title("🧠 Model Information")

    st.write(
        "Learn about the machine learning model powering CyberShield."
    )

    st.markdown("""
    <div class="card">
        <h3>Random Forest Classifier</h3>
        <p>
        Random Forest is a supervised machine learning algorithm
        that combines multiple decision trees to make predictions.
        It is used in this project to classify network traffic
        into different categories.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Model Specifications")

    details = {
        "Algorithm": "Random Forest Classifier",
        "Number of Estimators": "100",
        "Input Features": "42",
        "Target Variable": "attack_cat",
        "Dataset": "UNSW-NB15",
        "Classification Type": "Multiclass Classification"
    }

    for key, value in details.items():

        st.markdown(
            f"**{key}:** {value}"
        )

    st.markdown("---")

    st.subheader("Detection Workflow")

    steps = [
        "1. Upload network traffic dataset.",
        "2. Validate required input features.",
        "3. Encode categorical features.",
        "4. Scale numerical features.",
        "5. Apply Random Forest classification.",
        "6. Display and download prediction results."
    ]

    for step in steps:
        st.write("➜", step)


# ---------------- ABOUT PROJECT ----------------

elif page == "ℹ️ About Project":

    st.title("ℹ️ About CyberShield")

    st.markdown("""
    <div class="card">
        <h3>Project Overview</h3>
        <p>
        CyberShield is a machine learning-based Network Attack
        Detection System developed to analyse network traffic
        and classify potential cyber threats.
        </p>
        <p>
        The project uses the UNSW-NB15 dataset and a trained
        Random Forest classifier to identify different
        categories of network activity.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Technologies Used")

    technologies = [
        "Python",
        "Pandas and NumPy",
        "Scikit-learn",
        "Random Forest",
        "Streamlit",
        "Google Colab",
        "GitHub"
    ]

    for tech in technologies:
        st.write("•", tech)

    st.markdown("---")

    st.caption(
        "CyberShield | Machine Learning Based Network Attack Detection"
    )
