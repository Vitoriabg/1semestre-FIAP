
import streamlit as st
import pandas as pd
import sqlite3
from banco_dados_agricola import BancoDadosAgricola
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

st.set_page_config(page_title="Sistema de Irrigação Inteligente", layout="wide")
st.title("🌿 Sistema de Irrigação Inteligente com Machine Learning")

# Conectar ao banco
bd = BancoDadosAgricola()
conn = sqlite3.connect(bd.nome_bd)
df = pd.read_sql_query("SELECT * FROM leituras_sensores", conn)

menu = st.sidebar.selectbox("📋 Menu", ["Visualizar Dados", "Gráficos", "Previsão com ML", "Sobre o Projeto"])

if menu == "Visualizar Dados":
    st.subheader("📄 Tabela de Leituras dos Sensores")
    st.dataframe(df.sort_values("data_hora", ascending=False), use_container_width=True)

elif menu == "Gráficos":
    st.subheader("📈 Visualização de Dados")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Umidade do Solo**")
        st.line_chart(df[['data_hora', 'umidade']].set_index("data_hora"))
    with col2:
        st.markdown("**pH do Solo**")
        st.line_chart(df[['data_hora', 'ph']].set_index("data_hora"))
    col3, col4 = st.columns(2)
    with col3:
        st.bar_chart(df["fosforo"])
    with col4:
        st.bar_chart(df["potassio"])

elif menu == "Previsão com ML":
    st.subheader("🤖 Previsão de Necessidade de Irrigação")
    if 'status_bomba' in df.columns:
        X = df[['umidade', 'ph', 'fosforo', 'potassio']]
        y = df['status_bomba']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        modelo = RandomForestClassifier()
        modelo.fit(X_train, y_train)
        acuracia = modelo.score(X_test, y_test)
        st.success(f"Acurácia do modelo: {acuracia:.2%}")

        st.markdown("### Simular Previsão")
        umidade = st.slider("Umidade (%)", 0, 100, 40)
        ph = st.slider("pH", 4.0, 8.0, 6.5)
        fosforo = st.selectbox("Fósforo presente?", [0, 1])
        potassio = st.selectbox("Potássio presente?", [0, 1])

        previsao = modelo.predict([[umidade, ph, fosforo, potassio]])[0]
        if previsao == 1:
            st.warning("⚠️ É recomendada irrigação.")
        else:
            st.success("✅ Não é necessária irrigação agora.")

elif menu == "Sobre o Projeto":
    st.markdown("""
    ### 💡 Sobre o Sistema
    Este sistema de irrigação inteligente:
    - Coleta dados de sensores (umidade, pH, fósforo, potássio);
    - Armazena tudo em um banco SQLite local;
    - Usa Machine Learning (Random Forest) para prever a necessidade de irrigação;
    - Permite visualização interativa com Streamlit.

    Desenvolvido como uma solução educacional e prática com foco em automação agrícola inteligente.
    """)

