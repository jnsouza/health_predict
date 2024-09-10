import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import requests

# URL da API do backend
# taxiFareApiUrl = 'https://taxifare.lewagon.ai/predict'
api_url = "http://localhost:8501/predict"
# Configuração da página e título
st.set_page_config(
    page_title="Well-Being Calculator",
    page_icon="🏃‍♀️❤️"
)

st.markdown("""
    <h1 style='text-align: center; color: black;'>
    Well-being Calculator 🩺
    </h1>
""", unsafe_allow_html=True)

# Informação sobre a aplicação
st.info("This application is designed to assess your well-being using machine learning algorithms. If you have concerns about your health, please consult a healthcare professional.")

# Sidebar para input dos dados
with st.sidebar:
    st.header("Patient data")

    # Idade e mapeamento
    age = st.slider("Age", 0, 100, 30)
    def map_age_to_category(age):
        if 18 <= age <= 24: return 1
        elif 25 <= age <= 29: return 2
        elif 30 <= age <= 34: return 3
        elif 35 <= age <= 39: return 4
        elif 40 <= age <= 44: return 5
        elif 45 <= age <= 49: return 6
        elif 50 <= age <= 54: return 7
        elif 55 <= age <= 59: return 8
        elif 60 <= age <= 64: return 9
        elif 65 <= age <= 69: return 10
        elif 70 <= age <= 74: return 11
        elif 75 <= age <= 79: return 12
        elif age >= 80: return 13
        else: return 14
    age_category_value = map_age_to_category(age)

    # Peso e altura
    weight = st.number_input("Weight (kg)", 30, 200, 70)
    height = st.number_input("Height (cm)", 100, 250, 170)

    # Seleção de sexo
    sex = st.selectbox("Sex", ["Male", "Female"])
    sex_var = 1 if sex == "Male" else 2

    # Categoria de BMI
    bmi_category = st.select_slider("BMI Category",
                                options=["Underweight", "Normal Weight", "Overweight", "Obese"])
    bmi_map = {"Underweight": 1750, "Normal Weight": 2250, "Overweight": 2750, "Obese": 3500}
    bmi_value = bmi_map[bmi_category]

    # Nível de atividade física
    _pacat3 = st.selectbox("Physical Activity Level", ["Highly Active", "Active", "Insufficiently Active", "Inactive", "Don't Know"])
    pacat3_map = {"Highly Active": 1, "Active": 2, "Insufficiently Active": 3, "Inactive": 4, "Don't Know": 9}
    _pacat3_value = pacat3_map[_pacat3]

    # Tipo de atividade física
    exract22 = st.selectbox("Type of physical activity", ["Walking", "Running or jogging", "Gardening or yard work", "Bicycling", "Aerobics", "Calisthenics", "Elliptical machine", "Household activities", "Weight lifting", "Yoga/Pilates", "Other"])
    exract22_activity_map = {"Walking": 1, "Running or jogging": 2, "Gardening or yard work": 3, "Bicycling": 4, "Aerobics": 5, "Calisthenics": 6, "Elliptical machine": 7, "Household activities": 8, "Weight lifting": 9, "Yoga/Pilates": 10, "Other": 11}
    exract22_value = exract22_activity_map[exract22]


    # Frequência de atividade de força por semana
    strfreq = st.slider("Strength activity frequency (days/week)", 0, 7, 0)
    strfreq_value = strfreq * 100 if strfreq > 0 else 0

    # Minutos totais de atividade física por semana
    pa3min = st.slider("Total minutes of physical activity per week", 0, 1000, 180)

    # Saúde física e mental
    physhlth = st.slider("Days not feeling well physically (past 30 days)", 0, 30, 0)
    menthlth = st.slider("Days not feeling well mentally (past 30 days)", 0, 30, 0)

    # Doenças e condições
    depressive_disorder = st.selectbox("Ever told you had a depressive disorder?", ["Yes", "No"])
    depressive_disorder = 1 if depressive_disorder == "Yes" else 2

    cvdstrk3 = st.selectbox("Have you ever been diagnosed with a stroke?", ["No", "Yes"])
    cvdstrk3 = 2 if cvdstrk3 == "No" else 1

    rfhype6 = st.selectbox("Do you have high blood pressure?", ["No", "Yes"])
    rfhype6 = 2 if rfhype6 == "No" else 1

    rf_chol3 = st.selectbox("Do you have high cholesterol?", ["No", "Yes"])
    rf_chol3 = 2 if rf_chol3 == "No" else 1

    d_michd = st.selectbox("Have you been diagnosed with coronary heart disease?", ["Yes", "No"])
    d_michd = 1 if d_michd == "Yes" else 2

    drdxar2 = st.selectbox("Have you been diagnosed with arthritis?", ["Yes", "No"])
    drdxar2 = 1 if drdxar2 == "Yes" else 2

    diabete4 = st.selectbox("Have you been told you had diabetes?", ["Yes", "No", "Pre-diabetes/borderline", "Don't know/Not sure"])
    diabete4_map = {"Yes": 1, "No": 3, "Pre-diabetes/borderline": 4, "Don't know/Not sure": 7}
    diabete4_value = diabete4_map[diabete4]

    # Variáveis hardcoded
    educag_value = 4.0
    incomg1_value = 5.0
    ltahth1 = 1.0
    checkup1 = 1.0
    exanery2 = 1.0
    cvdinft4 = 1.0
    cvdcrhd4 = 2.0
    cvdstrk3 = 2.0
    chcocnc1 = 2.0
    chccopd3 = 2.0
    chckdny2 = 2.0
    decide = 2.0
    phys14d = 0
    ment14d = 0
    actin13 = 1
    paindx3 = 1
    maxvo21 = 2395
    exerhmm1 = 129.52
    exract12 = exract22_value
    diffalon = 2

    if st.button("🧮 Calculate Well-Being"):
            # Dicionário de inputs para o backend
        input_data = {
        "age_category": age_category_value,
        "weight": weight,
        "height": height,
        "sex": sex_var,
        "bmi_value": bmi_value,
        "physical_activity_level": _pacat3_value,
        "physhlth": physhlth,
        "menthlth": menthlth,
        "depressive_disorder": depressive_disorder,
        "rfhype6": rfhype6,
        "rf_chol3": rf_chol3,
        "d_michd": d_michd,
        "exract22": exract22_value,
        "strfreq": strfreq_value,
        "pa3min": pa3min,
        "ltahth1": ltahth1,
        "checkup1": checkup1,
        "exanery2": exanery2,
        "cvdinft4": cvdinft4,
        "cvdcrhd4": cvdcrhd4,
        "decide": decide,
        "phys14d": phys14d,
        "ment14d": ment14d,
        "actin13": actin13,
        "paindx3": paindx3,
        "maxvo21": maxvo21,
        "exerhmm1": exerhmm1,
        "exract12": exract12,
        "diffalon": diffalon
    }
        print(input_data)
        print("AQUI ESTÁ O QUE VAI PRO BACK!!!!!!!")

        # Fazendo o post para o backend/Sending request to the API
        response = requests.post(api_url, params=input_data)
        print(response.text, "retornou do backend")

        # # # Verificar se o request foi bem-sucedido
        # if response.status_code == 200:
        #     prediction = response.json().get('prediction')

        #     st.balloons()  # Trigger balloon animation
        #     st.markdown(f'<h2 style="color:green; animation: fadeIn 2s ease-in;">💸 ${prediction:.2f}</h2>', unsafe_allow_html=True)
        # else:
        #     st.error(f"Error: {response.status_code}")



    # score = response
    # print(score)
    # print("ISSO ESTÁ RETORNANDO DO BACK!!!!!!!!!!!!!!!!")
    st.markdown("<br><br>", unsafe_allow_html=True)
# Exibir o resultado na página principal
st.subheader("Well-Being Score and Analysis")
st.write("Your Well-Being Score will be displayed here after you calculate.")

# Adicionando mais detalhes
st.write(f"""
Prediction done
**Well-Being Score:** 20%

**Confidence in the well-being assessment:** 90.2 %

**BMI level:** Normal Weight
""")

fig = go.Figure(go.Indicator(
    mode="gauge+number",
    value=2,
    title={'text': "Well-Being Score"},
    gauge={'axis': {'range': [1, 3]},
           'bar': {'color': "green"},
           'steps': [
               {'range': [0, 1], 'color': "lightgreen"},
               {'range': [1, 2.0], 'color': "orange"},
               {'range': [2.0, 3], 'color': "red"}]}
))
st.plotly_chart(fig)
