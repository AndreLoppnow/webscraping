# Webscraping Loja Maeto

Este projeto realiza webscraping de produtos do site [Loja Maeto](https://www.lojamaeto.com), salvando os dados em um banco SQLite local.

## Funcionalidades

- Busca de produtos por nome.
- Coleta automática dos links dos produtos encontrados.
- Extração de detalhes dos produtos (SKU, nome, preços, parcelas, informações técnicas).
- Armazenamento dos dados em banco de dados SQLite, com atualização automática.

## Estrutura dos Arquivos

- `main.py`: Ponto de entrada do projeto. Gerencia o fluxo de scraping e armazenamento.
- `scraper.py`: Responsável por coletar links e detalhes dos produtos usando Playwright.
- `database.py`: Gerencia a criação das tabelas e inserção/atualização dos dados no banco SQLite.
- `requirements.txt`: Lista de dependências do projeto.
- `data/produtos.db`: Banco de dados SQLite gerado automaticamente.

## Como usar

1. **Instale as dependências**  
   Recomendado usar um ambiente virtual:
   ```sh
   python -m venv env
   .\env\Scripts\activate  # No Windows
   pip install -r requirements.txt
   playwright install
   ```

2. **Execute o script principal**
   ```sh
   python main.py
   ```
   Digite o nome do produto quando solicitado.

3. **Os dados serão salvos em [`data/produtos.db`](data/produtos.db )**.

## Observações

- O scraping utiliza o Playwright em modo headless.
- O banco de dados é criado automaticamente na primeira execução.
- O script atualiza produtos já existentes pelo SKU.

## Requisitos

- Python 3.13.3
- [Playwright](https://playwright.dev/python/)
- requests

## Licença

Uso educacional.
