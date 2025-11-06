# 🌾 Projeto FarmTech Solutions - Banco de Dados

## 🎯 Objetivo
Desenvolver um sistema de banco de dados para guardar informações de sensores usados na plantação (umidade, pH, nutrientes), ações do sistema (como aplicar água e fertilizantes) e dados das plantações.

---

##  Informações Relevantes

### Primeira etapa - Qual foi a quantidade total de água aplicada em cada mês?
- Data e hora da aplicação
- Quantidade de água aplicada
- Plantação onde foi aplicada

### Segunda etapa - Como variou o nível de pH do solo ao longo do ano?
- Data e hora da leitura
- Valor do pH
- Sensor responsável pela leitura
- Plantação monitorada

### Terceira etapa - Quais nutrientes (fósforo e potássio) estão em falta?
- Data e hora da leitura
- Valor de fósforo (P) e potássio (K)
- Sensor que fez a leitura
- Plantação monitorada

### Quarta etapa - Informações dos sensores
- Tipo de sensor (umidade, pH, nutrientes)
- Localização do sensor
- Status (ativo/inativo)

### Quinta etapa - Ações automáticas do sistema
- Data e hora da ação
- Tipo de ação (aplicar água, aplicar fertilizante)
- Quantidade aplicada
- Plantação relacionada

---

## Entidades e Atributos

### Entidade: Sensor
- id_sensor (int, PK)
- tipo_sensor (varchar)
- localizacao (varchar)
- status (varchar)

### Entidade: Plantacao
- id_plantacao (int, PK)
- nome_cultura (varchar)
- localizacao (varchar)
- data_inicio (date)
- data_fim (date, opcional)

### Entidade: Leitura
- id_leitura (int, PK)
- id_sensor (int, FK)
- data_hora (timestamp)
- valor_umidade (double, opcional)
- valor_ph (double, opcional)
- valor_nutriente_P (double, opcional)
- valor_nutriente_K (double, opcional)

### Entidade: Ajuste
- id_ajuste (int, PK)
- id_plantacao (int, FK)
- data_hora_ajuste (timestamp)
- quantidade_agua (double)
- quantidade_fertilizante (double)
- descricao_ajuste (varchar)

### Entidade: Leitura_Plantacao (tabela de ligação)
- id_leitura (int, FK)
- id_plantacao (int, FK)

---

## Cardinalidade

### Sensor 🔁 Leitura
- Um sensor pode ter várias leituras (1:N)

### Plantacao 🔁 Leitura
- Uma plantação pode ter várias leituras
- Uma leitura pode servir a várias plantações
- Relacionamento N:N, resolvido com a tabela "Leitura_Plantacao"

### Plantacao 🔁 Ajuste
- Uma plantação pode ter vários ajustes (1:N)


