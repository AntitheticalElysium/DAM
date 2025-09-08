import streamlit as st
import joblib

# Page configuration
st.set_page_config(
    page_title="🏡 House Price Predictor",
    page_icon="🏠",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Sidebar for user inputs
st.sidebar.header("Enter House Details")
size = st.sidebar.slider("Size of the house (sq ft)", 100, 10000, 1500)
bedrooms = st.sidebar.slider("Number of bedrooms", 1, 10, 3)
garden = st.sidebar.selectbox("Does the house have a garden?", ("Yes", "No"))

# Title and description
st.title("🏡 House Price Prediction App")
st.markdown("""
Predict the **price of a house** based on its size, number of bedrooms, and whether it has a garden.
Use the sidebar to input the house features.
""")

# Load model
model = joblib.load("regression.joblib")

if st.button("Predict Price"):
    garden_binary = 1 if garden == "Yes" else 0
    prediction = model.predict([[size, bedrooms, garden_binary]])
    st.success(f"The predicted price of the house is: **${prediction[0]:,.0f}**")

st.markdown("---")
st.markdown("Made with ❤️ using Streamlit")

