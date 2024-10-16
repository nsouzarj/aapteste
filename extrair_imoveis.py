from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

# Configuração do Selenium
chrome_options = Options()
#chrome_options.add_argument("--headless")  # Executar em modo headless
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

# Inicializar o driver
service = Service('caminho/para/seu/chromedriver')  # Substitua pelo caminho do seu chromedriver
driver = webdriver.Chrome(service=service, options=chrome_options)

# Acessar a página de listagem de imóveis
url  = "https://www.zapimoveis.com.br/venda/?__ab=sup-hl-pl:newC,exp-aa-test:B,super-high:new,off-no-hl:new,TOP-FIXED:card-b,pos-zap:control,new-rec:b,lgpd-ldp:test&transacao=venda&pagina=1"
  # Substitua pela URL real
driver.get(url)

# Esperar o carregamento da página
time.sleep(5)  # Ajuste o tempo conforme necessário

# Obter o HTML da página
html_content = driver.page_source

# Criar um objeto BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Encontrar todos os cards de imóveis
cards = soup.find_all('div', class_='ListingCard_result-card__Pumtx')

# Lista para armazenar os dados dos imóveis
imoveis = []

# Extrair informações de cada card
for card in cards:
    titulo = card.find('h2', class_='l-text--variant-heading-small').text.strip()
    descricao = card.find('p', class_='ListingCard_card__description__slBTG').text.strip()
    preco = card.find('p', class_='l-text--variant-heading-small l-text--weight-bold').text.strip()
    localizacao = card.find('section', class_='card__location').text.strip()
    
    # Extrair o link do imóvel
    link = card.find('a', itemprop='url')['href']
    
    # Adicionar os dados do imóvel à lista
    imoveis.append({
        'titulo': titulo,
        'descricao': descricao,
        'preco': preco,
        'localizacao': localizacao,
        'link': link  # Adicionando o link
    })

# Exibir os imóveis extraídos
for imovel in imoveis:
    print(imovel)

# Fechar o navegador
driver.quit()
