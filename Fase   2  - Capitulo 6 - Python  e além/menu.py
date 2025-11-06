from funcoes_oracle import (
    inserir_insumo_oracle,
    listar_insumos_oracle,
    listar_insumos_oracle_json,
    deletar_insumo_oracle,
    atualizar_quantidade_insumo_oracle,
    relatorio_validade_proxima_oracle,
    relatorio_estatistico_oracle,
)
from persistencia_local import *


def menu_principal():
    while True:
        print("\n--- MENU PRINCIPAL ---")
        print("1. Gerenciar Insumos")
        print("2. Relatórios")
        print("3. Backup Local")
        print("0. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            menu_insumos()
        elif opcao == "2":
            menu_relatorios()
        elif opcao == "3":
            menu_backup()
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")


def menu_insumos():
    while True:
        print("\n--- MENU INSUMOS ---")
        print("1. Adicionar Insumo")
        print("2. Listar Insumos")
        print("3. Atualizar Quantidade")
        print("4. Remover Insumo")
        print("0. Voltar")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome = input("Nome: ")
            tipo = input("Tipo: ")
            quantidade = int(input("Quantidade: "))
            validade = input("Validade (YYYY-MM-DD): ")
            insumo = {"nome": nome, "tipo": tipo,
                      "quantidade": quantidade, "validade": validade}
            inserir_insumo_oracle(insumo)
        elif opcao == "2":
            listar_insumos_oracle()
        elif opcao == "3":
            nome = input("Nome do insumo: ")
            nova_qtd = int(input("Nova quantidade: "))
            atualizar_quantidade_insumo_oracle(nome, nova_qtd)
        elif opcao == "4":
            nome = input("Nome do insumo a remover: ")
            deletar_insumo_oracle(nome)
        elif opcao == '5':
            salvar_dados_localmente()
        elif opcao == "0":
            break
        else:
            print("Opção inválida!")


def menu_relatorios():
    while True:
        print("\n--- MENU RELATÓRIOS ---")
        print("1. Validade Próxima")
        print("2. Estatística por Tipo")
        print("0. Voltar")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            dias = int(input("Quantos dias até a validade? "))
            relatorio_validade_proxima_oracle(dias)
        elif opcao == "2":
            relatorio_estatistico_oracle()
        elif opcao == "0":
            break
        else:
            print("Opção inválida!")


def menu_backup():
    while True:
        print("\n--- MENU BACKUP LOCAL ---")
        print("1. Salvar backup em JSON")
        print("2. Carregar dados do JSON")
        print("3. Exportar TXT")
        print("0. Voltar")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            dados = listar_insumos_oracle_json()
            salvar_json(dados)
        elif opcao == "2":
            dados = carregar_json()
            for insumo in dados:
                print(insumo)
        elif opcao == "3":
            dados = carregar_json()
            exportar_txt(dados)
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")
    while True:
        print("\n--- MENU BACKUP LOCAL ---")
        print("1. Importar Dados")
        print("2. Exportar Dados Txt")
        print("0. Voltar")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            listar_insumos_oracle()
        elif opcao == "2":
            carregar_json()
        elif opcao == "0":
            break
        else:
            print("Opção inválida!")


def salvar_dados_localmente():
    # você já deve ter uma função assim
    dados = listar_insumos_oracle_json()
    salvar_json(dados)
