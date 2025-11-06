from oracle_connection import conectar_oracle, desconectar_oracle


def inserir_insumo_oracle(insumo):
    # insumo é um dicionário: {'nome': str, 'tipo': str, 'quantidade': int, 'validade': str}
    conn = conectar_oracle()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO insumos (nome, tipo, quantidade, validade)
                VALUES (:1, :2, :3, TO_DATE(:4, 'YYYY-MM-DD'))
            """, (insumo['nome'], insumo['tipo'], insumo['quantidade'], insumo['validade']))
            conn.commit()
            print("Insumo inserido com sucesso.")
        except Exception as e:
            print("Erro ao inserir:", e)
        finally:
            desconectar_oracle(conn)


def listar_insumos_oracle():
    conn = conectar_oracle()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT nome, tipo, quantidade, TO_CHAR(validade, 'YYYY-MM-DD') FROM insumos")
            for row in cursor.fetchall():
                print(
                    f"Nome: {row[0]}, Tipo: {row[1]}, Quantidade: {row[2]}, Validade: {row[3]}")
        except Exception as e:
            print("Erro ao listar:", e)
        finally:
            desconectar_oracle(conn)


def atualizar_quantidade_insumo_oracle(nome, nova_qtd):
    conn = conectar_oracle()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE insumos SET quantidade = :1 WHERE nome = :2", (nova_qtd, nome))
            conn.commit()
            print("Quantidade atualizada.")
        except Exception as e:
            print("Erro ao atualizar:", e)
        finally:
            desconectar_oracle(conn)


def deletar_insumo_oracle(nome):
    conn = conectar_oracle()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM insumos WHERE nome = :1", (nome,))
            conn.commit()
            print("Insumo deletado.")
        except Exception as e:
            print("Erro ao deletar:", e)
        finally:
            desconectar_oracle(conn)


def relatorio_validade_proxima_oracle(dias):
    conn = conectar_oracle()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
    SELECT nome, validade
    FROM insumos
    WHERE TRUNC(validade) BETWEEN TRUNC(SYSDATE) AND TRUNC(SYSDATE + :dias)
    """, [dias])
            print("Insumos com validade próxima:")
            for row in cursor.fetchall():
                print(f"Nome: {row[0]} - Validade: {row[1]}")
        except Exception as e:
            print("Erro no relatório:", e)
        finally:
            desconectar_oracle(conn)


def relatorio_estatistico_oracle():
    # Exemplo de uso de dicionário para agregar estatísticas
    conn = conectar_oracle()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT tipo, COUNT(*), SUM(quantidade) FROM insumos GROUP BY tipo")
            print("Relatório Estatístico por Tipo de Insumo:")
            for tipo, qtd, soma in cursor.fetchall():
                print(
                    f"Tipo: {tipo}, Quantidade Total de Itens: {qtd}, Soma das Quantidades: {soma}")
        except Exception as e:
            print("Erro no relatório estatístico:", e)
        finally:
            desconectar_oracle(conn)


def listar_insumos_oracle_json():
    conn = conectar_oracle()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT nome, tipo, quantidade, TO_CHAR(validade, 'YYYY-MM-DD') FROM insumos"
            )
            resultados = cursor.fetchall()

            dados = []
            for row in resultados:
                dados.append({
                    "nome": row[0],
                    "tipo": row[1],
                    "quantidade": row[2],
                    "validade": row[3] if row[3] else "-"
                })

            # Exibir se quiser
            for item in dados:
                print(item)

            return dados  # Essencial para o JSON

        except Exception as e:
            print("Erro ao listar insumos para JSON:", e)
            return []
        finally:
            cursor.close()
            conn.close()
