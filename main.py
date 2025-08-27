from database import criar_tabela, inserir_produto
from scraper import get_produtos_link, scrape_produtos_detalhes
from time import sleep

def main():
    print("Iniciando o processo de scraping...")
    criar_tabela()
    produto = input("Digite o nome do produto: ")
    urls = get_produtos_link("https://www.lojamaeto.com/search/?q="+produto)
    if not urls:
        print("Nenhum link de produto encontrado.")
        return
    print(f"Encontrados {len(urls)} links de produtos.")
    
    for link in urls:
        url_completa = f"https://www.lojamaeto.com{link}" if link.startswith('/') else link
        produto_data = scrape_produtos_detalhes(url_completa)
        if produto_data:
            inserir_produto(produto_data)
            sleep(1)
             
    print("Processo de scraping concluído.")

if __name__ == "__main__":
    main()