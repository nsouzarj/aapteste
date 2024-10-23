from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
import sys
from openpyxl import Workbook
from funcoes_especificas import get_ceps_por_logradouro,extrair_numeros,encontrar_tipo_imovel,parse_address,remover_parte_texto,extrair_e_formatar_data,separar_precos
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import requests_cache
import requests

requests_cache.install_cache('cache')


# Caminho da planilha
caminho_da_planilha = sys.argv[1]

# Caminho do webchorme 
caminho_do_webchrome = sys.argv[2]

#filtro pro cidade
caminho_do_filtro=sys.argv[3]

#tipo de filtro pode ser venda 
tipo_de_filtro=sys.argv[4]

# Configurando opções do Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")  # Comente esta linha para ver o navegador
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")  # Desativa a aceleração de hardware
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
requests_cache.install_cache('cache')
# Inicializando o ChromeDriver
# Caminho para o ChromeDriver
chrome_driver_path = caminho_do_webchrome
#"C:\Users\User\ChromeWithDriver\chromedriver.exe"
# Configurar o cache (use 'cache' como nome do arquivo do cache)

service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options= chrome_options)


# Inicializando um conjunto para armazenar links únicos
links_imoveis = set()
# Número da página inicial
pagina_atual = 1
cont = 0 
# PAgina por scrol de tela
pagina_tela = 0
contador_geral = 1;


""" Array que contem os tipso de movel """
tipos_imoveis = [
    "Apartamento",
    "Studio",
    "Kitnet",
    "Casa",
    "Sobrado",
    "Casa de Condomínio",
    "Casa de Vila",
    "Cobertura",
    "Flat",
    "Loft",
    "Terreno / Lote / Condomínio",
    "Fazenda / Sítio / Chácara",
    "Loja / Salão / Ponto Comercial",
    "Conjunto Comercial / Sala",
    "Casa Comercial",
    "Hotel / Motel / Pousada",
    "Andar / Laje Corporativa",
    "Prédio Inteiro",
    "Terrenos / Lotes Comerciais",
    "Galpão / Depósito / Armazém",
    "Garagem"
]

# Formata data em extendo
  # Retorna None se não encontrar a data


# Coletando links dos imóveis
"""  Comente esse treco do while ate o final caso queira testar um único link do imóvel """

service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)# Loop principal para as páginas
registro = 0
#actions.move_to_eleme


# nt(drawer)  # Move the mouse to the drawer initiall
# Loop para navegar pelas páginas
try:
    while pagina_atual >= 1:
        # Montando a URL com o número da página atual
        link_nova_lina = caminho_do_filtro + str(pagina_atual)
        url = link_nova_lina
        
        # Acessando a URL (usando requests_cache)
        response =  requests.get(url)  # Faz a requisição usando requests_cache
        if response.from_cache:
            print(f"Carregando página {pagina_atual} do cache.")
        else:
            print(f"Baixando página {pagina_atual}.")

        # O resto do seu código (dentro do loop) continua exatamente igual:
        driver.maximize_window()
        driver.get(url)
        actions = ActionChains(driver)

        print("COLENTANDO OS LINK DOS IMOvES..")
        print((f"PAGINA ATUAL: {pagina_atual} "))

        # Espera até que os imóveis estejam carregados
        # WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/main/section/div/form/div[2]/div[4]/div[1]/div/div[1]/div/a/div/div[1]/div[2]')))
        # print("Elemento de verificação encontrado. Iniciando a coleta de links.")

        # Seleciona todos os cards de imóveis na página
        imoveis = driver.find_elements(By.XPATH, '//*[@id="__next"]/main/section/div/form/div[2]/div[4]/div[1]/div/div')
        print(f"Número de imóveis encontrados na página: {len(imoveis)}")

        # Verifica se já coletou todos os imóveis da página atual
        if len(imoveis) == 1:
            print("Final de leitura dos registros.")
            break 

        # Pagina os registro em cadas pagina ate 106 no maximo
        a = 0
        print(f"PAGINANDO REGISTROS: {pagina_atual}")
        driver.maximize_window()
        actions = ActionChains(driver)
        # Loop para iterar pelos elementos de imóvel
        for cont in range(1, 150):  # Limita a 105 registros
            try:
                # Coleta o link e outros dados
                a += 1
                   
                link_element = driver.find_elements(By.XPATH, f'//*[@id="__next"]/main/section/div/form/div[2]/div[4]/div[1]/div/div[{cont}]/div/a')
                  
                botao_anuncio = driver.find_elements(By.XPATH, f'//*[@id="__next"]/main/section/div/form/div[2]/div[4]/div[1]/div/div[{cont}]/div/div/div/div/div[2]/div[3]/div[2]/button')   
               
                botao_menssagen = driver.find_elements(By.XPATH, f'//*[@id="__next"]/main/section/div/form/div[2]/div[4]/div[1]/div/div[{cont}]/div/a/div/div/div[2]/div[3]/div[2]/div[1]/button[2]')  
 
                if botao_anuncio and len(botao_anuncio) > 0 and len(botao_menssagen)==0: 
                    # Encontra o botão clicável usando WebDriverWait
                    button1 = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="__next"]/main/section/div/form/div[2]/div[4]/div[1]/div/div[{cont}]/div/div/div/div/div[2]/div[3]/div[2]/button')))
                    texto = button1.text
                    
                    # Clica no botão de anúncio
                    try:
                       driver.implicitly_wait(5) 
                       driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE) # Fechando o anúnci
                       button1.click()
                       time.sleep(5)
                    except:
                       botao_anuncio[0].click()
      
                    link_imovel = driver.find_elements(By.XPATH, '//*[@id="__next"]/main/section/aside/form/section/div/section[2]/section/div[5]/div[1]/a') # Ajuste o tempo de espera conforme necessário

      
                    if link_imovel:
                        link_result = link_imovel[0].get_attribute('href')
                        print("IMOVEL COM ANÚNCIO")
                        print(f"{cont} - {link_result}")
                        links_imoveis.add(link_result)
                        
                        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE) # Fechando o anúncio
                        time.sleep(4)

                # Coleta o link do imóvel (se não houver anúncio)
                if link_element and len(link_element) > 0 and len(botao_menssagen) > 0:
                    link = link_element[0].get_attribute('href')
                    links_imoveis.add(link)
                    print(f"LINK: {cont} - {link}")

                # Rola a página para carregar mais imóveis
                if a == 14:
                    driver.execute_script("arguments[0].scrollIntoView();", imoveis[-1])
                    time.sleep(2)  # Ajuste o tempo de espera conforme necessário
                    a = 0
                    # Não use 'continue' aqui, pois ele está fora do bloco 'try'

            except Exception as e:  # Captura qualquer exceção
                #print(f"ERRO: {e}")
                continue  # Continua para a próxima iteração do loop
            
            # Continua para o próximo registro
        pagina_atual=+1
                



except Exception as e:
    print(f"ERRO GERAL: {e}")
    driver.quit()
finally:
    print("Finalizando a coleta de dados.")
    print(f"Total de imóveis coletados: {contador_geral}")
    driver.quit()
    
                 

# Mostra os registros catalogados no  link_imoveis
print("CRIANDO A PLANILHDA DO EXCEL.") 
print(f"TOTAL DE REGISTRS COLETADOS: {len(links_imoveis)}")

# Criando uma nova planilha Excel e definindo os cabeçalhos
#Seta o diretorio onde será salvao a planilha
output_dir = caminho_da_planilha
workbook = Workbook()
sheet = workbook.active
sheet.title = "Imóveis"
cabecalhos = ["data_inclusao", "tipo_imovel", "cep_endereco", "logradouro_endereco", "numero_endereço", "bairro_endereco", "uf_endereco","cidade_endereco","dormitorios",
              "suites","vagas","area_util","vlr_venda","vlr_aluguel","vlr_condominio","vlr_iptu","anunciante","link","codigo_imovel"]
sheet.append(cabecalhos)  # Adiciona os cabeçalhos à planilha

""" Isso e para teste de um link especifico descomente aqui """
#links_imoveis.add("https://www.zapimoveis.cm.br/imovel/venda-sobrados-4-quartos-com-piscina-sao-lourenco-bertioga-sp-150m2-id-2746700743/")
# Coletando detalhes de cada imóvel
registro_atual = 0
for link in links_imoveis:
    # Inicializando o ChromeDriver
    service1 = Service(chrome_driver_path)
    driver1 = webdriver.Chrome(service=service1, options=chrome_options)
    try:
      wait = WebDriverWait(driver1, 5)
      driver1.get(link) # Acessa a página do imóvel
      print(f"LINK - {link}")
    except Exception as e:
      print(f"ERROR: Na leirura do endereço ---> {e} ---> {link}")
      break
    
    try:
        
        address = WebDriverWait(driver1, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[1]/div[1]/div[1]/div[5]/div[1]/p')))
        items_lista=WebDriverWait(driver1, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[1]/div[1]/div[1]/div[4]/div/div/div')))
       # Aguarda a presença do elemento com o XPath
        """ Traz os items para ser tartado"""
        items_lista = WebDriverWait(driver1, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[1]/div[1]/div[1]'))
                                                      
        )
        # Traz os valores do imovel
        precos_imovel = WebDriverWait(driver1, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[1]/div[1]/div[1]/div[3]/div[1]'))
                                                      
        )
        preco=""
        if precos_imovel:
               precos_imovel
               preco= separar_precos(precos_imovel.text)
                    
        # Converte o elemento Selenium para um objeto lxml.html.HtmlElement
        html_content = items_lista.get_attribute('outerHTML')
       
        soup = BeautifulSoup(html_content, 'html.parser')       
        # Extraindo as informações
        amenity_items = soup.find_all('p', class_='amenities-item')
 
        amenities_data = {}
        # Itera a lista
        # Setar oo avlores default
        area_total=""
        num_dormitorios=""
        num_suites=""
        num_vagas=""
        #  Faz a busca bo objeto
        for item in amenity_items:
          property_name = item.get('itemprop')
     
          if property_name=='floorSize':
             property_value = item.find('span', class_='amenities-item-text').text.strip()    
             area_total = extrair_numeros(property_value)   
    
          if property_name=='numberOfRooms':
             property_value = item.find('span', class_='amenities-item-text').text.strip()        
             num_dormitorios = extrair_numeros(property_value) 

          if property_name=='numberOfSuites':
             property_value = item.find('span', class_='amenities-item-text').text.strip()        
             num_suites = extrair_numeros(property_value) 
               
          if property_name=='numberOfParkingSpaces':
             property_value = item.find('span', class_='amenities-item-text').text.strip()        
             num_vagas = extrair_numeros(property_value)           
   
        title = WebDriverWait(driver1, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[1]/div[1]/div[2]/section/div[1]/h1')))
     
     
        # PEga tipo de valor "vnda" "aliguel"
        tipo_valor_venda=WebDriverWait(driver1, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="business-type-info"]')))   
        if tipo_valor_venda.text == "Venda":
            valor_venda = WebDriverWait(driver1, 10).until(EC.presence_of_element_located((By.XPATH, '//p[@data-testid="price-info-value"]')))    
            valor_venda_limpo=valor_venda.text;
            valor_aluguel_limpo=""
            #valor_venda = WebDriverWait(driver1, 10).until(EC.presence_of_element_located((By.XPATH, ' /html/body/div[2]/div[1]/div[1]/div[1]/div[3]/div/div[1]/div[1]/p[2]')))
            if valor_venda.text != "Sob consulta":
           
                condo_fee = WebDriverWait(driver1, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="condo-fee-price"]')))
                if not condo_fee.text:
                   condo_fee = "Isento"  # Assinala um valor padrão se vazio
                iptu = WebDriverWait(driver1, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="iptu-price"]')))
                if not iptu.text:
                   iptu = "Isento"  # Assinala um valor padrão se vazi  
               
                if isinstance(condo_fee, str):  # Verifica se condo_fee é uma string
                    condo_fee = "Não foi possível recuperar"  # Assinala um valor padrão se vazio
                else:
                    condo_fee = condo_fee.text  # Obtém o texto se for um WebElement
             
                if isinstance(iptu, str):  # Verifica se iptu é uma string
                    iptu = "Não foi possível recuperar"  # Assinala um valor padrão se vazio
                else:
                    iptu = iptu.text 
                    
        elif tipo_valor_venda.text == "Aluguel":
                                                                                                       
            valor_aluguel = WebDriverWait(driver1, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[1]/div[1]/div[1]/div[3]/div/div[1]/div[1]/p[2]')))
            valor_aluguel_limpo=valor_aluguel.text
            valor_venda_limpo=""
            
            condo_fee = WebDriverWait(driver1, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="condo-fee-price"]')))
            if not condo_fee.text:
               condo_fee = "Isento"  # Assinala um valor padrão se vazio
            
            iptu = WebDriverWait(driver1, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="iptu-price"]')))
            if not iptu.text:
               iptu = "Isento"  # Assinala um valor padrão se vazio
            
            
            if isinstance(condo_fee, str):  # Verifica se condo_fee é uma string
               condo_fee = "Não foi possível recuperar"  # Assinala um valor padrão se vazio
            else:
               condo_fee = condo_fee.text  # Obtém o texto se for um WebElement
             
            if isinstance(iptu, str):  # Verifica se iptu é uma string
               iptu = "Não foi possível recuperar"  # Assinala um valor padrão se vazio
            else:
               iptu = iptu.text   
        
            area_valores=   WebDriverWait(driver1, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[1]/div[1]/div[1]/div[3]/div[1]/div[1]')))
            if not area_valores.text:
                print("Nao existe")
                
        # Traz a data em extendo e trasnforma em formato MM/DD/YYYy
        data_extenso = WebDriverWait(driver1, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[1]/div[1]/div[2]/section/div[4]/span[2]')))  
        data_cadastro = extrair_e_formatar_data(data_extenso.text)
        #area_num = remover_parte_texto(area.text, "m²")
        # Click the button at the specified XPath
        button = WebDriverWait(driver1, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[1]/div[1]/div[2]/section/div[3]/button')))
        button.click()  
        # Traz o anunciante do imovel 
        anunciante_do_imovel = WebDriverWait(driver1, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/div[2]/div/section/section/div[1]/div/p[1]')))
        # Zap 
        zap_do_anunciante = WebDriverWait(driver1, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/div[2]/div/section/section/div[2]/p[3]')))
        # Imprime na tela o link   
        logradouro, numero, bairro, cidade, estado = parse_address(address.text)
           
        # Traz o cep dplogradouro
        cep = get_ceps_por_logradouro(logradouro, numero, cidade, estado)
        if cep:
           cepencontado= cep['cep']
        else:
           cepencontado="Nao encontrado"
        tipo_movel=encontrar_tipo_imovel(title.text,tipos_imoveis)
        parte_zap = remover_parte_texto(zap_do_anunciante.text, "No Zap: ")
    
        time.sleep(2) 
        if tipo_de_filtro=="venda":
               
            precovenda=preco['Venda']  
            sheet.append([data_cadastro,tipo_movel,cepencontado, logradouro, numero,bairro,estado,cidade, num_dormitorios ,num_suites ,num_vagas ,area_total,precovenda,"", condo_fee, iptu,anunciante_do_imovel.text,link, parte_zap])
        elif  tipo_de_filtro=="aluguel":
            precoaluguel=preco['Aluguel']  
            sheet.append([data_cadastro,tipo_movel,cepencontado, logradouro, numero,bairro,estado,cidade, num_dormitorios ,num_suites ,num_vagas ,area_total,"",precoaluguel, condo_fee, iptu,anunciante_do_imovel.text,link, parte_zap])   
               
    
        
        registro_atual += 1

        # Salva a planilha a cada 50 registros
        if registro_atual % 50 == 0:
            #workbook.save(os.path.join("C:", "Users", "User", "Documents", "zapimoveis", "listadeimoveis.xlsx"))
            os.makedirs(output_dir, exist_ok=True)  # Create the directory if it doesn't exist
            workbook.save(os.path.join(output_dir, "listadeimoveis.xlsx")) 
            print(f"##  PLANILHA SALVA (Registro {registro_atual}) ##")
            registro_atual=0
    except Exception as e:
        print(f"ERROR: Na coleta detalhes do imóvel: {e}  ---> {link}" )
       
 # Adjust this if needed
os.makedirs(output_dir, exist_ok=True)  # Create the directory if it doesn't existbook.save(os.path.join(output_dir, "listadeimoveis.xlsx")) 
workbook.save(os.path.join(output_dir, "listadeimoveis.xlsx")) 
print("Planilha Excel criada com sucesso!")
# Fechando o driver
driver.quit()
print("FINALIZADO COM SUCESSO..")
time.sleep(10)
sys.exit()