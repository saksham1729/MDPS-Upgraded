### ✅ Complete Updated Code (Ready to Run)

import pickle
import streamlit as st
import pandas as pd
import joblib

import streamlit as st
import joblib



try:
    drug_model = joblib.load("drugc_model.pkl")
except Exception as e:
    st.error(f"❌ Failed to load model: {e}")

st.stop()



# Load models
diabetes_model = pickle.load(open('diabetes_model.sav', 'rb'))
heart_disease_model = pickle.load(open('heart_disease_model.sav', 'rb'))
parkinsons_model = pickle.load(open('parkinsons_model.sav', 'rb'))
fever_model = pickle.load(open('fever_medication_rf_model(1).pkl', 'rb'))


# Initialize session states
for var in ['page', 'gender', 'age', 'disease', 'mode']:
    if var not in st.session_state:
        st.session_state[var] = ''

# Page 1: Gender
if st.session_state.page == '' or st.session_state.page == 'gender':
    st.title("👤 Welcome to Disease Detection")
    st.session_state.gender = st.radio("Select your gender:", ["Male", "Female", "Other"])
    if st.button("Next"):
        st.session_state.page = 'age'
        st.rerun()

# Page 2: Age
elif st.session_state.page == 'age':
    st.title("🔢 Enter Your Age")
    st.session_state.age = st.slider("Select your age:", 1, 120, 30)
    if st.button("Next"):
        st.session_state.page = 'mode_selection'
        st.rerun()

# Page 3: Mode Selection
elif st.session_state.page == 'mode_selection':
    st.title("🧠 Choose Prediction Mode")
    st.session_state.mode = st.radio("Select prediction type:", ["Advanced", "Normal"])
    if st.button("Continue"):
        st.session_state.page = 'predict_selector'
        st.rerun()

# Page 4: Route to appropriate mode
elif st.session_state.page == 'predict_selector':
    if st.session_state.mode == "Advanced":
        st.session_state.page = 'select_disease'
    else:
        st.session_state.page = 'normal_choice'
    st.rerun()

# Page 5: Advanced - Select Disease
elif st.session_state.page == 'select_disease':
    st.title("🧪 Select Disease Type")
    st.session_state.disease = st.selectbox("Choose one:", ["Diabetes", "Heart Disease", "Parkinson's"])
    if st.button("Continue"):
        st.session_state.page = 'predict'
        st.rerun()

# Page 6: Advanced Prediction Logic
elif st.session_state.page == 'predict':
    st.title(f"{st.session_state.disease} Prediction")
    st.caption(f"Gender: {st.session_state.gender} | Age: {st.session_state.age}")

    if st.session_state.disease == "Diabetes":
        col1, col2, col3 = st.columns(3)
        Pregnancies = col1.number_input('Number of Pregnancies', min_value=0) if st.session_state.gender == "Female" else 0
        Glucose = col2.number_input('Glucose Level', min_value=0)
        BloodPressure = col3.number_input('Blood Pressure', min_value=0)
        SkinThickness = col1.number_input('Skin Thickness', min_value=0)
        Insulin = col2.number_input('Insulin Level', min_value=0)
        BMI = col3.number_input('BMI', min_value=0.0)
        DPF = col1.number_input('Diabetes Pedigree Function', min_value=0.0)

        if st.button("Get Diabetes Result"):
            prediction = diabetes_model.predict([[Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DPF, st.session_state.age]])
            result = "🚨 Diabetic" if prediction[0] == 1 else "✅ Not Diabetic"
            st.success(result)

    elif st.session_state.disease == "Heart Disease":
        col1, col2, col3 = st.columns(3)
        gender_map = {"Male": 1, "Female": 0, "Other": 0}
        sex = gender_map.get(st.session_state.gender, 0)
        cp = col3.selectbox("Chest Pain Type", [0, 1, 2, 3])
        trestbps = col1.number_input("Resting BP", min_value=0)
        chol = col2.number_input("Cholesterol", min_value=0)
        fbs = col3.selectbox("Fasting Blood Sugar >120", [0, 1])
        restecg = col1.selectbox("Resting ECG", [0, 1, 2])
        thalach = col2.number_input("Max Heart Rate", min_value=0)
        exang = col3.selectbox("Exercise Induced Angina", [0, 1])
        oldpeak = col1.number_input("ST depression", min_value=0.0)
        slope = col2.selectbox("Slope", [0, 1, 2])
        ca = col3.selectbox("Major Vessels Colored", [0, 1, 2, 3])
        thal = col1.selectbox("Thalassemia", [0, 1, 2])

        if st.button("Get Heart Disease Result"):
            prediction = heart_disease_model.predict([[st.session_state.age, sex, cp, trestbps, chol, fbs,restecg, thalach, exang, oldpeak, slope, ca, thal]])
            result = "🚨 Has Heart Disease" if prediction[0] == 1 else "✅ No Heart Disease"
            st.success(result)

    elif st.session_state.disease == "Parkinson's":
        st.caption("Enter extracted voice metrics 👇")
        inputs = [st.number_input(label) for label in [
            'MDVP:Fo(Hz)', 'MDVP:Fhi(Hz)', 'MDVP:Flo(Hz)', 'MDVP:Jitter(%)', 'MDVP:Jitter(Abs)', 'MDVP:RAP', 'MDVP:PPQ',
            'Jitter:DDP', 'MDVP:Shimmer', 'MDVP:Shimmer(dB)', 'Shimmer:APQ3', 'Shimmer:APQ5', 'MDVP:APQ', 'Shimmer:DDA',
            'NHR', 'HNR', 'RPDE', 'DFA', 'Spread1', 'Spread2', 'D2', 'PPE'
        ]]
        if st.button("Get Parkinson’s Result"):
            prediction = parkinsons_model.predict([inputs])
            result = "🚨 Has Parkinson’s Disease" if prediction[0] == 1 else "✅ No Parkinson’s Disease"
            st.success(result)

# Page 7: Normal Choice Routing
elif st.session_state.page == "normal_choice":
    st.title("🩺 Normal Disease Assistant")
    st.caption(f"Gender: {st.session_state.gender} | Age: {st.session_state.age}")
    choice = st.radio("Choose a tool:", ["Fever Prediction", "Drug Help"])
    if st.button("Continue"):
        st.session_state.page = "fever_prediction" if choice == "Fever Prediction" else "drug_help"
        st.rerun()

# Page 8: Fever Prediction
elif st.session_state.page == "fever_prediction":
    st.title("🌡️ Fever Medication Recommendation")


    # Inputs
    Temperature = st.slider("Body Temperature (°C)", 35.0, 42.0, 37.0)
    Fever_Severity = st.selectbox("Fever Severity", ["Normal", "Mild Fever", "High Fever"])
    BMI = st.slider("Body Mass Index", 18.0, 35.0, 22.0)
    Headache = st.radio("Do you have a headache?", ["Yes", "No"])
    Body_Ache = st.radio("Do you have body aches?", ["Yes", "No"])
    Fatigue = st.radio("Are you feeling fatigued?", ["Yes", "No"])
    Chronic_Conditions = st.radio("Any chronic conditions?", ["Yes", "No"])
    Allergies = st.radio("Any medication allergies?", ["Yes", "No"])
    Smoking_History = st.radio("Smoking history?", ["Yes", "No"])
    Alcohol_Consumption = st.radio("Alcohol consumption?", ["Yes", "No"])
    Humidity = st.slider("Current Humidity (%)", 30, 90, 60)
    AQI = st.slider("Air Quality Index", 0, 500, 100)
    Physical_Activity = st.selectbox("Daily Physical Activity Level", ["Sedentary", "Moderate", "Active"])
    Diet_Type = st.selectbox("Diet Type", ["Vegetarian", "Non-Vegetarian", "Vegan"])
    Heart_Rate = st.slider("Resting Heart Rate (bpm)", 60, 120, 75)
    Blood_Pressure = st.selectbox("Blood Pressure Level", ["Normal", "High", "Low"])
    Previous_Medication = st.selectbox("Previously Taken Medication", ["Paracetamol", "Ibuprofen", "Aspirin", "None"])

    # Prediction
    if st.button("🧪 Get Medication"):
        input_df = pd.DataFrame([{
            "Temperature": Temperature,
            "Fever_Severity": Fever_Severity,
            "Age": st.session_state.age,
            "Gender": st.session_state.gender,
            "BMI": BMI,
            "Headache": Headache,
            "Body_Ache": Body_Ache,
            "Fatigue": Fatigue,
            "Chronic_Conditions": Chronic_Conditions,
            "Allergies": Allergies,
            "Smoking_History": Smoking_History,
            "Alcohol_Consumption": Alcohol_Consumption,
            "Humidity": Humidity,
            "AQI": AQI,
            "Physical_Activity": Physical_Activity,
            "Diet_Type": Diet_Type,
            "Heart_Rate": Heart_Rate,
            "Blood_Pressure": Blood_Pressure,
            "Previous_Medication": Previous_Medication
        }])
        prediction = fever_model.predict(input_df)
        st.success(f"💊 Recommended Medication: **{prediction[0]}**")


elif st.session_state.page == "drug_help":
    st.title("💊 Drug Recommendation Help")


    # User inputs
    medical_condition = st.selectbox("Medical Condition", ["Acne", "Cancer", "Heart Disease", "Diabetes", "Fever"])
    rx_otc = st.selectbox("Prescription Type", ["Rx", "OTC", "Rx/OTC"])
    # 🧬 Show pregnancy_category only for Female
    if st.session_state.gender == "Female":
        pregnancy_category = st.selectbox("Pregnancy Category", ["A", "B", "C", "D", "X", "N"])
    else:
        pregnancy_category = "Not Applicable"
    
    csa = st.selectbox("CSA Schedule", ["N", "U", "M", "1", "2", "3", "4", "5"])
    alcohol = st.radio("Alcohol Interaction", ["X", "None"])
    rating = st.slider("Minimum Effectiveness Rating", 1, 10, 7)

    if st.button("Suggest Drug"):
        input_df = pd.DataFrame([{
            "medical_condition": medical_condition,
            "rx_otc": rx_otc,
            "pregnancy_category": pregnancy_category,
            "csa": csa,
            "alcohol": alcohol,
            "rating": rating
        }])
        input_df["activity"] = "Unknown"
        input_df["no_of_reviews"] = 0
        input_df["medical_condition_description"] = "Not provided"

        result = drug_model.predict(input_df)
        st.success(f"🌟 Suggested Drug: **{result[0]}**")
