import streamlit as st
import pandas as pd
# from api.predict import make_prediction

# Título do app
st.title('Previsão de Saúde')

# Coletar dados do usuário
st.header("Insira seus dados:")
htm4 = st.number_input("Altura (HTM4)")
wtkg3 = st.number_input("Peso (WTKG3)")
physhlth = st.number_input("Dias com problemas de saúde física (PHYSHLTH)")
menthlth = st.number_input("Dias com problemas de saúde mental (MENTHLTH)")
age = st.slider("Idade (AGEG5YR)", 1, 14, step=1)  # Exemplo de seleção para uma coluna categórica

# Botão para fazer a previsão
if st.button("Prever"):
    input_data = {
        "HTM4": [htm4],
        "WTKG3": [wtkg3],
        "PHYSHLTH": [physhlth],
        "MENTHLTH": [menthlth],
        "AGEG5YR": [age]
    }

    # Converte os dados para DataFrame
    input_df = pd.DataFrame(input_data)

    # Chama a função de previsão
    # prediction = make_prediction(input_df)

    # Mostra o resultado
    # st.write(f"O resultado previsto é: {prediction}")
