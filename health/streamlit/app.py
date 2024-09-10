import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import requests

input_data = {}

# URL da API do backend
# taxiFareApiUrl = 'https://taxifare.lewagon.ai/predict'
api_url = "http://localhost:8000/predict"
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
well_being_score = None
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
    bmi_map = {"Underweight": 1, "Normal Weight": 2, "Overweight": 3, "Obese": 4}
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

    educag_value = st.selectbox( "Level of Education Completed",
    options=[1, 2, 3, 4],  # Mapeando os valores corretos
    format_func=lambda x: {
        1: "Did not graduate High School",
        2: "Graduated High School",
        3: "Attended College or Technical School",
        4: "Graduated from College or Technical School",
    }[x])

    incomg1_value = st.selectbox( "Income Categories",
    options=[1, 2, 3, 4, 5, 6, 7, 9],  # Mapeando os valores corretos
    format_func=lambda x: {
        1: "Less than $15,000",
        2: "$15,000 to < $25,000",
        3: "$25,000 to < $35,000",
        4: "$35,000 to < $50,000",
        5: "$50,000 to < $100,000",
        6: "$100,000 to < $200,000",
        7: "$200,000 or more",
        9: "Don't know/Not sure/Missing"
    }[x])

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
    phys14d = 1
    ment14d = 1
    actin13 = 1
    paindx3 = 1
    maxvo21 = 2395
    exerhmm1 = 129.52
    exract12 = exract22_value
    diffalon = 2

    if st.button("🧮 Calculate Well-Being"):
        input_data = {
        "_AGEG5YR": age_category_value,  # Mapeando a idade para a categoria correta
        "WTKG3": weight,  # Peso
        "HTM4": height,  # Altura
        "SEXVAR": sex_var,  # Sexo
        "_BMI5CAT": bmi_value,  # Valor de BMI (Índice de Massa Corporal)
        "_PACAT3": _pacat3_value,  # Nível de atividade física
        "PHYSHLTH": physhlth,  # Saúde física (dias sem se sentir bem)
        "MENTHLTH": menthlth,  # Saúde mental (dias sem se sentir bem)
        "ADDEPEV3": depressive_disorder,  # Depressão
        "_RFHYPE6": rfhype6,  # Pressão alta
        "_RFCHOL3": rf_chol3,  # Colesterol alto
        "_MICHD": d_michd,  # Doença cardíaca
        "EXRACT22": exract22_value,  # Tipo de atividade física
        "STRFREQ_": strfreq_value,  # Frequência de atividade de força
        "PA3MIN_": pa3min,  # Minutos totais de atividade física por semana
        "_LTASTH1": ltahth1,  # Asma
        "CHECKUP1": checkup1,  # Exames médicos
        "EXERANY2": exanery2,  # Alguma atividade física
        "CVDINFR4": cvdinft4,  # Infarto
        "CVDCRHD4": cvdcrhd4,  # Doença cardíaca crônica
        "DECIDE": decide,  # Dificuldade em tomar decisões
        "_PHYS14D": phys14d,  # Dias de má saúde física
        "_MENT14D": ment14d,  # Dias de má saúde mental
        "ACTIN13_": actin13,  # Atividade moderada
        "_PAINDX3": paindx3,  # Índice de atividade física
        "MAXVO21_": maxvo21,  # Máximo VO2
        "EXERHMM1": exerhmm1,  # Minutos de exercício
        "EXRACT12": exract12,  # Segunda atividade física
        "DIFFALON": diffalon,  # Dificuldade para fazer atividades sozinho
        "_EDUCAG": educag_value,  # Nível de educação
        "_INCOMG1": incomg1_value, # Nível de renda
        "_DRDXAR2": drdxar2,
        'CVDSTRK3': cvdstrk3,  # AVC
        'CHCOCNC1': chcocnc1,  # Câncer
        'CHCCOPD3': chccopd3,  # Doença pulmonar
        'CHCKDNY2': chckdny2,  # Doença renal
        'DIABETE4': diabete4_value  # Diabetes
    }

        try:
            response = requests.post(api_url, json=input_data)  # Aqui você usa json=input_data

            if response.status_code == 200:
                prediction = response.json()

                st.success(f"Prediction: {prediction['result']}")
                well_being_score = prediction['result']
                # st.write(f"Prediction Probability: {prediction['probability']}")
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"Failed to connect to the API. Error: {str(e)}")

    st.markdown("<br><br>", unsafe_allow_html=True)

# Se a predição ainda não foi feita, mostre uma mensagem genérica
if well_being_score is None:
    st.subheader("Score and Analysis")
    st.write("Your Well-Being Score will be displayed here after you calculate.")
else:
    # Exibir o gráfico com o score após a predição
    fig = go.Figure(go.Indicator(
    mode="gauge+number",
    value=well_being_score,  # Esse é o valor que será atualizado dinamicamente
    title={'text': "Well-Being Score"},
    gauge={
        'axis': {'range': [0, 3], 'visible': True},  # Alterando o range para 0-3
        'bar': {'color': "rgba(128, 128, 128, 0.6)"}, # Cor com opacidade
        'bgcolor': "white",  # Remova o fundo colorido
        'borderwidth': 0,  # Sem borda
        'steps': [
            {'range': [0, 1], 'color': "lightgreen"},  # Excelente/Muito Bom
            {'range': [1, 2], 'color': "orange"},  # Bom
            {'range': [2, 3], 'color': "red"}  # Razoável/Péssimo
        ],
        'threshold': {
            'line': {'color': "black", 'width': 4},  # Linha preta indicando o valor
            'thickness': 0.75,
            'value': well_being_score
        }
    }
))
    st.plotly_chart(fig)
    st.markdown("""
        ### Well-Being Score Ranges:
        - **0 - 1**: Excellent/Very Good
        - **1 - 2**: Good
        - **2 - 3**: Fair/Poor
        """)
