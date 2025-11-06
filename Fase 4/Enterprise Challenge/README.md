# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">

# Enterprise Challenge - Sprint 2 - Reply

## 👨‍🎓 Integrantes: 
- <a href="https://www.linkedin.com/in/juliano-romeiro-rodrigues/">Juliano Romeiro Rodrigues</a>
- <a href="">Mariana Barbui dos Santos Zitelli</a>
- <a href="https://www.linkedin.com/in/nicolas--araujo/">Nicolas Antonio Silva Araujo</a> 
- <a href="https://www.linkedin.com/in/vitoria-bagatin-31ba88266/">Vitória Pereira Bagatin</a> 


## 📜 Descrição

Este projeto foi desenvolvido no contexto da metodologia PBL (Problem-Based Learning), visando criar um sistema de monitoramento industrial inteligente capaz de detectar condições anormais em máquinas e ambientes de produção. O objetivo principal é prevenir falhas, aumentar a segurança e otimizar a manutenção preditiva por meio da leitura em tempo real de três parâmetros críticos: temperatura, vibração e distância.
O sistema utiliza um microcontrolador ESP32, combinado com sensores de baixo custo, para fornecer alertas visuais e sonoros quando as condições operacionais ultrapassam limites pré-definidos. A solução é escalável e pode ser adaptada para diferentes cenários industriais, desde linhas de produção até equipamentos isolados


## 🔋 Componentes e Funcionalidades

Sensor de Temperatura (DS18B20)
- Monitora a temperatura em °C.
- Limites operacionais:
- Normal: 0°C a 60°C
- Alerta: >60°C (aciona LED amarelo)
- Crítico: >80°C (aciona LED vermelho + buzzer)
- Emergência: ≥90°C (desliga equipamento via relé)
- Motivo da escolha: Alta precisão (±0.5°C); Interface OneWire (fácil integração); À prova d'água (para ambientes industriais); Faixa ampla (-55°C a +125°C)

Sensor de Vibração (MPU6050)
- Mede aceleração em "g" (1g = 9.81 m/s²).
- Limites operacionais:
- Normal: 0.1g a 0.5g
- Alerta: >1.0g (indica desbalanceamento)
- Crítico: >2.0g (desliga máquina automaticamente)
- Motivo da escolha: Mede vibração em 3 eixos (dados em 'g'); Comunicação I2C padrão; Custo-benefício para monitoramento mecânico

Sensor de Distância (HC-SR04)
- Detecta obstáculos ou falhas em esteiras industriais (faixa: 2cm a 4m).
- Limites operacionais:
- Normal: 10cm a 200cm
- Alerta: <5cm (obstrução) ou >250cm (falta de peça)
- Motivo da escolha: Baixo consumo de energia; Imunidade a interferências luminosas; Custo acessível para aplicações industriais

Sistema de Alertas
- LED Verde: Condições normais.
  ![Teste-1-Normal.png](https://github.com/Nico-Araujo/FIAP/blob/7b90c023259156c022748d47bcb00d4fa08d29d1/Fase%204/Enterprise%20Challenge/Teste-1-Normal.png)
- LED Amarelo: Alerta (parâmetro fora da faixa ideal, mas não crítico).
  ![Teste-2-Alerta.png](https://github.com/Nico-Araujo/FIAP/blob/b8ae03a5cae66d37746eaffc43f392e569417d6a/Fase%204/Enterprise%20Challenge/Teste-2-Alerta.png)
- LED Vermelho + Buzzer (1000Hz): Emergência (ação imediata necessária).
  ![Teste-3-Critico.png](https://github.com/Nico-Araujo/FIAP/blob/0db3c5e7fa86e66ca519f7b2eac04c727f752b92/Fase%204/Enterprise%20Challenge/Teste-3-Critico.png)
- Relé: Desliga equipamentos automaticamente em casos críticos.

## Circuito

![Circuito-Challenge-Esp32.png](https://github.com/Nico-Araujo/FIAP/blob/5cc8750ab00ef7c1a4fcdfb5e586621566fd1ac5/Fase%204/Enterprise%20Challenge/Circuito-Challenge-Esp32.png)

Para verificar a funcionalidade do circuito basta clicar [aqui](https://wokwi.com/projects/433493506824089601)


## 📁 Estrutura de pastas

Dentre os arquivos e pastas presentes na raiz do projeto, definem-se:

- <b>Simulação Sensores</b>: Nesta pasta se encontram os arquivos da coleta de dados de sensores com ESP32 em ambiente simulado. Em vez de dados reais, usamos dados gerados e analisados em R.
- <b>Circuito-Challenge-Esp32.png</b>: Imagem do circuito e todos os componentes no Wokwi
- <b>Codigo-Circuito-Challenge-Esp32.cpp</b>: Código em c++ do circuito
- <b>Teste-1-Normal.png</b>: Print da simulação em condições normais
- <b>Teste-2-Alerta.png</b>: Print da simulação em condições de alerta
- <b>Teste-3-Critico.png</b>: Print da simulação em condições de estado crítico

- <b>README.md</b>: arquivo que serve como guia e explicação geral sobre o projeto (o mesmo que você está lendo agora).

## 🔧 Como executar o código

## Pré-requisitos

### Hardware
- Placa ESP32 (ex: ESP32-WROOM-32)
- Sensores:
  - DS18B20 (temperatura)
  - MPU6050 (vibração)
  - HC-SR04 (distância)
- Componentes:
  - 3 LEDs (verde, amarelo, vermelho)
  - Buzzer ativo 5V
  - Relé 5V
  - Resistor 4.7kΩ
  - Protoboard e jumpers

### Software
- [Arduino IDE 1.8+](https://www.arduino.cc/en/software)
- Pacote ESP32

### Bibliotecas (instale via `Sketch > Incluir Biblioteca > Gerenciar Bibliotecas`)
- OneWire
- DallasTemperature
- MPU6050 (by Electronic Cats)
- Wire (já vem instalada)

## Instalação

1. **Conecte os componentes** seguindo o diagrama:

 | Sensor       | Pino ESP32 |
 |--------------|-----------|
 | DS18B20 (DQ) | GPIO4     |
 | HC-SR04 (Trig)| GPIO5    |
 | HC-SR04 (Echo)| GPIO18   |
 | MPU6050 (SDA)| GPIO15    |
 | MPU6050 (SCL)| GPIO16    |
 | Relé         | GPIO19    |
 | Buzzer       | GPIO23    |
 | LED Verde    | GPIO21    |
 | LED Amarelo  | GPIO22    |
 | LED Vermelho | GPIO25    |

 > **Importante:** Use resistor 4.7kΩ entre DQ e VCC no DS18B20 (Fazendo um pull up)

2. **Configure a IDE Arduino**:
 - Selecione `Ferramentas > Placa > ESP32 Dev Module`
 - Escolha a porta COM correta

## 🚀 Execução

1. Copie o código deste repositório: [aqui](https://github.com/Nico-Araujo/FIAP/blob/4ced673f5fbabc7227ff271ea7cfacd9469c7b51/Fase%204/Enterprise%20Challenge/Codigo-Circuito-Challenge-Esp32.cpp)
2. Cole no software escolhido para a simulação (IDE Arduino, VS Code, Wokwi...)

