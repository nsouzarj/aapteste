import requests
import re
import time

""" Traz cep do logradouro da api  https://viacep.com.br/ """
def get_ceps_por_logradouro(logradouro, numero=None, cidade=None, estado=None):
  
  # Faz a requisição à API do ViaCEP
  url = f"https://viacep.com.br/ws/{estado}/{cidade}/{logradouro}/json/"
  response = requests.get(url)
  time.sleep(5)

  # Verifica se a requisição foi bem-sucedida
  if response.status_code == 200:
    # Carrega os dados da resposta em JSON
    ceps = response.json()

    # Se houver mais de um CEP e o número for fornecido, encontra o mais próximo
    if isinstance(ceps, list):
      if numero == "inexistente":
        # Se o número é "Inexistente", retorna o primeiro CEP da lista
        return ceps[0] if ceps else None
      elif numero:
        # Se o número é um inteiro, encontra o CEP mais próximo
        cep_mais_proximo = encontrar_cep_mais_proximo(ceps, int(numero))
        return cep_mais_proximo
    else:
      # Se não houver número ou só houver um CEP, retorna o primeiro da lista
      return ceps 
  else:
    return None
# Pega o cep mais proximo

""" Econtra o cepo mais proximo da api """
def encontrar_cep_mais_proximo(ceps, numero):


  cep_mais_proximo = None
  menor_diferenca = float('inf')

  for cep in ceps:
    # Verifica se o número está presente e converte para inteiro
    numero_cep = cep.get('numero') 
    if numero_cep:
      try:
        numero_cep_int = int(numero_cep)
      except ValueError:
        continue  # Ignora se o número não for um inteiro
    else:
      numero_cep_int = -1
    
    # Calcula a diferença absoluta entre o número fornecido e o número do CEP
    diferenca = abs(numero - numero_cep_int)

    # Atualiza o CEP mais próximo se a diferença for menor
    if diferenca < menor_diferenca:
      menor_diferenca = diferenca
      cep_mais_proximo = cep

  return cep_mais_proximo


""" Extrai o numeod do texto """

def extrair_numeros(frase):

    partes = frase.split()
    numeros = []
    for parte in partes:
        if parte.isdigit() or '-' in parte: # Inclui partes com hífen 
          numeros.extend(parte.split('-')) # Separa partes com hífen em números individuais
        if numeros:
          return '-'.join(numeros)    
        else:
          return ""



""" Retorna o tipo do imovel"""
def encontrar_tipo_imovel(descricao, tipos_imoveis):
    for indice, tipo in enumerate(tipos_imoveis):
        if tipo.lower() in descricao.lower():  # Ignora maiúsculas/minúsculas
            return tipo  # Retorna o tipo encontrado
    return None 
 

"""Esta função trata a localização do imóvel separando por partes"""
def parse_address(address):
  
    # Substitui o hífen por uma vírgula para facilitar a separação
    # Encontra a posição da ","
    indice_virgula = address.find(",")
    indice_traco =address.find("-")
    
    num_virgula= address.count(",")
    num_traco=address.count("-")
    
    if num_virgula==2 and num_traco==2:
        address=address.replace("-", ",")
        endereco_modificado=address   
    
    if num_virgula==1 and num_traco==2:
        address=address.replace("-", ",")
        endereco_modificado=address 
    
    if num_virgula==1 and num_traco==1:
        address=address.replace("-", ",")
        endereco_modificado=address 
        
    if num_virgula==1 and num_traco==3:
     #  partes = address.split("-")
       endereco_modificado = re.sub(r' - ', ',', address)
       
    if num_virgula==1 and num_traco==4:
     #  partes = address.split("-")
       endereco_modificado = re.sub(r' - ', ',', address)   
      
    #endereco_modificado = address[:indice_virgula+1] + address[indice_virgula+1:].replace(",", ",")
    #endereco_modificado = address[:indice_virgula+2:] + address[indice_virgula+1:].replace("-", ",")
    #endereco_modificado = endereco_modificado[:indice_virgula+1] + endereco_modificado[indice_virgula+1:].replace(" - ", ",")
    #endereco_modificado = endereco_modificado[:indice_virgula+1] + endereco_modificado[indice_virgula+1:].replace(" ,", ",")  
    # Verifica se o endereço tem o padrão específico
    
    # Regex pattern para capturar os componentes do endereço
    # Tenta fazer o match do endereço com o padrão
    pattern="^(?P<logradouro>[^,]+),?\\s*(?P<numero>\\d*)?\\s*,?\\s*(?P<bairro>[^,]*)?,?\\s*(?P<cidade>[^,]+?)\\s*,\\s*(?P<estado>[A-Z]{2})$"
    
    try:
        match = re.match(pattern, endereco_modificado.strip())
        # Trata o match
        if match:
            logradouro = match.group("logradouro").strip() if match.group("logradouro") else "inexistente"
            numero = match.group("numero").strip() if match.group("numero") else "inexistente"
            bairro = match.group("bairro").strip() if match.group("bairro") else "inexistente"
            cidade = match.group("cidade").strip() if match.group("cidade") else "inexistente"
            estado = match.group("estado").strip() if match.group("estado") else "inexistente"
            if cidade=="":
               cidade = bairro
               bairro="inexistente"  
            # Retorna como uma tupla
            return (logradouro, numero, bairro, cidade, estado)
        else:
            return ("inexistente", "inexistente", "inexistente", "inexistente", "inexistente") 
    except Exception as e:
        print(f"Erro ao analisar o endereço não est ano formato correto: {e}")
        return ("inexistente", "inexistente", "inexistente", "inexistente", "inexistente") 
      
# Como usar & tipo de endereços     # 
# logradouro, numero, bairro, cidade, estado = parse_address("Rua Toledo - Vila Castela , Nova Lima - MG")
# AQUI SAO OS TIPOS DE ENDEREÇO como exemplo
# Rua Gama, 116 - Condominio Quintas do Sol, Nova Lima - MG
# Rua dos Beija-Flores - Alphaville Lagoa Dos Ingleses, Nova Lima - MG
# Rua dos Jatobás - Alphaville Lagoa Dos Ingleses, Nova Lima - MG
# Vila del Rey, Nova Lima - MG
# Rua dos Bem-Te-Vis - Alphaville Lagoa Dos Ingleses, Nova Lima - MG
# Rua Bem-Te-Vi, 1 - Vila del Rey, Nova Lima - MG
# Rua Estrela da Manhã, 225 - Vale dos Cristais, Nova Lima - MG
      
      
""" Funcao que remove a parte do texto """ 
def remover_parte_texto(texto, parte_a_remover):
    """Remove a parte especificada da string e retorna o restante."""
    return texto.replace(parte_a_remover, "").strip()  
  
  
""" Extrai a data do formato extesno """  
def extrair_e_formatar_data(texto):
    # Dicionário para mapear meses em português para números
    meses = {
        'janeiro': 1,
        'fevereiro': 2,
        'março': 3,
        'abril': 4,
        'maio': 5,
        'junho': 6,
        'julho': 7,
        'agosto': 8,
        'setembro': 9,
        'outubro': 10,
        'novembro': 11,
        'dezembro': 12,
        'jan': 1,
        'fev': 2,
        'mar': 3,
        'abr': 4,
        'mai': 5,
        'jun': 6,
        'jul': 7,
        'ago': 8,
        'set': 9,
        'out': 10,
        'nov': 11,
        'dez': 12,
    }

    # Usando expressão regular para encontrar a data no formato "26 de junho de 2024"
    padrao = r'(\d{1,2}) de (\w+) de (\d{4})'
    resultado = re.search(padrao, texto)

    if resultado:
        dia = int(resultado.group(1))
        mes_str = resultado.group(2)
        ano = int(resultado.group(3))

        # Verifica se o mês está no dicionário
        if mes_str in meses:
            mes = meses[mes_str]
            # Formata a data no formato desejado
            data_formatada = f"{dia:02d}/{mes:02d}/{ano}"
            return data_formatada
        else:
            print(f"Erro: mês '{mes_str}' não reconhecido.")
            return None
    else:
        return None  # Retorna None se não encontrar a data  
         
           