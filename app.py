import streamlit as st
import pickle
import numpy as np

# Load the trained model
with open('model.pkl', 'rb') as file:
    model = pickle.load(file)

st.title('Loan Eligibility Prediction')

# Input fields
gender = st.selectbox('Gender', ['Male', 'Female'])
married = st.selectbox('Married', ['Yes', 'No'])
dependents = st.selectbox('Dependents', ['0', '1', '2', '3+'])
education = st.selectbox('Education', ['Graduate', 'Not Graduate'])
self_employed = st.selectbox('Self Employed', ['Yes', 'No'])
applicant_income = st.number_input('Applicant Income', min_value=150)
coapplicant_income = st.number_input('Coapplicant Income', min_value=0)
loan_amount = st.number_input('Loan Amount', min_value=9)
loan_amount_term = st.number_input('Loan Amount Term', min_value=12)
credit_history = st.selectbox('Credit History', ['1', '0'])
property_area = st.selectbox('Property Area', ['Urban', 'Semi-Urban', 'Rural'])

# Preprocess inputs as needed for the model
if st.button('Predict'):
    # Mapping inputs to numeric for the model
    gender_map = {'Male': 1, 'Female': 0}
    married_map = {'Yes': 1, 'No': 0}
    dependents_map = {'0': 0, '1': 1, '2': 2, '3+': 4}
    education_map = {'Graduate': 1, 'Not Graduate': 0}
    self_employed_map = {'Yes': 1, 'No': 0}
    property_area_map = {'Urban': 2, 'Semi-Urban': 1, 'Rural': 0}
    
    # Prepare the input data for the model
    input_data = np.array([
        gender_map[gender],
        married_map[married],
        dependents_map[dependents],
        education_map[education],
        self_employed_map[self_employed],
        applicant_income,
        coapplicant_income,
        loan_amount,
        loan_amount_term,
        int(credit_history),
        property_area_map[property_area]
    ]).reshape(1, -1)

    # Custom rule for income to loan amount ratio check
    if applicant_income >= loan_amount or coapplicant_income >= loan_amount:
        st.success('The applicant is likely to get a loan based on income vs loan amount.')
    else: 
        # Predict loan eligibility using the model
        prediction = model.predict(input_data)

        if prediction == 1:
            st.success('The applicant is likely to get a loan.')
        else:
            st.error('The applicant is unlikely to get a loan.')
