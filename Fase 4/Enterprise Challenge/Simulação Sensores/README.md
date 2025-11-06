
# Projeto: Simulação de Sensores com ESP32 (Temperatura, Vibração, Distância)

Este projeto simula a coleta de dados de sensores com ESP32 em ambiente simulado. Em vez de dados reais, usamos dados gerados e analisados em R.

## Sensores Simulados

1. **Temperatura** (°C)
   - Normal: até 60°C
   - Alerta: > 60°C
   - Crítico: ≥ 90°C → Desligamento simulado
  
![Monitoramento-Temperatura](https://github.com/Nico-Araujo/FIAP/blob/6d472ea93e4c65fce0d1a852d377f8287661a488/Fase%204/Enterprise%20Challenge/Simula%C3%A7%C3%A3o%20Sensores/Monitoramento%20de%20Temperatura_page-0001.jpg)


2. **Vibração** (g)
   - Normal: até 1.0g
   - Alerta: > 1.0g
   - Crítico: ≥ 2.0g → Parada simulada
   
![Monitoramento-Vibracao](https://github.com/Nico-Araujo/FIAP/blob/cf53b3774a0481db5b02a0bad4d02b080e5bb78a/Fase%204/Enterprise%20Challenge/Simula%C3%A7%C3%A3o%20Sensores/Monitoramento%20de%20Vibra%C3%A7%C3%A3o_page-0001.jpg)


3. **Distância (HC-SR04)** (cm)
   - Normal: 10 cm a 200 cm
   - Crítico:
     - < 5 cm → Obstrução; > 250 cm → Peça ausente
   
![Monitoramento-Distancia](https://github.com/Nico-Araujo/FIAP/blob/5b5ec4f7d4b1d047b4172266f1ef579758151ca5/Fase%204/Enterprise%20Challenge/Simula%C3%A7%C3%A3o%20Sensores/Monitoramento%20de%20Dist%C3%A2ncia_page-0001.jpg)


## Conteúdo

- `dados_sensores_simulados.csv`: dados simulados de 100 leituras.
- `simulacao_sensores.R`: script para gerar gráficos e análises em R.
- `README.md`: este documento.

## Como Rodar

1. Instale o R: https://cran.r-project.org
2. Instale o pacote `ggplot2`:
   ```r
   install.packages("ggplot2")
   ```
3. Execute o script:
   ```r
   source("simulacao_sensores.R")
   ```

Você verá três gráficos:
- Temperatura x Tempo (com alertas)
- Vibração x Tempo (com alertas)
- Distância x Tempo (com zonas críticas)
