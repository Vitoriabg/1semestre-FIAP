import requests
import json
import datetime
import time
from typing import Dict, Any, Optional, Tuple
from banco_dados_agricola import BancoDadosAgricola

class IntegracaoClima:
    def __init__(self, chave_api: str, cidade: str = "São Paulo", codigo_pais: str = "BR"):
        """
        Inicializa a integração com a API do OpenWeather.
        
        Args:
            chave_api: Chave de API do OpenWeather
            cidade: Cidade para previsão do tempo
            codigo_pais: Código do país
        """
        self.chave_api = chave_api
        self.cidade = cidade
        self.codigo_pais = codigo_pais
        self.url_base = "https://api.openweathermap.org/data/2.5"
        
    def obter_clima_atual(self) -> Dict[str, Any]:
        """
        Obtém o clima atual.
        
        Returns:
            Dicionário com dados do clima atual
        """
        url = f"{self.url_base}/weather"
        params = {
            "q": f"{self.cidade},{self.codigo_pais}",
            "appid": self.chave_api,
            "units": "metric",
            "lang": "pt_br"
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Erro ao obter clima atual: {response.status_code}")
            print(response.text)
            return {}
            
    def obter_previsao(self, dias: int = 1) -> Dict[str, Any]:
        """
        Obtém a previsão do tempo para os próximos dias.
        
        Args:
            dias: Número de dias para previsão (1-5)
            
        Returns:
            Dicionário com dados da previsão
        """
        url = f"{self.url_base}/forecast"
        params = {
            "q": f"{self.cidade},{self.codigo_pais}",
            "appid": self.chave_api,
            "units": "metric",
            "lang": "pt_br",
            "cnt": min(dias * 8, 40)  # 8 previsões por dia (a cada 3 horas)
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Erro ao obter previsão: {response.status_code}")
            print(response.text)
            return {}
    
    def vai_chover_hoje(self) -> Tuple[bool, float]:
        """
        Verifica se vai chover hoje.
        
        Returns:
            Tupla com (vai_chover, probabilidade_de_chuva)
        """
        previsao = self.obter_previsao(1)
        
        if not previsao or "list" not in previsao:
            return False, 0.0
            
        # Verificar as próximas 24 horas
        vai_chover = False
        probabilidade_maxima = 0.0
        
        for periodo in previsao["list"][:8]:  # 8 períodos de 3 horas = 24 horas
            # Verificar se há chuva na previsão
            if "rain" in periodo:
                vai_chover = True
                
            # Verificar probabilidade de precipitação
            if "pop" in periodo:
                probabilidade = periodo["pop"] * 100  # Converter para porcentagem
                probabilidade_maxima = max(probabilidade_maxima, probabilidade)
                
            # Verificar descrição do clima
            id_clima = periodo["weather"][0]["id"]
            # IDs 2xx (tempestade), 3xx (garoa), 5xx (chuva), 6xx (neve)
            if id_clima < 700:
                vai_chover = True
                
        return vai_chover, probabilidade_maxima
        
    def deve_ativar_bomba(self, umidade: float, limiar_chuva: float = 50.0) -> bool:
        """
        Decide se a bomba deve ser ativada com base na umidade e previsão de chuva.
        
        Args:
            umidade: Valor atual de umidade (%)
            limiar_chuva: Limiar de probabilidade de chuva para não ativar a bomba (%)
            
        Returns:
            True se a bomba deve ser ativada, False caso contrário
        """
        # Se a umidade já estiver alta, não precisa irrigar
        if umidade >= 70.0:
            return False
            
        # Verificar previsão de chuva
        vai_chover, probabilidade = self.vai_chover_hoje()
        
        # Se a probabilidade de chuva for alta, não irrigar
        if vai_chover and probabilidade >= limiar_chuva:
            return False
            
        # Se a umidade estiver baixa e não há previsão de chuva significativa, irrigar
        return umidade < 40.0


# Demonstração da integração com o clima
def demonstrar_integracao_clima(chave_api: str):
    """
    Demonstra a integração com a API do OpenWeather.
    
    Args:
        chave_api: Chave de API do OpenWeather
    """
    # Se não tiver uma chave de API, usar um exemplo simulado
    if not chave_api or chave_api == "SUA_CHAVE_API_AQUI":
        print("\n=== Demonstração com dados simulados (sem chave API) ===\n")
        # Simular dados de clima
        vai_chover = False
        probabilidade = 10.0
        umidade = 35.0
        
        print(f"Umidade atual: {umidade}%")
        print(f"Previsão de chuva: {'Sim' if vai_chover else 'Não'}")
        print(f"Probabilidade de chuva: {probabilidade:.1f}%")
        
        # Decisão de irrigação
        deve_irrigar = umidade < 40.0 and (not vai_chover or probabilidade < 50.0)
        print(f"\nDecisão: {'Ativar' if deve_irrigar else 'Não ativar'} a bomba de irrigação")
        
        # Registrar no banco de dados
        with BancoDadosAgricola() as bd:
            # Gerar dados simulados
            ph = 6.5
            fosforo = 75
            potassio = 60
            status_bomba = 1 if deve_irrigar else 0
            
            id_leitura = bd.inserir_leitura(
                umidade=umidade,
                ph=ph,
                fosforo=fosforo,
                potassio=potassio,
                status_bomba=status_bomba,
                observacoes=f"Decisão baseada em clima simulado. Prob. chuva: {probabilidade:.1f}%"
            )
            
            print(f"\nRegistro adicionado ao banco de dados (ID: {id_leitura})")
            print(f"Dados: Umidade={umidade}%, pH={ph}, P={fosforo}, K={potassio}, Bomba={'Ligada' if status_bomba else 'Desligada'}")
        
        return
    
    # Usar a API real
    print("\n=== Demonstração da Integração com OpenWeather API ===\n")
    
    clima = IntegracaoClima(chave_api)
    
    # Obter clima atual
    atual = clima.obter_clima_atual()
    if atual:
        print(f"Clima atual em {clima.cidade}:")
        print(f"  Temperatura: {atual.get('main', {}).get('temp', 'N/A')}°C")
        print(f"  Umidade: {atual.get('main', {}).get('humidity', 'N/A')}%")
        print(f"  Condição: {atual.get('weather', [{}])[0].get('description', 'N/A')}")
        
        # Usar a umidade real da API
        umidade = atual.get('main', {}).get('humidity', 35.0)
    else:
        # Valor padrão se não conseguir obter da API
        umidade = 35.0
        print("Não foi possível obter o clima atual. Usando valor padrão de umidade: 35%")
    
    # Verificar previsão de chuva
    vai_chover, probabilidade = clima.vai_chover_hoje()
    print(f"\nPrevisão para as próximas 24 horas:")
    print(f"  Vai chover: {'Sim' if vai_chover else 'Não'}")
    print(f"  Probabilidade máxima de precipitação: {probabilidade:.1f}%")
    
    # Decisão de irrigação
    deve_irrigar = clima.deve_ativar_bomba(umidade)
    print(f"\nDecisão: {'Ativar' if deve_irrigar else 'Não ativar'} a bomba de irrigação")
    
    # Registrar no banco de dados
    with BancoDadosAgricola() as bd:
        # Gerar alguns dados simulados (que viriam dos sensores)
        ph = 6.5
        fosforo = 75
        potassio = 60
        status_bomba = 1 if deve_irrigar else 0
        
        id_leitura = bd.inserir_leitura(
            umidade=umidade,
            ph=ph,
            fosforo=fosforo,
            potassio=potassio,
            status_bomba=status_bomba,
            observacoes=f"Decisão baseada no clima. Prob. chuva: {probabilidade:.1f}%"
        )
        
        print(f"\nRegistro adicionado ao banco de dados (ID: {id_leitura})")
        print(f"Dados: Umidade={umidade}%, pH={ph}, P={fosforo}, K={potassio}, Bomba={'Ligada' if status_bomba else 'Desligada'}")


if __name__ == "__main__":
   
    CHAVE_API = "7aff6a9802e63fd6dc7d0091391f0195"
    
    demonstrar_integracao_clima(CHAVE_API)