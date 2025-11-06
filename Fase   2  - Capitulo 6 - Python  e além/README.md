# 🌾 Gestão de Insumos Agrícolas com Oracle

Este projeto realiza a gestão de insumos agrícolas — como fertilizantes, sementes e defensivos — utilizando banco de dados Oracle e também **backup local em JSON** para segurança e portabilidade dos dados.

---

## 🚀 Funcionalidades

✅ Inserção de novos insumos  
✅ Listagem de insumos cadastrados  
✅ Atualização da quantidade de insumos  
✅ Remoção de insumos do banco  
✅ 📊 Relatórios:
- Por validade próxima
- Estatístico por tipo de insumo  

✅ 💾 **Backup local automático em JSON**  
✅ Uso de estruturas complexas em Python (dicionários, laços, tratamento de dados)

---

## ⚙️ Como Executar

1. Configure sua conexão com Oracle no arquivo `oracle_connection.py`.
2. Execute o sistema:

```bash
python main.py
```

---

## 💾 Backup Local (JSON)

O sistema possui funcionalidade de **backup dos dados do Oracle** para um arquivo `.json`, permitindo:

- Armazenamento local para auditoria ou consulta
- Integração com sistemas externos
- Recuperação offline de informações

> O backup pode ser feito pelo menu principal do sistema.

📁 Arquivo gerado: `backup_insumos.json`

---

## 🧱 Estrutura esperada do banco de dados

Certifique-se que a tabela `insumos` está criada no Oracle com a seguinte estrutura:

```sql
CREATE TABLE insumos (
    nome VARCHAR2(50),
    tipo VARCHAR2(50),
    quantidade NUMBER,
    validade DATE
);
```

---

## 📦 Requisitos

- Python 3.x
- Oracle Database (local ou remoto)
- Biblioteca `cx_Oracle`:

```bash
pip install cx_Oracle
```

---

## 📁 Estrutura de Pastas

```
Gestao_de_Insumos/
│
├── main.py                 # Script principal
├── menu.py                 # Menu interativo com opções
├── funcoes_oracle.py       # Funções de banco Oracle
├── funcoes_json.py         # Funções de backup em JSON
├── oracle_connection.py    # Conexão com banco de dados
├── backup_insumos.json     # 🔄 Arquivo de backup local (gerado pelo sistema)
└── README.md               # Este arquivo
```

---

## 👩‍🌾 Ideal para

- Sistemas de controle rural
- Projetos acadêmicos (FIAP, faculdades técnicas etc.)
- Empresas agrícolas de pequeno/médio porte que desejam controle simples e seguro

---

✨ Desenvolvido com Python + Oracle para soluções inteligentes no campo!

