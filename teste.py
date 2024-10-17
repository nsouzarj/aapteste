from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from openpyxl import Workbook
import pandas as pd
import re
import locale
from datetime import datetime

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

""" Rerona o tipo do imovel"""
def encontrar_tipo_imovel(descricao, tipos_imoveis):
    for indice, tipo in enumerate(tipos_imoveis):
        if tipo.lower() in descricao.lower():  # Ignora maiúsculas/minúsculas
            return tipo  # Retorna o tipo encontrado
    return None  


""" Esta funcao trata a localizacao do imovel separando por partes"""
def separar_endereco(endereco):
    # Usando expressões regulares para separar os componentes do endereço
    padrao = r'^(.*?)(?:,\s*(\d+))?\s*-\s*(.*?),\s*(.*?)-\s*(\w{2})$'
    resultado = re.match(padrao, endereco)

    if resultado:
        logradouro = resultado.group(1).strip()
        numero = resultado.group(2) if resultado.group(2) else None  # Se não houver número, retorna None
        bairro = resultado.group(3).strip()
        cidade = resultado.group(4).strip()
        estado = resultado.group(5).strip()
        
        # Retornando cada parte do endereço
        yield logradouro
        yield numero
        yield bairro
        yield cidade
        yield estado
    else:
        yield None 
        
#Funcao que moreov parte do texto 
def remover_parte_texto(texto, parte_a_remover):
    """Remove a parte especificada da string e retorna o restante."""
    return texto.replace(parte_a_remover, "").strip()   

# Formata data em extendo
def extrair_e_formatar_data(texto):
    # Definindo a localidade para português
    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')  # Pode ser necessário ajustar dependendo do sistema

    # Usando expressão regular para encontrar a data no formato "26 de junho de 2024"
    padrao = r'(\d{1,2} de \w+ de \d{4})'
    resultado = re.search(padrao, texto)

    if resultado:
        # Extraindo a data encontrada
        data_str = resultado.group(1)
        # Convertendo a data para o formato desejado
        data_formatada = datetime.strptime(data_str, '%d de %B de %Y').strftime('%d/%m/%Y')
        return data_formatada
    else:
        return None  # Retorna None se não encontrar a data
     

# Coletando links dos imóveis
while pagina_atual >= 1:  # Loop principal para as páginas
    registro = 0
    #https://www.zapimoveis.com.br/venda/casas/mg+nova-lima/varanda/?__ab=sup-hl-pl:newC,exp-aa-test:B,super-high:new,off-no-hl:new,TOP-FIXED:card-b,pos-zap:control,new-rec:b,lgpd-ldp:test&transacao=venda&onde=,Minas%20Gerais,Nova%20Lima,,,,,city,BR%3EMinas%20Gerais%3ENULL%3ENova%20Lima,-19.984906,-43.846963,&tipos=casa_residencial&pagina={pagina_atual}&amenities=Varanda/Sacada,Piscina&vagas=4
    # Inicializando o ChromeDriver
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    # Montando a URL com o número da página atual
    link_nova_lina = f"https://www.zapimoveis.com.br/venda/casas/mg+nova-lima/varanda/?__ab=sup-hl-pl:newC,exp-aa-test:B,super-high:new,off-no-hl:new,TOP-FIXED:card-b,pos-zap:control,new-rec:b,lgpd-ldp:test&transacao=venda&onde=,Minas%20Gerais,Nova%20Lima,,,,,city,BR%3EMinas%20Gerais%3ENULL%3ENova%20Lima,-19.984906,-43.846963,&tipos=casa_residencial&pagina={pagina_atual}&amenities=Varanda/Sacada,Piscina&vagas=4"
    # url = f"https://www.zapimoveis.com.br/venda/imoveis/rj+rio-de-janeiro/?__ab=sup-hl-pl:newC,exp-aa-test:B,super-high:new,off-no-hl:new,TOP-FIXED:card-b,pos-zap:control,new-rec:b,lgpd-ldp:test&transacao=venda&onde=,Rio%20de%20Janeiro,Rio%20de%20Janeiro,,,,,city,BR%3ERio%20de%20Janeiro%3ENULL%3ERio%20de%20Janeiro,-22.906847,-43.172897,&pagina={pagina_atual}"
    url=link_nova_lina     # Acessando a URL
    print(f"Acessando a URL: {url}")
    driver.get(url)
    print((f" PAGINA ATUAL: {pagina_atual} "))

    # Espera até que os imóveis estejam carregados
   ## WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/main/section/div/form/div[2]/div[4]/div[1]/div/div[1]/div/a/div/div[1]/div[2]')))
   ## print("Elemento de verificação encontrado. Iniciando a coleta de links.")

    # Seleciona todos os cards de imóveis na página
    imoveis = driver.find_elements(By.XPATH, '//*[@id="__next"]/main/section/div/form/div[2]/div[4]/div[1]/div/div') 
                                             
    print(f"Número de imóveis encontrados na página: {len(imoveis)}")  
    
    # Verifica se já coletou todos os imóveis da página atual
    if not imoveis:
        print("Nenhum imóvel encontrado na página.")
        break
    # Pagina os registro em cadas pagina ate 106 no maximo
    a=0
    print(f"PAGINANDO REGISTROS: {pagina_atual}")
      
    for i in range(1, 106):  # Começa de 1 e vai até 105
        cont = i  # Agora cont começa de 1
        
        try:
            # Tenta encontrar o botão
            try:
                botao = WebDriverWait(driver, 8).until(
                    EC.presence_of_element_located((By.XPATH, f'//*[@id="__next"]/main/section/div/form/div[2]/div[4]/div[1]/div/div[{cont}]/div/div/div/div[1]/div[2]/div[2]/div[2]/button'))
                )
            except Exception:
                print(f"Elemento não encontrado, coletando link mesmo assim.")   
            
            # Verifica se o elemento do link existe antes de tentar acessá-lo
            link_element = driver.find_elements(By.XPATH, f'//*[@id="__next"]/main/section/div/form/div[2]/div[4]/div[1]/div/div[{cont}]/div/a')
            if link_element:  # Se o elemento foi encontrado
                link = link_element[0]
                links_imoveis.add(link.get_attribute('href')) 
                print(f"LINK: {i} - {link.get_attribute('href')}")
            else:
                print(f"Link não encontrado para o elemento {cont}.")
                continue  # Pula para a próxima iteração se o link não for encontrado

            valor = driver.find_element(By.XPATH, f'//*[@id="__next"]/main/section/div/form/div[2]/div[4]/div[1]/div/div[{cont}]/div/a/div/div[1]/div[2]/div[2]/div[1]/p[1]') 
            descricao = driver.find_element(By.XPATH, f'//*[@id="__next"]/main/section/div/form/div[2]/div[4]/div[1]/div/div[{cont}]/div/a/div/div[1]/div[2]/div[1]/h2/span[1]') 
            print(f"VALOR: {valor.text} ")
            a += 1
            driver.execute_script("arguments[0].scrollIntoView();", imoveis[-1])
            time.sleep(2)
            pagina_tela += len(imoveis)

            # Verifica se já coletou 105 registros para rolar a página
            if a == 105:
                print("Coletou 105 registros, passando para a próxima página.")
                pagina_atual += 1  # Incrementa o número da página
                break  # Sai do loop para reiniciar a coleta na nova página

        except Exception as e:
            print(f"Erro ao encontrar o link para o elemento {cont}: {e}")
            break                  

print("CRIANDO A PLANILHDA DO EXCEL.") 
# Criando uma nova planilha Excel e definindo os cabeçalhos
workbook = Workbook()
sheet = workbook.active
sheet.title = "Imóveis"
cabecalhos = ["data_inclusao", "tipo_imovel", "cep_endereco", "logradouro_endereco", "numero_endereço", "bairro_endereco", "uf_endereco","cidade_endereco","dormitorios",
              "suites","vagas","area_util","vlr_venda","vlr_aluguel","vlr_condominio","vlr_iptu","anunciante","link","codigo_imovel"]
sheet.append(cabecalhos)  # Adiciona os cabeçalhos à planilha

# Coletando detalhes de cada imóvel
for link in links_imoveis:
    # Inicializando o ChromeDriver
    service1 = Service(chrome_driver_path)
    driver1 = webdriver.Chrome(service=service1, options=chrome_options)
    driver1.get(link)  # Acessa a página do imóvel
    time.sleep(3)  # Espera a página carregar

    try:
        
        address = WebDriverWait(driver1, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[1]/div[1]/div[1]/div[5]/div[1]/p')))
        area = WebDriverWait(driver1, 10).until(EC.presence_of_element_located((By.XPATH, '//span[@data-cy="ldp-propertyFeatures-txt"]')))
        title = WebDriverWait(driver1, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[1]/div[1]/div[2]/section/div[1]/h1')))
     
        # PEga tipo de valor "vnda" "aliguel"
        tipo_valor=WebDriverWait(driver1, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="business-type-info"]')))   
        if tipo_valor.text == "Venda":
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
                   iptu = "Isento"  # Assinala um valor padrão se vazio
               
               
                if isinstance(condo_fee, str):  # Verifica se condo_fee é uma string
                    condo_fee = "Não foi possível recuperar"  # Assinala um valor padrão se vazio
                else:
                    condo_fee = condo_fee.text  # Obtém o texto se for um WebElement
             
                if isinstance(iptu, str):  # Verifica se iptu é uma string
                    iptu = "Não foi possível recuperar"  # Assinala um valor padrão se vazio
                else:
                    iptu = iptu.text    
            
        elif tipo_valor.text == "Aluguel":
            valor_aluguel = WebDriverWait(driver1, 10).until(EC.presence_of_element_located((By.XPATH, ' /html/body/div[2]/div[1]/div[1]/div[1]/div[3]/div/div[1]/div[1]/p[2]')))
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
        
        # Traz a data em extendo e trasnforma em formato MM/DD/YYYy
        data_extenso = WebDriverWait(driver1, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[1]/div[1]/div[2]/section/div[4]/span[2]')))  
        data_cadastro = extrair_e_formatar_data(data_extenso.text)
        area_num = remover_parte_texto(area.text, "m²")
        # Click the button at the specified XPath
      
        button = WebDriverWait(driver1, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[1]/div[1]/div[2]/section/div[3]/button')))
        button.click()  
        # Traz o anunciante do imovel 
        anunciante_do_imovel = WebDriverWait(driver1, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/div[2]/div/section/section/div[1]/div/p[1]')))
        # Zap 
        zap_do_anunciante = WebDriverWait(driver1, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/div[2]/div/section/section/div[2]/p[3]')))
        # Imprime na tela o link         
        
        logradouro, numero, bairro, cidade, estado = separar_endereco(address.text)
        tipo_movel=encontrar_tipo_imovel(title.text,tipos_imoveis)
        parte_zap = remover_parte_texto(zap_do_anunciante.text, "No Zap: ")
    
        time.sleep(2) 
        # Aqui adicona na planilha crianda
        sheet.append([data_cadastro,tipo_movel,"cep", logradouro, numero,bairro,estado,cidade, "00","00","00",area_num,valor_venda_limpo,valor_aluguel_limpo, condo_fee, iptu,anunciante_do_imovel.text,link, parte_zap])
    except Exception as e:
        print(f"Erro ao coletar detalhes do imóvel: {e}")

# Criando um DataFrame vazio com os cabeçalhos
df = pd.DataFrame(columns=cabecalhos)
# Salvando o DataFrame em um arquivo Excel
df.to_excel("imoveis.xlsx", index=False)
workbook.save("imoveis.xlsx")
print("Planilha Excel criada com sucesso!")
# Fechando o driver
driver.quit()
