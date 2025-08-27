from playwright.sync_api import sync_playwright
import re

def get_produtos_link(url):
    """
    Coleta todos os links dos produtos em uma página usando Playwright.
    """    
    print(f"Buscando links na página: {url}")
    links = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=60000)
                
        page.wait_for_selector("a.grid-card-link.url-image")

        anchors = page.locator("a.grid-card-link.url-image")
        for i in range(anchors.count()):
            href = anchors.nth(i).get_attribute("href")
            if href:
                links.append(href)

        browser.close()

    return links

def scrape_produtos_detalhes(produto_url):
    """
    Coleta os detalhes de um produto usando Playwright.
    """    
    print(f"Buscando detalhes do produto: {produto_url}")

    data = {
        'sku': '',
        'nome': '',
        'preco': 0.0,
        'preco_pix': 0.0,
        'valor_parcela': 0.0,
        'num_parcelas': 0,
        'informacoes_tecnicas': {}     
    }

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(produto_url, timeout=60000)

            # Espera título do produto carregar
            page.wait_for_selector("h1.product-title")

            # SKU e nome
            data['sku'] = page.locator("span.sku-active").inner_text().strip()
            
            #Nome do produto
            nome_produto = page.locator("h1.product-title > span").first.inner_text().strip()
            nome_produto = re.sub(r"\(Cód\..*?\)$", "", nome_produto).strip()
            data['nome'] = nome_produto
            
            # Preço do cartão
            preco_cartao_texto = page.locator("span.price-sales.pv-price-sale").inner_text()
            match_cartao = re.search(r"R\$\s*([\d.,]+)", preco_cartao_texto)
            data['preco'] = float(match_cartao.group(1).replace(".", "").replace(",", ".")) if match_cartao else 0.0

            # Preço Pix
            if page.locator("#pixChangePrice").count() > 0:
                preco_pix_texto = page.locator("#pixChangePrice").inner_text()
                match_pix = re.search(r"R\$\s*([\d.,]+)", preco_pix_texto)
                data['preco_pix'] = float(match_pix.group(1).replace(".", "").replace(",", ".")) if match_pix else 0.0

            # Parcelas 
            parcel_container = page.locator("div#mainProductParcel span.pv-parcel-resume")
            if parcel_container.count() > 0:
                valor_parcela_texto = parcel_container.locator("span.installments-amount").inner_text()
                num_parcelas_texto = parcel_container.locator("span.installments-number").inner_text()

                match_valor = re.search(r"[\d.,]+", valor_parcela_texto)
                data['valor_parcela'] = float(match_valor.group().replace(".", "").replace(",", ".")) if match_valor else 0.0

                match_num = re.search(r"\d+", num_parcelas_texto)
                data['num_parcelas'] = int(match_num.group()) if match_num else 0

            # Informações técnicas
            if page.locator("tbody").count() > 0:
                linhas = page.locator("tbody tr")
                for i in range(linhas.count()):
                    atributo = linhas.nth(i).locator("td.attribute-name").inner_text()
                    valor = linhas.nth(i).locator("td.attribute-value").inner_text()
                    data['informacoes_tecnicas'][atributo.strip()] = valor.strip()

            browser.close()

    except Exception as e:
        print(f"Erro ao extrair dados do produto {produto_url}: {e}")

    return data
