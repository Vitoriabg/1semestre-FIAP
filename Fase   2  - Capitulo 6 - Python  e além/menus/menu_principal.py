from menus.menu_insumos import menu_insumos
from menus.menu_relatorios import menu_relatorios

def menu_principal():
    while True:
        print("\n--- MENU PRINCIPAL ---")
        print("1. Gerenciar Insumos")
        print("2. Relatórios")
        print("0. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            menu_insumos()
        elif opcao == "2":
            menu_relatorios()
        elif opcao == "0":
            print("Saindo...")
            break
        else:
            print("Opção inválida!")
