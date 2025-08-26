sqlite3 LojaMaeto.db

-- Criação da tabela Produtos
CREATE TABLE produto (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sku TEXT UNIQUE NOT NULL,
    nome_produto TEXT,
    preco REAL,    
    preco_pix REAL,
    valor_parcelas REAL,
    numero_parcelas INTEGER,
    estoque INTEGER 
);

CREATE TABLE informacao_tecnica (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    produto_id INTEGER,
    valor TEXT,
    atributo TEXT,
    FOREIGN KEY (produto_id) REFERENCES produtos(id)
);
