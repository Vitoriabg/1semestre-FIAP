
from banco_dados_agricola import BancoDadosAgricola

bd = BancoDadosAgricola()
dados = bd.consultar_todos()
for registro in dados:
    print(registro)
