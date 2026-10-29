

import streamlit as st
import pandas as pd
import joblib
from datetime import date

st.title("Medical Insurance Cost Prediction")
st.write("Enter your details to predict insurance charges.")

# Check whether the model loads
try:
    model = joblib.load("insurance_model.pkl")
    st.success("Model loaded successfully!")
except Exception as e:
    st.error(f"Model loading error: {e}")
    st.stop()

st.write("Model is ready. Now enter your details below.")



today = date.today()

# Latest date of birth allowed: 18 years ago
max_dob = date(
    today.year - 18,
    today.month,
    today.day
)

# Earliest date of birth allowed: 100 years ago
min_dob = date(
    today.year - 100,
    today.month,
    today.day
)

dob = st.date_input(
    "Select your Date of Birth",
    value=date(today.year - 30, today.month, today.day),
    min_value=min_dob,
    max_value=max_dob
)

age = today.year - dob.year - (
    (today.month, today.day) < (dob.month, dob.day)
)

st.write(f"Your age: {age} years")

sex = st.selectbox("Sex", ["female", "male"])
bmi_text = st.text_input("Enter BMI", value="25.0")

try:
    bmi = float(bmi_text)

    if not 10 <= bmi <= 60:
        st.warning("Please enter a BMI between 10 and 60.")
        st.stop()

except ValueError:
    st.warning("Please enter a valid number for BMI.")
    st.stop()
children = st.selectbox("Number of Children", [0, 1, 2, 3, 4, 5])
smoker = st.selectbox("Smoker", ["no", "yes"])
region = st.selectbox(
    "Region",
    ["northeast", "northwest", "southeast", "southwest"]
)

if st.button("Predict Insurance Charges"):
    input_data = pd.DataFrame([{
        "age": age,
        "bmi": bmi,
        "children": children,
        "sex_male": 1 if sex == "male" else 0,
        "smoker_yes": 1 if smoker == "yes" else 0,
        "region_northwest": 1 if region == "northwest" else 0,
        "region_southeast": 1 if region == "southeast" else 0,
        "region_southwest": 1 if region == "southwest" else 0
    }])

    try:
        prediction = model.predict(input_data)[0]
        st.success(f"Predicted Insurance Charges: {prediction:,.2f}")
    except Exception as e:
        st.error(f"Prediction error: {e}")
