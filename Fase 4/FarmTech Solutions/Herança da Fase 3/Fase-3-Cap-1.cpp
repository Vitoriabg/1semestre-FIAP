#include <DHT.h>

// Definições de pinos
#define DHTPIN 4           // Pino de dados do DHT22
#define DHTTYPE DHT22      // Tipo do sensor
#define PH_PIN 34          // LDR como simulação de pH (analógico)
#define P_SENSOR_PIN 5     // Botão para fósforo
#define K_SENSOR_PIN 18    // Botão para potássio
#define RELAY_PIN 16       // Pino para controle do relé

DHT dht(DHTPIN, DHTTYPE); // Instancia o sensor DHT

void setup() {
  Serial.begin(115200);
  dht.begin();

  pinMode(P_SENSOR_PIN, INPUT_PULLUP); // Usa resistor interno
  pinMode(K_SENSOR_PIN, INPUT_PULLUP); // Usa resistor interno
  pinMode(RELAY_PIN, OUTPUT);
  digitalWrite(RELAY_PIN, LOW); // Começa com a bomba desligada
}

void loop() {
  // Leitura dos sensores
  float humidity = dht.readHumidity();
  int phRaw = analogRead(PH_PIN);
  float phSimulado = map(phRaw, 0, 4095, 0, 14); // Conversão para escala de pH (0-14)

  bool fosforoPresente = digitalRead(P_SENSOR_PIN) == LOW;
  bool potassioPresente = digitalRead(K_SENSOR_PIN) == LOW;

  // Lógica para ligar bomba
  bool ligarBomba = false;
  if (!isnan(humidity)) {
    if (humidity < 50 && fosforoPresente && potassioPresente) {
      ligarBomba = true;
    }
  }

  digitalWrite(RELAY_PIN, ligarBomba ? HIGH : LOW);

  // Impressão no monitor serial
  Serial.println("----- Leitura dos Sensores -----");
  Serial.print("Umidade: ");
  Serial.print(humidity);
  Serial.println("%");

  Serial.print("pH Simulado (LDR): ");
  Serial.println(phSimulado);

  Serial.print("Fósforo presente: ");
  Serial.println(fosforoPresente ? "Sim" : "Não");

  Serial.print("Potássio presente: ");
  Serial.println(potassioPresente ? "Sim" : "Não");

  Serial.print("Bomba de irrigação: ");
  Serial.println(ligarBomba ? "LIGADA" : "DESLIGADA");

  delay(2000);
}