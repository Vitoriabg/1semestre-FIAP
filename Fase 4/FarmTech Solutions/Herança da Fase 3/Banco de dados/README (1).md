# 🌱 Sistema de Banco de Dados para Máquina Agrícola

Projeto FIAP que simula um sistema inteligente de irrigação usando sensores agrícolas, banco de dados em SQLite, visualização de dados com **Streamlit** e integração com a **API do OpenWeather**.

---

## 📁 Estrutura do Projeto

```bash
maquina-agricola-bd/
│
├── banco_dados_agricola.py       # Banco de dados SQLite com operações CRUD
├── painel_visualizacao.py        # Painel interativo com gráficos e filtros
├── integracao_clima.py           # API climática com OpenWeather integrada
├── dados_sensores.csv            # Dados exportados automaticamente
└── README.md                     # Documentação do projeto
```

---

## ⚙️ Operações Realizadas no banco_dados_agricola.py

- `criar_tabelas()`: Criação da tabela `leituras_sensores`
- `inserir_leitura()`: Insere uma nova leitura
- `obter_todas_leituras()` e `obter_leitura_por_id()`: Consultas
- `atualizar_leitura()`: Atualização parcial
- `deletar_leitura()`: Remoção de registros
- `exportar_para_csv()`: Exporta os dados para CSV
- `importar_do_serial()`: Importa dados simulados do monitor serial

---

## 🧬 MER — Modelo Entidade-Relacionamento

### Tabela: `leituras_sensores`

| Campo         | Tipo     | Descrição                         |
|---------------|----------|-----------------------------------|
| id            | INTEGER  | Chave primária (PK)               |
| data_hora     | TEXT     | Data/hora da leitura              |
| umidade       | REAL     | Valor do sensor DHT22             |
| ph            | REAL     | Valor do sensor LDR (pH)          |
| fosforo       | INTEGER  | Nível simulado (0-100)            |
| potassio      | INTEGER  | Nível simulado (0-100)            |
| status_bomba  | INTEGER  | 0 = Desligada / 1 = Ligada        |
| observacoes   | TEXT     | Informações extras                |

---

## 📊 Painel de Visualização (Streamlit)

Execute o seguinte comando:

```bash
streamlit run painel_visualizacao.py
```

Funcionalidades:
- Filtros por data
- Gráficos de umidade, pH, fósforo e potássio
- Status da bomba ao longo do tempo
- Tabela de dados brutos

---

## ☁️ Integração com API OpenWeather

No arquivo `integracao_clima.py`, já está configurada sua **API KEY: `7aff6a9802e63fd6dc7d0091391f0195`**

Com isso, o sistema:
- Obtém **umidade, temperatura e condição do clima atual**
- Analisa a **previsão das próximas 24 horas**
- **Decide automaticamente** se a bomba deve ser ativada
- Insere essa decisão no banco com observações

### Rodar a integração:

```bash
python integracao_clima.py
```

---

## 📦 Como Usar (Simulação completa)

1. Execute `banco_dados_agricola.py` para gerar dados simulados (ou coletar do ESP32 via serial).
2. Execute `integracao_clima.py` para aplicar a lógica com dados reais de clima.
3. Visualize todos os dados no painel rodando `painel_visualizacao.py`.
4. Consulte o arquivo `dados_sensores.csv` com os dados exportados.

---

## 🧠 Justificativa Técnica

- **MER simples e funcional** com foco em tempo-real e decisão automática.
- **CRUD completo** permite testar inserção, visualização e manutenção de dados.
- **Streamlit** oferece uma interface amigável para leigos.
- **API pública** dá inteligência ao sistema com base em clima real.

