import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
import datetime
import numpy as np
from banco_dados_agricola import BancoDadosAgricola

# Configuração da página
st.set_page_config(
    page_title="Painel de Monitoramento Agrícola",
    page_icon="🌱",
    layout="wide"
)

# Título do dashboard
st.title("🌱 Painel de Monitoramento Agrícola")
st.markdown("Visualização dos dados coletados pelos sensores da máquina agrícola")

# Função para carregar os dados do banco
@st.cache_data(ttl=60)  # Cache por 60 segundos
def carregar_dados():
    with BancoDadosAgricola() as bd:
        dados = bd.obter_todas_leituras()
    
    if not dados:
        return pd.DataFrame()
    
    df = pd.DataFrame(dados)
    # Converter timestamp para datetime
    df['data_hora'] = pd.to_datetime(df['data_hora'])
    return df

# Carregar os dados
df = carregar_dados()

if df.empty:
    st.warning("Não há dados disponíveis no banco. Execute o script banco_dados_agricola.py para gerar dados de exemplo.")
    st.stop()

# Sidebar para filtros
st.sidebar.header("Filtros")

# Filtro de data
data_min = df['data_hora'].min().date()
data_max = df['data_hora'].max().date()

data_inicial = st.sidebar.date_input(
    "Data inicial",
    data_min,
    min_value=data_min,
    max_value=data_max
)

data_final = st.sidebar.date_input(
    "Data final",
    data_max,
    min_value=data_inicial,
    max_value=data_max
)

# Filtrar dados por data
df_filtrado = df[
    (df['data_hora'].dt.date >= data_inicial) & 
    (df['data_hora'].dt.date <= data_final)
]

# Botão para atualizar os dados
if st.sidebar.button("Atualizar Dados"):
    df = carregar_dados()
    st.experimental_rerun()

# Métricas principais
st.subheader("Métricas Atuais")
col1, col2, col3, col4 = st.columns(4)

# Últimas leituras
if not df_filtrado.empty:
    ultima_leitura = df_filtrado.iloc[-1]
    
    col1.metric(
        "Umidade", 
        f"{ultima_leitura['umidade']:.1f}%",
        f"{ultima_leitura['umidade'] - df_filtrado.iloc[-2]['umidade']:.1f}%" if len(df_filtrado) > 1 else None
    )
    
    col2.metric(
        "pH", 
        f"{ultima_leitura['ph']:.1f}",
        f"{ultima_leitura['ph'] - df_filtrado.iloc[-2]['ph']:.1f}" if len(df_filtrado) > 1 else None
    )
    
    col3.metric(
        "Fósforo (P)", 
        f"{ultima_leitura['fosforo']}",
        f"{ultima_leitura['fosforo'] - df_filtrado.iloc[-2]['fosforo']}" if len(df_filtrado) > 1 else None
    )
    
    col4.metric(
        "Potássio (K)", 
        f"{ultima_leitura['potassio']}",
        f"{ultima_leitura['potassio'] - df_filtrado.iloc[-2]['potassio']}" if len(df_filtrado) > 1 else None
    )

# Gráfico de linha: Umidade e Status da Bomba ao longo do tempo
st.subheader("Umidade e Status da Bomba ao Longo do Tempo")

fig, ax1 = plt.subplots(figsize=(12, 6))

# Eixo para umidade
ax1.set_xlabel('Data/Hora')
ax1.set_ylabel('Umidade (%)', color='tab:blue')
ax1.plot(df_filtrado['data_hora'], df_filtrado['umidade'], 'b-', label='Umidade')
ax1.tick_params(axis='y', labelcolor='tab:blue')

# Eixo secundário para status da bomba
ax2 = ax1.twinx()
ax2.set_ylabel('Status da Bomba', color='tab:red')
ax2.plot(df_filtrado['data_hora'], df_filtrado['status_bomba'], 'r-', label='Status da Bomba')
ax2.tick_params(axis='y', labelcolor='tab:red')
ax2.set_yticks([0, 1])
ax2.set_yticklabels(['Desligada', 'Ligada'])

fig.tight_layout()
plt.title('Umidade e Status da Bomba')
plt.grid(True, alpha=0.3)

# Adicionar legenda
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

st.pyplot(fig)

# Gráfico de barras: Níveis de pH, Fósforo e Potássio
st.subheader("Níveis de pH, Fósforo e Potássio")

# Agrupar por dia para simplificar o gráfico
df_diario = df_filtrado.copy()
df_diario['data'] = df_diario['data_hora'].dt.date
media_diaria = df_diario.groupby('data').mean().reset_index()

fig, ax = plt.subplots(figsize=(12, 6))

x = np.arange(len(media_diaria))
largura = 0.25

# Barras para pH (escala diferente)
ax1 = ax
ax1.set_xlabel('Data')
ax1.set_ylabel('pH', color='tab:blue')
barras1 = ax1.bar(x - largura, media_diaria['ph'], largura, label='pH', color='tab:blue')
ax1.tick_params(axis='y', labelcolor='tab:blue')
ax1.set_ylim(0, 10)  # pH normalmente vai de 0 a 14, mas ajustamos para melhor visualização

# Eixo secundário para P e K
ax2 = ax1.twinx()
ax2.set_ylabel('Níveis (P e K)', color='tab:red')
barras2 = ax2.bar(x, media_diaria['fosforo'], largura, label='Fósforo (P)', color='tab:green')
barras3 = ax2.bar(x + largura, media_diaria['potassio'], largura, label='Potássio (K)', color='tab:orange')
ax2.tick_params(axis='y', labelcolor='tab:red')

# Configurar eixo x
ax1.set_xticks(x)
ax1.set_xticklabels([d.strftime('%d/%m') for d in media_diaria['data']], rotation=45)

# Adicionar legenda
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

plt.title('Níveis Médios Diários de pH, Fósforo e Potássio')
plt.grid(True, alpha=0.3)
fig.tight_layout()

st.pyplot(fig)

# Tabela de dados
st.subheader("Dados Brutos")
st.dataframe(df_filtrado.sort_values('data_hora', ascending=False))

# Informações adicionais
st.markdown("---")
st.markdown("""
### Informações sobre os Sensores
- **Sensor de Umidade**: DHT22 (Faixa: 0-100%)
- **Sensor de pH**: LDR analógico (Faixa: 0-14)
- **Sensor de Fósforo (P)**: Botão físico (Valores: 0-100)
- **Sensor de Potássio (K)**: Botão físico (Valores: 0-100)
- **Controle de Irrigação**: Relé + LED (Status: 0=Desligado, 1=Ligado)
""")

# Rodapé
st.markdown("---")
st.markdown("Painel desenvolvido com Streamlit para monitoramento de máquina agrícola")