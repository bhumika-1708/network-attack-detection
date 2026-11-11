import streamlit as st
import joblib
import numpy as np
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Network Attack Detection",
    page_icon="🛡️",
    layout="wide"
)

# Main heading
st.title("🛡️ Network Attack Detection System")

st.markdown("""
### Machine Learning Based Network Security

This application uses a trained Random Forest
classifier to identify potentially malicious
network traffic.
""")

st.divider()

st.subheader("About the Project")

st.write("""
Our system uses Machine Learning techniques
to analyse network traffic and detect potential
cyber attacks.
""")

st.info("The prediction interface is currently under development.")
