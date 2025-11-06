
# Projeto de Irrigação Automatizada com ESP32

## Descrição do Projeto
Este projeto implementa um sistema de irrigação automatizado utilizando o microcontrolador ESP32, que monitora condições do solo e ativa uma bomba de água quando determinados critérios são atendidos.

## Componentes Principais
- ESP32: Microcontrolador principal
- Sensor DHT22: Mede umidade e temperatura do ar
- LDR (simulando sensor de pH): Simula a medição do pH do solo
- Botões (P e K): Simulam a detecção de fósforo e potássio no solo
- Relé: Controla a bomba de irrigação

## Lógica de Controle
O sistema toma decisões de irrigação baseado na seguinte lógica:

if (umidade < 50% && fósforo_presente && potássio_presente) {
    liga_bomba();
} else {
    desliga_bomba();
}

## Diagrama do Circuito
![Cap-1-Circuito](https://github.com/user-attachments/assets/b8f384e4-2354-415f-b865-7cb0ceba3ab8)

    ESP32 --> DHT22[Sensor DHT22]
    ESP32 --> LDR[LDR - Simulador de pH]
    ESP32 --> BotaoP[Botão Fósforo]
    ESP32 --> BotaoK[Botão Potássio]
    ESP32 --> Rele[Relé da Bomba]
    Rele --> Bomba[Bomba de Água]
    
## Funcionamento
O sistema monitora continuamente:
- Umidade do ar (via DHT22)
- Nível de pH simulado (via LDR)
- Presença de nutrientes (via botões)
- A cada 2 segundos, os dados são exibidos no Serial Monitor

A bomba é ativada quando:
- Umidade está abaixo de 50%
- Fósforo está presente (botão pressionado)
- Potássio está presente (botão pressionado)

## Instalação
1. Conecte os componentes conforme o diagrama
2. Carregue o código para o ESP32 usando Arduino IDE
3. Abra o Monitor Serial para visualizar as leituras
