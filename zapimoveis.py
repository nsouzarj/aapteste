from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from openpyxl import Workbook
from funcoes_especificas import get_ceps_por_logradouro,extrair_numeros,encontrar_tipo_imovel,parse_address,remover_parte_texto,extrair_e_formatar_data
from bs4 import BeautifulSoup

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
while pagina_atual >= 1:
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)# Loop principal para as páginas
    registro = 0
    #https://www.zapimoveis.com.br/venda/casas/mg+nova-lima/varanda/?__ab=sup-hl-pl:newC,exp-aa-test:B,super-high:new,off-no-hl:new,TOP-FIXED:card-b,pos-zap:control,new-rec:b,lgpd-ldp:test&transacao=venda&onde=,Minas%20Gerais,Nova%20Lima,,,,,city,BR%3EMinas%20Gerais%3ENULL%3ENova%20Lima,-19.984906,-43.846963,&tipos=casa_residencial&pagina={pagina_atual}&amenities=Varanda/Sacada,Piscina&vagas=4
    # Inicializando o ChromeDriver
  
    # Montando a URL com o número da página atual
    link_nova_lina = f"https://www.zapimoveis.com.br/venda/casas/rj+rio-de-janeiro/4-quartos/?__ab=sup-hl-pl:newC,exp-aa-test:B,super-high:new,off-no-hl:new,TOP-FIXED:card-b,pos-zap:control,new-rec:b,lgpd-ldp:test&transacao=venda&onde=,Rio%20de%20Janeiro,Rio%20de%20Janeiro,,,,,city,BR%3ERio%20de%20Janeiro%3ENULL%3ERio%20de%20Janeiro,-22.906847,-43.172897,&tipos=casa_residencial&pagina={pagina_atual}&amenities=Piscina,Aceita%20pets,Mobiliado,Varanda/Sacada&banheiros=4&quartos=4&vagas=4"
    # url = f"https://www.zapimoveis.com.br/venda/imoveis/rj+rio-de-janeiro/?__ab=sup-hl-pl:newC,exp-aa-test:B,super-high:new,off-no-hl:new,TOP-FIXED:card-b,pos-zap:control,new-rec:b,lgpd-ldp:test&transacao=venda&onde=,Rio%20de%20Janeiro,Rio%20de%20Janeiro,,,,,city,BR%3ERio%20de%20Janeiro%3ENULL%3ERio%20de%20Janeiro,-22.906847,-43.172897,&pagina={pagina_atual}"
    url=link_nova_lina     # Acessando a URL
    #print(f"Acessando a URL: {url}")
    driver.get(url)
    print("COLENTANDO OS LINK DOS IMOvES..")
    print((f"PAGINA ATUAL: {pagina_atual} "))

    ## Espera até que os imóveis estejam carregados
    ## WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/main/section/div/form/div[2]/div[4]/div[1]/div/div[1]/div/a/div/div[1]/div[2]')))
    ## print("Elemento de verificação encontrado. Iniciando a coleta de links.")

    # Seleciona todos os cards de imóveis na página
    imoveis = driver.find_elements(By.XPATH, '//*[@id="__next"]/main/section/div/form/div[2]/div[4]/div[1]/div/div')                                          
    print(f"Número de imóveis encontrados na página: {len(imoveis)}")
    if len(imoveis) ==1:
       print("Final de leiura dos registros.")
       break 
        
         
    
    # Verifica se já coletou todos os imóveis da página atual
    if not imoveis:
        print("Nenhum imóvel encontrado na página.")
        break
    # Pagina os registro em cadas pagina ate 106 no maximo
    a=0
    print(f"PAGINANDO REGISTROS: {pagina_atual}")
    for cont in range(1,  106):  # Limita a 105 registros
        try:
            # Coleta o link e outros dados
            
            link_element = driver.find_elements(By.XPATH, f'//*[@id="__next"]/main/section/div/form/div[2]/div[4]/div[1]/div/div[{cont}]/div/a')
            if link_element:
                link = link_element[0].get_attribute('href')
                links_imoveis.add(link)
                print(f"LINK: {cont} - {link}")
                print(f"CONTADOR:  {len(links_imoveis)}")
                a+=1
                contador_geral+=1;
                if a==10:
                  driver.execute_script("arguments[0].scrollIntoView();", imoveis[-1])  
                  time.sleep(5)  # Espera um pouco para que novos imóveis sejam carregados
                  a=0   
            # ... coleta de outros dados ...
        except Exception as e:
            print(f"Erro ao encontrar o link para o elemento")
            continue  # Continua para o próximo registro

    pagina_atual += 1                  

# Mostra os registros catalogados no  link_imoveis
print("CRIANDO A PLANILHDA DO EXCEL.") 
print(f"TOTAL DE REGISTRS COLETADOS: {len(links_imoveis)}")


# Criando uma nova planilha Excel e definindo os cabeçalhos
workbook = Workbook()
sheet = workbook.active
sheet.title = "Imóveis"
cabecalhos = ["data_inclusao", "tipo_imovel", "cep_endereco", "logradouro_endereco", "numero_endereço", "bairro_endereco", "uf_endereco","cidade_endereco","dormitorios",
              "suites","vagas","area_util","vlr_venda","vlr_aluguel","vlr_condominio","vlr_iptu","anunciante","link","codigo_imovel"]
sheet.append(cabecalhos)  # Adiciona os cabeçalhos à planilha

""" Isso e para teste de um link especifico descomente aqui """
# links_imoveis.add("https://www.zapimoveis.com.br/imovel/venda-casa-de-condominio-4-quartos-com-piscina-estancia-serrana-nova-lima-mg-851m2-id-2705427697/")
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
            EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[1]/div[1]/div[1]/div[4]/div/div/div'))
        )
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
        # Aqui adicona na planilha crianda
        sheet.append([data_cadastro,tipo_movel,cepencontado, logradouro, numero,bairro,estado,cidade, num_dormitorios ,num_suites ,num_vagas ,area_total,valor_venda_limpo,valor_aluguel_limpo, condo_fee, iptu,anunciante_do_imovel.text,link, parte_zap])
        registro_atual += 1

        # Salva a planilha a cada 50 registros
        if registro_atual % 50 == 0:
            #workbook.save(os.path.join("C:", "Users", "User", "Documents", "zapimoveis", "listadeimoveis.xlsx"))
            output_dir = "C:\\Users\\User\\Documents\\zapimoveis"  # Adjust this if needed
            os.makedirs(output_dir, exist_ok=True)  # Create the directory if it doesn't exist
            workbook.save(os.path.join(output_dir, "listadeimoveis.xlsx")) 
            print(f"##  PLANILHA SALVA (Registro {registro_atual}) ##")
            registro_atual=0
    except Exception as e:
        print(f"ERROR: Na coleta detalhes do imóvel: {e}  ---> {link}" )
       
# Salva a planilha final (novamente, para garantir que todos os dados estão salvos)
output_dir = "C:\\Users\\User\\Documents\\zapimoveis"  # Adjust this if needed
os.makedirs(output_dir, exist_ok=True)  # Create the directory if it doesn't existbook.save(os.path.join(output_dir, "listadeimoveis.xlsx")) 
workbook.save(os.path.join(output_dir, "listadeimoveis.xlsx")) 
print("Planilha Excel criada com sucesso!")

# Fechando o driver
driver.quit()