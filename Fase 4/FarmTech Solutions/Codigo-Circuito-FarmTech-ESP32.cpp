#include <DHT.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

// ===== DEFINIÇÕES DE PINOS (OTIMIZADAS COM uint8_t) =====
const uint8_t DHTPIN = 4;          // Pino do DHT22 (1 byte)
const uint8_t DHTTYPE = DHT22;     // Tipo do sensor (1 byte)
const uint8_t PH_PIN = 34;         // Pino do LDR (1 byte)
const uint8_t P_SENSOR_PIN = 5;    // Slide switch - Fósforo (1 byte)
const uint8_t K_SENSOR_PIN = 18;   // Slide switch - Potássio (1 byte)
const uint8_t RELAY_PIN = 16;      // Pino do relé (1 byte)

// ===== CONFIGURAÇÃO DO LCD 20x4 I2C =====
const uint8_t LCD_ADDRESS = 0x27;  // Endereço I2C comum (1 byte)
const uint8_t LCD_COLUMNS = 20;    // 20 caracteres por linha (1 byte)
const uint8_t LCD_ROWS = 4;        // 4 linhas (1 byte)

DHT dht(DHTPIN, DHTTYPE);
LiquidCrystal_I2C lcd(LCD_ADDRESS, LCD_COLUMNS, LCD_ROWS);

// ===== ESTRUTURA DE DADOS OTIMIZADA =====
struct SensorData {
  float humidity;          // 4 bytes (precisão decimal necessária)
  float phSimulado;        // 4 bytes (pH 0.0-14.0)
  bool fosforoPresente;    // 1 byte (true/false)
  bool potassioPresente;   // 1 byte (true/false)
  bool bombaLigada;        // 1 byte (true/false)
};

// ===== VARIÁVEIS GLOBAIS =====
SensorData currentData;    // Armazena as leituras atuais

// ===== PROTÓTIPOS DE FUNÇÃO =====
void readSensors();
bool shouldPumpActivate();
void updateDisplay();
void printToSerialPlotter();

// ===== SETUP (INICIALIZAÇÃO) =====
void setup() {
  Serial.begin(115200);
  dht.begin();

  // Inicializa o LCD 20x4
  lcd.init();
  lcd.backlight();
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print(F("Sistema Irrigacao"));  // F() armazena na Flash
  lcd.setCursor(0, 1);
  lcd.print(F("Inicializando..."));

  // Configura os pinos
  pinMode(P_SENSOR_PIN, INPUT);
  pinMode(K_SENSOR_PIN, INPUT);
  pinMode(RELAY_PIN, OUTPUT);
  digitalWrite(RELAY_PIN, LOW);

  delay(2000);
}

// ===== LEITURA DOS SENSORES =====
void readSensors() {
  currentData.humidity = dht.readHumidity();
  
  int16_t phRaw = analogRead(PH_PIN);  // 2 bytes (0-4095)
  currentData.phSimulado = map(phRaw, 0, 4095, 0, 140) / 10.0f;  // 'f' para float
  
  currentData.fosforoPresente = digitalRead(P_SENSOR_PIN) == HIGH;
  currentData.potassioPresente = digitalRead(K_SENSOR_PIN) == HIGH;
}

// ===== LÓGICA DE ATIVAÇÃO DA BOMBA =====
bool shouldPumpActivate() {
  return (!isnan(currentData.humidity) && 
         (currentData.humidity < 50) && 
         currentData.fosforoPresente && 
         currentData.potassioPresente);
}

// ===== ATUALIZA O DISPLAY LCD =====
void updateDisplay() {
  lcd.clear();
  
  // Linha 1: Umidade e pH
  lcd.setCursor(0, 0);
  lcd.print(F("U:"));
  lcd.print(currentData.humidity, 0);
  lcd.print(F("% pH:"));
  lcd.print(currentData.phSimulado, 1);

  // Linha 2: Fósforo e Potássio
  lcd.setCursor(0, 1);
  lcd.print(F("P:"));
  lcd.print(currentData.fosforoPresente ? F("SIM  ") : F("NAO  "));
  lcd.print(F("K:"));
  lcd.print(currentData.potassioPresente ? F("SIM") : F("NAO"));

  // Linha 3: Status da bomba
  lcd.setCursor(0, 2);
  lcd.print(F("Bomba: "));
  lcd.print(currentData.bombaLigada ? F("LIGADA") : F("DESLIGADA"));

  // Linha 4: Mensagem de status
  lcd.setCursor(0, 3);
  if (currentData.bombaLigada) {
    lcd.print(F("IRRIGANDO..."));
  } else if (currentData.humidity < 50) {
    lcd.print(F("UMIDADE BAIXA!"));
  } else {
    lcd.print(F("SISTEMA OK"));
  }
}

// ===== SAÍDA PARA SERIAL PLOTTER =====
void printToSerialPlotter() {
  Serial.print(F("Umidade:"));
  Serial.print(currentData.humidity);
  Serial.print(F(" pH:"));
  Serial.print(currentData.phSimulado);
  Serial.print(F(" Bomba:"));
  Serial.println(currentData.bombaLigada ? "1" : "0");
}

// ===== LOOP PRINCIPAL =====
void loop() {
  readSensors();
  currentData.bombaLigada = shouldPumpActivate();
  
  digitalWrite(RELAY_PIN, currentData.bombaLigada ? HIGH : LOW);
  
  updateDisplay();
  printToSerialPlotter();

  delay(2000);
}