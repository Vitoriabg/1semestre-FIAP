
import json
import os
from datetime import datetime

# Caminho dos arquivos locais
CAMINHO_JSON = "dados_insumos.json"
CAMINHO_TXT = "relatorio_insumos.txt"


def salvar_json(dados):
    """
    Salva os dados de insumos no arquivo JSON.
    """
    try:
        with open(CAMINHO_JSON, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)
        print("Backup local em JSON salvo com sucesso.")
    except Exception as e:
        print(f"Erro ao salvar JSON: {e}")


def carregar_json():
    """
    Carrega os dados do arquivo JSON, se existir.
    """
    if not os.path.exists(CAMINHO_JSON):
        return []
    try:
        with open(CAMINHO_JSON, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Erro ao carregar JSON: {e}")
        return []


def exportar_txt(dados):
    """
    Exporta os dados de insumos em formato texto (.txt) legível.
    """
    try:
        with open(CAMINHO_TXT, 'w', encoding='utf-8') as f:
            f.write("RELATÓRIO DE INSUMOS AGRÍCOLAS\n")
            f.write(
                f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n")
            f.write(
                f"{'ID':<5} {'Nome':<20} {'Tipo':<15} {'Quantidade':<10} {'Data Compra':<15}\n")
            f.write("-" * 70 + "\n")
            for item in dados:
                f.write(f"{item.get('id', '-'):<5} {item.get('nome', '-'):<20} {item.get('tipo', '-'):<15} "
                        f"{item.get('quantidade', '-'):<10} {item.get('data_compra', '-'):<15}\n")
        print("Relatório .txt gerado com sucesso.")
    except Exception as e:
        print(f"Erro ao gerar relatório TXT: {e}")
