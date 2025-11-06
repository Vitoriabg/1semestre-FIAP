import cx_Oracle


def conectar_oracle():
    try:
        dsn = cx_Oracle.makedsn("ORACLE.FIAP.COM.BR",
                                1521, service_name="ORCL")
        conn = cx_Oracle.connect(user="RM562962", password="170180", dsn=dsn)
        print("Conexão com Oracle estabelecida.")
        return conn
    except Exception as e:
        print("Erro ao conectar:", e)
        return None


def desconectar_oracle(conn):
    if conn:
        conn.close()
        print("Conexão com Oracle encerrada.")
