import sqlite3
import datetime
import random
import csv
import os
from typing import List, Dict, Any, Tuple, Optional

class BancoDadosAgricola:
    def __init__(self, nome_bd: str = "dados_agricolas.db"):
        """Inicializa a conexão com o banco de dados."""
        self.nome_bd = nome_bd
        self.conn = sqlite3.connect(nome_bd)
        self.cursor = self.conn.cursor()
        self.criar_tabelas()
        
    def criar_tabelas(self) -> None:
        """Cria a tabela de sensores se não existir."""
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS leituras_sensores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_hora TEXT NOT NULL,
            umidade REAL,
            ph REAL,
            fosforo INTEGER,
            potassio INTEGER,
            status_bomba INTEGER,
            observacoes TEXT
        )
        ''')
        self.conn.commit()
        print("Tabela criada com sucesso!")
        
    def inserir_leitura(self, umidade: float, ph: float, fosforo: int, 
                      potassio: int, status_bomba: int, observacoes: str = "") -> int:
        """
        Insere uma nova leitura no banco de dados.
        
        Args:
            umidade: Valor de umidade (%)
            ph: Valor de pH
            fosforo: Nível de fósforo (P)
            potassio: Nível de potássio (K)
            status_bomba: Status da bomba (0=desligada, 1=ligada)
            observacoes: Observações adicionais
            
        Returns:
            ID do registro inserido
        """
        data_hora = datetime.datetime.now().isoformat()
        
        self.cursor.execute('''
        INSERT INTO leituras_sensores 
        (data_hora, umidade, ph, fosforo, potassio, status_bomba, observacoes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (data_hora, umidade, ph, fosforo, potassio, status_bomba, observacoes))
        
        self.conn.commit()
        return self.cursor.lastrowid
    
    def obter_todas_leituras(self) -> List[Dict[str, Any]]:
        """Retorna todas as leituras do banco de dados."""
        self.cursor.execute('SELECT * FROM leituras_sensores')
        linhas = self.cursor.fetchall()
        
        colunas = [description[0] for description in self.cursor.description]
        resultado = []
        
        for linha in linhas:
            resultado.append(dict(zip(colunas, linha)))
            
        return resultado
    
    def obter_leitura_por_id(self, id_leitura: int) -> Optional[Dict[str, Any]]:
        """Retorna uma leitura específica pelo ID."""
        self.cursor.execute('SELECT * FROM leituras_sensores WHERE id = ?', (id_leitura,))
        linha = self.cursor.fetchone()
        
        if linha:
            colunas = [description[0] for description in self.cursor.description]
            return dict(zip(colunas, linha))
        return None
    
    def atualizar_leitura(self, id_leitura: int, **kwargs) -> bool:
        """
        Atualiza uma leitura existente.
        
        Args:
            id_leitura: ID do registro a ser atualizado
            **kwargs: Campos a serem atualizados (umidade, ph, etc.)
            
        Returns:
            True se a atualização foi bem-sucedida, False caso contrário
        """
        if not kwargs:
            return False
            
        # Construir a query de atualização dinamicamente
        set_clause = ", ".join([f"{key} = ?" for key in kwargs.keys()])
        valores = list(kwargs.values())
        valores.append(id_leitura)
        
        self.cursor.execute(
            f'UPDATE leituras_sensores SET {set_clause} WHERE id = ?', 
            valores
        )
        
        self.conn.commit()
        return self.cursor.rowcount > 0
    
    def deletar_leitura(self, id_leitura: int) -> bool:
        """
        Deleta uma leitura pelo ID.
        
        Args:
            id_leitura: ID do registro a ser deletado
            
        Returns:
            True se a deleção foi bem-sucedida, False caso contrário
        """
        self.cursor.execute('DELETE FROM leituras_sensores WHERE id = ?', (id_leitura,))
        self.conn.commit()
        return self.cursor.rowcount > 0
    
    def exportar_para_csv(self, nome_arquivo: str = "dados_sensores.csv") -> str:
        """
        Exporta todos os dados para um arquivo CSV.
        
        Args:
            nome_arquivo: Nome do arquivo CSV
            
        Returns:
            Caminho do arquivo CSV gerado
        """
        dados = self.obter_todas_leituras()
        
        if not dados:
            return "Sem dados para exportar"
            
        with open(nome_arquivo, 'w', newline='') as csvfile:
            nomes_campos = dados[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=nomes_campos)
            
            writer.writeheader()
            for linha in dados:
                writer.writerow(linha)
                
        return os.path.abspath(nome_arquivo)
    
    def importar_do_serial(self, dados_serial: List[str]) -> List[int]:
        """
        Importa dados do monitor serial.
        
        Args:
            dados_serial: Lista de strings com dados do monitor serial
            
        Returns:
            Lista de IDs dos registros inseridos
        """
        ids_inseridos = []
        
        for linha in dados_serial:
            # Assumindo formato: "umidade,ph,fosforo,potassio,status_bomba"
            try:
                partes = linha.strip().split(',')
                if len(partes) >= 5:
                    umidade = float(partes[0])
                    ph = float(partes[1])
                    fosforo = int(partes[2])
                    potassio = int(partes[3])
                    status_bomba = int(partes[4])
                    
                    observacoes = ""
                    if len(partes) > 5:
                        observacoes = partes[5]
                        
                    id_leitura = self.inserir_leitura(
                        umidade, ph, fosforo, potassio, status_bomba, observacoes
                    )
                    ids_inseridos.append(id_leitura)
            except (ValueError, IndexError) as e:
                print(f"Erro ao processar linha: {linha}. Erro: {e}")
                
        return ids_inseridos
    
    def fechar(self):
        """Fecha a conexão com o banco de dados."""
        if self.conn:
            self.conn.close()
            
    def __enter__(self):
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.fechar()


# Função para gerar dados simulados do monitor serial
def gerar_dados_exemplo(num_amostras: int = 10) -> List[str]:
    """
    Gera dados simulados do monitor serial.
    
    Args:
        num_amostras: Número de amostras a serem geradas
        
    Returns:
        Lista de strings simulando dados do monitor serial
    """
    dados = []
    
    for _ in range(num_amostras):
        umidade = round(random.uniform(20.0, 90.0), 1)  # 20% a 90%
        ph = round(random.uniform(4.0, 8.5), 1)  # pH 4.0 a 8.5
        fosforo = random.randint(0, 100)  # Nível de 0 a 100
        potassio = random.randint(0, 100)  # Nível de 0 a 100
        status_bomba = 1 if umidade < 40.0 else 0  # Liga a bomba se umidade < 40%
        
        linha = f"{umidade},{ph},{fosforo},{potassio},{status_bomba}"
        dados.append(linha)
        
    return dados


# Demonstração do uso da classe
if __name__ == "__main__":
    # Criar instância do banco de dados
    bd = BancoDadosAgricola()
    
    print("\n=== Demonstração do Sistema de Banco de Dados Agrícola ===\n")
    
    # 1. Gerar e importar dados simulados
    print("Gerando dados simulados do monitor serial...")
    dados_serial = gerar_dados_exemplo(15)
    print(f"Dados gerados: {dados_serial[:3]}... (total: {len(dados_serial)})")
    
    print("\nImportando dados para o banco de dados...")
    ids_inseridos = bd.importar_do_serial(dados_serial)
    print(f"Registros inseridos: {len(ids_inseridos)}")
    
    # 2. Consultar todos os registros
    print("\nConsultando todos os registros:")
    todas_leituras = bd.obter_todas_leituras()
    for i, leitura in enumerate(todas_leituras[:3]):
        print(f"  Registro {i+1}: {leitura}")
    if len(todas_leituras) > 3:
        print(f"  ... (mais {len(todas_leituras) - 3} registros)")
    
    # 3. Consultar um registro específico
    if ids_inseridos:
        id_leitura = ids_inseridos[0]
        print(f"\nConsultando registro com ID {id_leitura}:")
        leitura = bd.obter_leitura_por_id(id_leitura)
        print(f"  {leitura}")
    
    # 4. Atualizar um registro
    if ids_inseridos:
        id_leitura = ids_inseridos[0]
        print(f"\nAtualizando registro com ID {id_leitura}:")
        sucesso = bd.atualizar_leitura(id_leitura, umidade=95.5, observacoes="Valor atualizado manualmente")
        print(f"  Atualização {'bem-sucedida' if sucesso else 'falhou'}")
        
        # Verificar a atualização
        leitura_atualizada = bd.obter_leitura_por_id(id_leitura)
        print(f"  Registro atualizado: {leitura_atualizada}")
    
    # 5. Deletar um registro
    if len(ids_inseridos) > 1:
        id_leitura = ids_inseridos[-1]
        print(f"\nDeletando registro com ID {id_leitura}:")
        sucesso = bd.deletar_leitura(id_leitura)
        print(f"  Deleção {'bem-sucedida' if sucesso else 'falhou'}")
        
        # Verificar a deleção
        leitura_deletada = bd.obter_leitura_por_id(id_leitura)
        print(f"  Tentativa de buscar registro deletado: {leitura_deletada}")
    
    # 6. Exportar para CSV
    print("\nExportando dados para CSV:")
    caminho_csv = bd.exportar_para_csv()
    print(f"  Arquivo CSV gerado em: {caminho_csv}")
    
    # Fechar a conexão
    bd.fechar()
    print("\n=== Demonstração concluída ===")