#include <Wire.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <MPU6050.h>
#include <WiFi.h>

// Definições dos pinos atualizadas
#define ONE_WIRE_BUS 4      // Pino do sensor DS18B20 (GPIO4)
#define TRIG_PIN 5          // Pino Trig do HC-SR04 (GPIO5)
#define ECHO_PIN 18         // Pino Echo do HC-SR04 (GPIO18)
#define RELAY_PIN 19        // Pino para controle do relé (GPIO19)
#define BUZZER_PIN 23       // Pino do buzzer (GPIO23)
#define LED_GREEN 21        // Pino do LED verde (GPIO21)
#define LED_YELLOW 22       // Pino do LED amarelo (GPIO22)
#define LED_RED 25          // Pino do LED vermelho (GPIO25)
#define MPU_SDA 15          // Pino SDA secundário para MPU6050 (GPIO15)
#define MPU_SCL 16          // Pino SCL secundário para MPU6050 (GPIO16)

// Limites de operação
#define TEMP_WARNING 60.0    // Temperatura de alerta (ºC)
#define TEMP_CRITICAL 80.0   // Temperatura crítica (ºC)
#define TEMP_SHUTDOWN 90.0   // Temperatura para desligamento (ºC)
#define VIB_WARNING 1.0      // Vibração de alerta (g)
#define VIB_CRITICAL 2.0     // Vibração crítica (g)
#define DIST_MIN 5.0         // Distância mínima (cm)
#define DIST_MAX 250.0       // Distância máxima (cm)
#define DIST_WARNING_LOW 10.0  // Distância baixa de alerta (cm)
#define DIST_WARNING_HIGH 200.0 // Distância alta de alerta (cm)

// Objetos dos sensores
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);
MPU6050 mpu;

// Variáveis de estado
bool systemNormal = true;
bool systemWarning = false;
bool systemCritical = false;

void setup() {
  Serial.begin(115200);

  //Conectando ao WIFI
  Serial.print("Conectando-se ao Wi-Fi");
  WiFi.begin("Wokwi-GUEST", "", 6);
  while (WiFi.status() != WL_CONNECTED) {
    delay(100);
    Serial.print(".");
  }
  Serial.println(" Conectado!");

  // Inicializa os pinos
  pinMode(LED_GREEN, OUTPUT);
  pinMode(LED_YELLOW, OUTPUT);
  pinMode(LED_RED, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);
  pinMode(RELAY_PIN, OUTPUT);
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  
  // Garante que tudo comece desligado
  digitalWrite(LED_GREEN, LOW);
  digitalWrite(LED_YELLOW, LOW);
  digitalWrite(LED_RED, LOW);
  digitalWrite(BUZZER_PIN, LOW);
  digitalWrite(RELAY_PIN, HIGH); // Relé normalmente aberto
  
  // Inicializa sensores
  sensors.begin();
  
  // Configura I2C com pinos secundários
  Wire.begin(MPU_SDA, MPU_SCL);
  mpu.initialize();
  
  if(!mpu.testConnection()) {
    Serial.println("MPU6050 não conectado! Verifique a fiação.");
    while(1);
  }
  
  Serial.println("Sistema inicializado. Iniciando monitoramento...");
}

void loop() {
  // Reinicia os estados
  systemNormal = true;
  systemWarning = false;
  systemCritical = false;
  
  // 1. Monitoramento de Temperatura
  sensors.requestTemperatures();
  float temperature = sensors.getTempCByIndex(0);
  
  if (temperature == DEVICE_DISCONNECTED_C) {
    Serial.println("Falha ao ler o sensor de temperatura!");
  } else {
    Serial.print("Temperatura: "); Serial.print(temperature); Serial.println(" °C");
    
    if (temperature > TEMP_CRITICAL || temperature >= TEMP_SHUTDOWN) {
      systemCritical = true;
      Serial.println("ALERTA: Temperatura crítica!");
      
      // Desliga o equipamento se a temperatura for muito alta
      if (temperature >= TEMP_SHUTDOWN) {
        digitalWrite(RELAY_PIN, LOW); // Desliga o relé
        Serial.println("EMERGÊNCIA: Equipamento desligado por superaquecimento!");
      }
    } else if (temperature > TEMP_WARNING) {
      systemWarning = true;
      Serial.println("Aviso: Temperatura acima do normal");
    }
  }
  
  // 2. Monitoramento de Vibração (MPU6050)
  int16_t ax, ay, az;
  mpu.getAcceleration(&ax, &ay, &az);
  
  // Converte valores brutos para g (considerando escala ±2g)
  float vibrationX = ax / 16384.0;
  float vibrationY = ay / 16384.0;
  float vibrationZ = az / 16384.0;
  
  // Calcula a vibração resultante
  float vibration = sqrt(vibrationX*vibrationX + vibrationY*vibrationY + vibrationZ*vibrationZ);
  
  Serial.print("Vibração: "); Serial.print(vibration); Serial.println(" g");
  
  if (vibration > VIB_CRITICAL) {
    systemCritical = true;
    Serial.println("ALERTA: Vibração crítica! Parando máquina...");
    digitalWrite(RELAY_PIN, LOW); // Desliga o relé
  } else if (vibration > VIB_WARNING) {
    systemWarning = true;
    Serial.println("Aviso: Vibração acima do normal");
  }
  
  // 3. Monitoramento de Distância
  float distance = measureDistance();
  Serial.print("Distância: "); Serial.print(distance); Serial.println(" cm");
  
  if (distance < DIST_MIN || distance > DIST_MAX) {
    systemCritical = true;
    Serial.println("ALERTA: Distância crítica!");
  } else if (distance < DIST_WARNING_LOW || distance > DIST_WARNING_HIGH) {
    systemWarning = true;
    Serial.println("Aviso: Distância fora da faixa normal");
  }
  
  // Controle dos LEDs e buzzer
  updateStatusIndicators();
  
  delay(1000); // Aguarda 1 segundo entre as leituras
}

float measureDistance() {
  // Envia pulso de 10us no pino Trig
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);
  
  // Mede o tempo de resposta no pino Echo
  long duration = pulseIn(ECHO_PIN, HIGH);
  
  // Calcula a distância (cm)
  float distance = duration * 0.034 / 2;
  
  return distance;
}

void updateStatusIndicators() {
  // Desliga todos os LEDs primeiro
  digitalWrite(LED_GREEN, LOW);
  digitalWrite(LED_YELLOW, LOW);
  digitalWrite(LED_RED, LOW);
  
  // Desliga o buzzer sempre que essa função for chamada (será reativado se necessário)
  noTone(BUZZER_PIN);
  digitalWrite(BUZZER_PIN, LOW);
  
  if (systemCritical) {
    // Estado crítico - LED vermelho e buzzer
    digitalWrite(LED_RED, HIGH);
    tone(BUZZER_PIN, 1000); // Buzzer ativo (1000Hz)
    Serial.println("STATUS: CRÍTICO - LED Vermelho e Buzzer ativados");
  } else if (systemWarning) {
    // Estado de alerta - LED amarelo (buzzer permanece desligado)
    digitalWrite(LED_YELLOW, HIGH);
    Serial.println("STATUS: ALERTA - LED Amarelo ativado");
  } else {
    // Estado normal - LED verde (buzzer já está desligado)
    digitalWrite(LED_GREEN, HIGH);
    Serial.println("STATUS: NORMAL - LED Verde ativado");
  }
}