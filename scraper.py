import requests
from bs4 import BeautifulSoup

def get_produtos_link(url):
    """
    Coleta todos os links dos produtos em uma página.
    """    
    
    print(f"Buscando links na página: {url}")
        
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Erro ao acessar a página: {response.status_code}")
        return []    
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    links = []
    for a in soup.find_all('a', href=True):
        links.append(a['href'])        
        
    return links

def scrape_produtos_detalhes(produto_url):
    """
    Coleta os detalahes de um produto apartir do link.
    """    
    print(f"Buscando detalhes do produto e informações técnicas do produto: {produto_url}")

    response = requests.get(produto_url)
    if response.status_code != 200:
        print(f"Erro ao acessar a página: {response.status_code}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')

    data = {
        'sku': '',
        'nome': '',
        'preco': 0.0,
        'preco_pix': 0.0,
        'valor_parcela': 0.0,
        'num_parecelas': 0,
        'informacoes_tecnicas': {}     
    }
    
    try:
        data['sku'] = soup.find('span', class_='sku').text.strip()
        data['nome'] = soup.find('h1', class_='product-title').text.strip()
        data['preco'] = float(soup.find('span', class_='price-sales pv-price-sale').text.replace('R$', '').replace(',', '.').strip())
        data['preco_pix'] = float(soup.find('span', class_='pixChangePrice').text.replace('R$', '').replace(',', '.').strip())
        data['valor_parcela'] = float(soup.find('span', class_='installments-amount').text.replace('R$', '').replace(',', '.').strip())
        data['num_parecelas'] = int(soup.find('span', class_='installments-number').text.strip().split()[0])
        
        inf_tecnicas = soup.find('tbody')
        if inf_tecnicas:
            for linha in inf_tecnicas.find_all('tr'):
                atributo = linha.find_all('td', class_='attribute-name')
                valor =  linha.find_all('td', class_='attribute-value')
                if atributo and valor:
                    data['informacoes_tecnicas'][atributo[0].text.strip()] = valor[0].text.strip()
                
        
    except Exception as e:
        print(f"Erro ao extrair os dados: {produto_url} {e}")
    
    return data

