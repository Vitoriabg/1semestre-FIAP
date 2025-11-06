from funcoes_oracle import (
    relatorio_validade_proxima_oracle,
    relatorio_validade_entre_datas_oracle,
    exportar_insumos_csv
)

def menu_relatorios():
    while True:
        print("\n--- MENU RELATÓRIOS ---")
        print("1. Insumos com validade próxima")
        print("2. Insumos entre duas datas de validade")
        print("3. Exportar dados para CSV")
        print("0. Voltar")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            dias = int(input("Quantos dias até o vencimento? "))
            relatorio_validade_proxima_oracle(dias)
        elif opcao == "2":
            data_inicio = input("Data início (YYYY-MM-DD): ")
            data_fim = input("Data fim (YYYY-MM-DD): ")
            relatorio_validade_entre_datas_oracle(data_inicio, data_fim)
        elif opcao == "3":
            exportar_insumos_csv()
        elif opcao == "0":
            break
        else:
            print("Opção inválida!")
