import sqlite3
import os

CAMINHO_DB = os.path.join(os.path.dirname(__file__), 'data', 'produtos.db')

def criar_tabela():
    """Cria a tabela de 'produto' e 'informacao_tecnica' no banco de dados"""
    
    os.makedirs(os.path.dirname(CAMINHO_DB), exist_ok=True)

    con = sqlite3.connect(CAMINHO_DB)
    cursor = con.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produto(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sku TEXT UNIQUE NOT NULL,
            nome_produto TEXT,
            preco REAL,    
            preco_pix REAL,
            valor_parcelas REAL,
            numero_parcelas INTEGER
    )''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS informacao_tecnica(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto_id INTEGER,
            atributo TEXT,
            valor TEXT,
            FOREIGN KEY (produto_id) REFERENCES produto(id)
   )''')
    
    con.commit()
    con.close()
    
def inserir_produto(data):
    """Insere ou atualiza os dados do produto e suas informações técnicas"""
    
    con = sqlite3.connect(CAMINHO_DB)
    cursor = con.cursor()
    try:
        cursor.execute('''
            INSERT INTO produto (sku, nome_produto, preco, preco_pix, valor_parcelas, numero_parcelas)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(sku) DO UPDATE SET
                nome_produto=excluded.nome_produto,
                preco=excluded.preco,
                preco_pix=excluded.preco_pix,
                valor_parcelas=excluded.valor_parcelas,
                numero_parcelas=excluded.numero_parcelas
        ''', (
            data['sku'],
            data['nome'],
            data['preco'],
            data['preco_pix'],
            data['valor_parcela'],
            data['num_parcelas'],
        ))
        produto_id = cursor.lastrowid or cursor.execute("SELECT id FROM produto WHERE sku=?", (data['sku'],)).fetchone()[0]
        
        cursor.execute("DELETE FROM informacao_tecnica WHERE produto_id=?", (produto_id,))
        
        for atributo, valor in data['informacoes_tecnicas'].items():
            cursor.execute('''
                INSERT INTO informacao_tecnica (produto_id, atributo, valor)
                VALUES (?, ?, ?)
            ''', (produto_id, atributo, valor))
        
        con.commit()
        return True
    except Exception as e:
        print(f"Erro ao inserir produto: {data.get('nome', 'N/A')} -> {e}")
        con.rollback()
        return False
    finally:        
        con.close()
