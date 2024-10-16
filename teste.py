from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from openpyxl import Workbook
import pandas as pd

# Configurando opções do Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")  # Comente esta linha para ver o navegador
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")  # Desativa a aceleração de hardware
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

# Caminho para o ChromeDriver
chrome_driver_path = r"C:\Users\User\ChromeWithDriver\chromedriver.exe"

# Inicializando o ChromeDriver
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Inicializando um conjunto para armazenar links únicos
links_imoveis = set()

# Número da página inicial
pagina_atual = 1

cont = 0 

pagina_tela = 0

# Coletando links dos imóveis
while pagina_atual >= 1:
    registro = 0
   
    # Inicializando o ChromeDriver
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    # Montando a URL com o número da página atual
    link_nova_lina = f"https://www.zapimoveis.com.br/venda/casas/mg+nova-lima/4-quartos/?__ab=sup-hl-pl:newC,exp-aa-test:B,super-high:new,off-no-hl:new,TOP-FIXED:card-b,pos-zap:control,new-rec:b,lgpd-ldp:test&transacao=venda&onde=,Minas%20Gerais,Nova%20Lima,,,,,city,BR%3EMinas%20Gerais%3ENULL%3ENova%20Lima,-19.984906,-43.846963,&tipos=casa_residencial&pagina=1&amenities=Piscina%20privativa&banheiros=4&quartos=4&vagas=4"
    
    url = link_nova_lina
    # url = f"https://www.zapimoveis.com.br/venda/imoveis/rj+rio-de-janeiro/?__ab=sup-hl-pl:newC,exp-aa-test:B,super-high:new,off-no-hl:new,TOP-FIXED:card-b,pos-zap:control,new-rec:b,lgpd-ldp:test&transacao=venda&onde=,Rio%20de%20Janeiro,Rio%20de%20Janeiro,,,,,city,BR%3ERio%20de%20Janeiro%3ENULL%3ERio%20de%20Janeiro,-22.906847,-43.172897,&pagina={pagina_atual}"

    # Acessando a URL
    print(f"Acessando a URL: {url}")
    driver.get(url)

    # Espera até que os imóveis estejam carregados
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/main/section/div/form/div[2]/div[4]/div[1]/div/div[1]/div/a/div/div[1]/div[2]')))
    print("Elemento de verificação encontrado. Iniciando a coleta de links.")

    # Seleciona todos os cards de imóveis na página
    imoveis = driver.find_elements(By.XPATH, '//*[@id="__next"]/main/section/div/form/div[2]/div[4]/div[1]/div/div') 
                                             
    print(f"Número de imóveis encontrados na página: {len(imoveis)}")  
    
    # Verifica se já coletou todos os imóveis da página atual
    if not imoveis:
        print("Nenhum imóvel encontrado na página.")
        break
    # Pagina os registro em cadas pagina ate 106 no maximo
    while pagina_tela < 106:
        driver.execute_script("arguments[0].scrollIntoView();", imoveis[-1]) 
        time.sleep(2)  # Espera um pouco para que novos imóveis sejam carregados            
        pagina_tela = pagina_tela + len(imoveis)
        print(f"PAGINANDO REGISTROS: {pagina_tela}")
    # Aqui comecao o loop de busca dos link para adciona no arrei    
    while registro < 106:
        try:
            # Extraindo o link de cada imóvel           
            registro = registro + 1
            cont = cont + 1
            print(f"REGISTRO: {registro}")
            link = driver.find_element(By.XPATH, f'//*[@id="__next"]/main/section/div/form/div[2]/div[4]/div[1]/div/div[{registro}]/div/a')
            links_imoveis.add(link.get_attribute('href'))  # Adicionando o link à lista
            print(f"Link: {link.get_attribute('href')}")
        except Exception:
            print("IMÓVEL EM ANÚNCIO OU LINK NAO ENCONTRADO ")  
    
    print(f"Pagina atual: {pagina_atual}")
                
    # Incrementa o número da página
    if registro == 106 and pagina_atual == 1:
        reg = len(links_imoveis)
        print(f"REGISTROS TOTAIS: {reg}")
        break
    else:
        pagina_atual += 1  
        
    # if pagina_atual == 6:
    # reg=len(links_imoveis)
    # print(f"REGISTROS TOTAIS: {reg}")
    # break


print("CRIANDO A PLANILHDA DO EXCEL.") 
# Criando uma nova planilha Excel e definindo os cabeçalhos
workbook = Workbook()
sheet = workbook.active
sheet.title = "Imóveis"
cabecalhos = ["Título", "Preço", "Condomínio", "IPTU", "Área", "Endereço", "Link"]
sheet.append(cabecalhos)  # Adiciona os cabeçalhos à planilha

# Coletando detalhes de cada imóvel
for link in links_imoveis:
    # Inicializando o ChromeDriver
    service1 = Service(chrome_driver_path)
    driver1 = webdriver.Chrome(service=service1, options=chrome_options)
    driver1.get(link)  # Acessa a página do imóvel
    time.sleep(3)  # Espera a página carregar

    try:
        # Aguardando até que o elemento de preço esteja presente
        preco = WebDriverWait(driver1, 30).until(EC.presence_of_element_located((By.XPATH, '//p[@data-testid="price-info-value"]')))
        if preco.text != "Sob consulta":
            address = WebDriverWait(driver1, 30).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[1]/div[1]/div[1]/div[5]/div[1]/p')))
            condo_fee = WebDriverWait(driver1, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="condo-fee-price"]')))
            if not condo_fee.text:
                condo_fee = "Isento"  # Assinala um valor padrão se vazio
            iptu = WebDriverWait(driver1, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="iptu-price"]')))
            if not iptu.text:
                iptu = "Isento"  # Assinala um valor padrão se vazio
            area = WebDriverWait(driver1, 30).until(EC.presence_of_element_located((By.XPATH, '//span[@data-cy="ldp-propertyFeatures-txt"]')))
            title = WebDriverWait(driver1, 30).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[1]/div[1]/div[2]/section/div[1]/h1')))
        else:
            address = WebDriverWait(driver1, 30).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[1]/div[1]/div[1]/div[5]/div[1]/p')))
            iptu = "Isento"
            condo_fee = "Isento"
            area = WebDriverWait(driver1, 30).until(EC.presence_of_element_located((By.XPATH, '//span[@data-cy="ldp-propertyFeatures-txt"]')))
            title = WebDriverWait(driver1, 30).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[1]/div[1]/div[2]/section/div[1]/h1')))
        
        # Verificando se condo_fee e iptu têm valores
        if isinstance(condo_fee, str):  # Verifica se condo_fee é uma string
            condo_fee = "N/A"  # Assinala um valor padrão se vazio
        else:
            condo_fee = condo_fee.text  # Obtém o texto se for um WebElement

        if isinstance(iptu, str):  # Verifica se iptu é uma string
            iptu = "N/A"  # Assinala um valor padrão se vazio
        else:
            iptu = iptu.text  # Obtém o texto se for um WebElement

        # Imprimindo os detalhes coletados
        print(f"Link: {link}")
        # print(f"Endereço: {address.text}")
        # print(f"Preço: {preco.text}")
        # print(f"Taxa de Condomínio: {condo_fee}")
        # print(f"IPTU: {iptu}")
        # print(f"Área: {area.text}")
        # print(f"Título: {title.text}")
     
        # Adicionando os detalhes à planilha
        sheet.append([title.text, preco.text, condo_fee, iptu, area.text, address.text, link])

    except Exception as e:
        print(f"Erro ao coletar detalhes do imóvel: {e.__traceback__}")

# Criando um DataFrame vazio com os cabeçalhos
df = pd.DataFrame(columns=cabecalhos)

# Salvando o DataFrame em um arquivo Excel
df.to_excel("imoveis.xlsx", index=False)
workbook.save("imoveis.xlsx")

print("Planilha Excel criada com sucesso!")

# Fechando o driver
driver.quit()
