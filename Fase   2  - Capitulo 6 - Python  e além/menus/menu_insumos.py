from funcoes_oracle import (
    inserir_insumo_oracle,
    listar_insumos_oracle,
    deletar_insumo_oracle,
    atualizar_quantidade_insumo_oracle
)

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
            # Aqui usamos um dicionário para agrupar os dados
            insumo = {"nome": nome, "tipo": tipo, "quantidade": quantidade, "validade": validade}
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
        elif opcao == "0":
            break
        else:
            print("Opção inválida!")
