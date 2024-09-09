import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# titulo da pagina
st.set_page_config(
    page_title="Well-Being Calculator",
    page_icon="🏃‍♀️❤️"
)

st.markdown("""
    <h1 style='text-align: center; color: black;'>
    Well-being Calculator 🩺
    </h1>
""", unsafe_allow_html=True)

# Função dummy para previsão
def predict_wellbeing(inputs):
    prediction = np.random.rand()  # Previsão dummy
    return prediction
st.write("Welcome to the Well-being Calculator. Fill in the details on the sidebar to get your well-being score.")

import streamlit as st

st.info("This application is designed to assess your well-being using machine learning algorithms. If you have concerns about your health, please consult a healthcare professional.")
# st.markdown("""
# <div style='font-size:20px; color:#333; font-weight: bold;'>
# This application is designed to assess your well-being using machine learning algorithms. If you have concerns about your health, please consult a healthcare professional.
# </div>
# """, unsafe_allow_html=True)

# Sidebar para input dos dados e botão de cálculo
with st.sidebar:
    st.header("Patient data")

    # Idade
    age = st.slider("Age", 0, 100, 30)

    # Peso e altura
    weight = st.number_input("Weight (kg)", 30, 200, 70)
    height = st.number_input("Height (cm)", 100, 250, 170)

    # Seleção de sexo (SEXVAR)
    sex = st.selectbox("Sex", ["Male", "Female"])
    sex_var = 1 if sex == "Male" else 2

    # Nível de atividade física (_PACAT3)
    _pacat3 = st.selectbox("Physical Activity Level",
                           ["Highly Active", "Active", "Insufficiently Active", "Inactive", "Don't Know"])
    pacat3_map = {
        "Highly Active": 1,
        "Active": 2,
        "Insufficiently Active": 3,
        "Inactive": 4,
        "Don't Know": 9
    }
    _pacat3_value = pacat3_map[_pacat3]

    # Tipo de atividade física
    exract22 = st.selectbox(
        "What other type of physical activity gave you the next most exercise during the past month?",
        ["Walking", "Running or jogging", "Gardening or yard work", "Bicycling", "Aerobics",
         "Calisthenics", "Elliptical machine", "Household activities", "Weight lifting",
         "Yoga/Pilates", "Other"]
    )
    exract22_activity_map = {
        "Walking": 1, "Running or jogging": 2, "Gardening or yard work": 3,
        "Bicycling": 4, "Aerobics": 5, "Calisthenics": 6,
        "Elliptical machine": 7, "Household activities": 8,
        "Weight lifting": 9, "Yoga/Pilates": 10, "Other": 11
    }
    exract22 = exract22_activity_map[exract22]

    # Saúde física e mental
    physhlth = st.slider("Days not feeling well physically in the past 30 days)", 0, 30, 0)
    menthlth = st.slider("Days not feeling well mentally in the past 30 days)", 0, 30, 0)

    # Depressive disorder (1 = Yes, 2 = No)
    depressive_disorder = st.selectbox("Ever told you had a depressive disorder?", ["Yes", "No"])
    depressive_disorder = 1 if depressive_disorder == "Yes" else 2

    # Pressão alta (1 = Yes, 2 = No)
    rf_hype6 = st.selectbox("Do you have high blood pressure?", ["No", "Yes"])
    rf_hype6 = 2 if rf_hype6 == "No" else 1

    # Colesterol alto (1 = Yes, 2 = No)
    rf_chol3 = st.selectbox("Do you have high cholesterol?", ["No", "Yes"])
    rf_chol3 = 2 if rf_chol3 == "No" else 1

    # Doença cardíaca (1 = Yes, 2 = No)
    d_michd = st.selectbox("Have you been diagnosed with coronary heart disease?", ["Yes", "No"])
    d_michd = 1 if d_michd == "Yes" else 2

    # Botão para calcular o bem-estar
    if st.button("Calculate Well-Being"):
        # Inputs para o modelo (convertendo as seleções em valores numéricos)
        inputs = [age, weight, height, _pacat3, physhlth, menthlth,
                  rf_hype6, rf_chol3, d_michd, exract22, depressive_disorder]

        # Fazer a previsão do bem-estar
        # MANDA PRO BACK E PREVÊ - FAZENDO UM POST
        #MOCKSCORE
        score = 52

        # try:
        #     score = predict_wellbeing(inputs)
        # except:
        #     score = None


        # Exibir o resultado
        # st.sidebar.success(f"Well-Being Score: {score:.2f}")
        st.sidebar.success(f"Well-Being Score: {score:52}")
        # Criar um DataFrame para exibir os dados do paciente
        patient_data = pd.DataFrame({
            'Input': ['Age', 'Weight', 'Height', 'Sex', 'Physical Activity Level',
                      'Physical Health', 'Mental Health', 'Depressive Disorder',
                      'High Blood Pressure', 'High Cholesterol', 'Heart Disease'],
            'Value': [age, weight, height, sex_var, _pacat3_value, physhlth, menthlth,
                      depressive_disorder, rf_hype6, rf_chol3, d_michd]
        })

        # Exibir a tabela com os dados do paciente
        st.write("Patient Data Summary")
        st.table(patient_data)

# dicionario_retorno =  {1: 'Bem',
#         2: 'Mediana',
#         3: 'Ruim'}

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
    gauge={'axis': {'range': [1, 3]}}
))
st.plotly_chart(fig)
