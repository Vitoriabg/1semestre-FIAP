
# Projeto de Simulação de Sensores (ESP32) em R

# Instale o pacote ggplot2 se necessário:
# install.packages("ggplot2")


library(ggplot2)

# Leitura do arquivo CSV que está na mesma pasta do script
dados <- read.csv("dados_sensores_simulados.csv")

# Gráfico de Temperatura
ggplot(dados, aes(x = tempo, y = temperatura)) +
  geom_line(color = "blue") +
  geom_hline(yintercept = 60, color = "orange", linetype = "dashed") +
  geom_hline(yintercept = 90, color = "red", linetype = "dashed") +
  labs(title = "Monitoramento de Temperatura",
       x = "Tempo", y = "Temperatura (°C)") +
  theme_minimal()

# Gráfico de Vibração
ggplot(dados, aes(x = tempo, y = vibracao)) +
  geom_line(color = "darkgreen") +
  geom_hline(yintercept = 1.0, color = "orange", linetype = "dashed") +
  geom_hline(yintercept = 2.0, color = "red", linetype = "dashed") +
  labs(title = "Monitoramento de Vibração",
       x = "Tempo", y = "Vibração (g)") +
  theme_minimal()

# Gráfico de Distância
ggplot(dados, aes(x = tempo, y = distancia)) +
  geom_line(color = "purple") +
  geom_hline(yintercept = 5, color = "red", linetype = "dotted") +
  geom_hline(yintercept = 250, color = "orange", linetype = "dashed") +
  labs(title = "Monitoramento de Distância com HC-SR04",
       x = "Tempo", y = "Distância (cm)") +
  theme_minimal()
