import requests
import json
import re

""" Traz cep do logradouro """
def get_ceps_por_logradouro(logradouro, numero=None, cidade=None, estado=None):
  """
  Busca CEPs de um logradouro e retorna o mais próximo, considerando o número (opcional).

  Args:
    logradouro: O nome do logradouro a ser pesquisado.
    numero: O número do logradouro (opcional). Pode ser um inteiro ou "Inexistente".
    cidade: A cidade do logradouro.
    estado: O estado do logradouro.

  Returns:
    Um dicionário contendo o CEP mais próximo do logradouro.
  """
  
  # Faz a requisição à API do ViaCEP
  url = f"https://viacep.com.br/ws/{estado}/{cidade}/{logradouro}/json/"
  response = requests.get(url)

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
def encontrar_cep_mais_proximo(ceps, numero):
  """
  Encontrar o CEP mais próximo com base no número do logradouro.

  Args:
    ceps: A lista de CEPs retornados pela API.
    numero: O número do logradouro (inteiro).

  Returns:
    O CEP mais próximo com base no número do logradouro.
  """

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
"""
# Exemplo de uso
logradouro = "Rua Tomaz Gonzaga"
numero = "400"  # Número é opcional
cidade = "Nova Lima"
estado = "MG"

cep_mais_proximo = get_ceps_por_logradouro(logradouro, numero, cidade, estado)

if cep_mais_proximo:
  print(f"CEP mais próximo de {logradouro}, {cidade}, {estado}: {cep_mais_proximo['cep']}")
else:
  print(f"Nenhum CEP encontrado para {logradouro}, {cidade}, {estado}.")
"""  

def extrair_numeros(frase):
    """Extrai números de uma frase, separando-os por hífen.

    Args:
      frase: A frase da qual os números serão extraídos.

    Returns:
      Uma string com os números encontrados separados por hífen, ou uma string vazia
      se nenhum número for encontrado.
    """
    partes = frase.split()
    numeros = []
    for parte in partes:
        if parte.isdigit() or '-' in parte: # Inclui partes com hífen 
          numeros.extend(parte.split('-')) # Separa partes com hífen em números individuais
        if numeros:
          return '-'.join(numeros)    
        else:
          return ""

# Exemplos de uso
"""    
frase1 = "3-3 andar"
frase2 = "4 quartos"
frase3 = "sem números"
frase4 = "40 m²"
print(f"Frase 1: '{frase1}', Números: {extrair_numeros(frase1)}")
print(f"Frase 2: '{frase2}', Números: {extrair_numeros(frase2)}")
print(f"Frase 3: '{frase3}', Números: {extrair_numeros(frase3)}")
print(f"Frase 4: '{frase4}', Números: {extrair_numeros(frase4)}")
"""



""" Rerona o tipo do imovel"""
def encontrar_tipo_imovel(descricao, tipos_imoveis):
    for indice, tipo in enumerate(tipos_imoveis):
        if tipo.lower() in descricao.lower():  # Ignora maiúsculas/minúsculas
            return tipo  # Retorna o tipo encontrado
    return None 
 
 

""" Esta funcao trata a localizacao do imovel separando por partes"""
def parse_address(address):
    # Substitui o hífen por uma vírgula para facilitar a separação
    # Encontra a posição da ","
    indice_virgula = address.find(",")

   # Substitui a parte depois da ","  
    endereco_modificado = address[:indice_virgula+1] + address[indice_virgula+1:].replace("-", ",")
    endereco_modificado = address[:indice_virgula+1] + address[indice_virgula+1:].replace(" - ", ",")
    # Remove espaços em branco após as vírgulas na parte da frase após a primeira vírgula
    endereco_modificado = endereco_modificado[:indice_virgula+1] + endereco_modificado[indice_virgula+1:].replace(" ,", ",")
    # Regex pattern para capturar os componentes do endereço
    pattern = r'^(?P<logradouro>[^,]+),?\s*(?P<numero>\d*)?\s*,?\s*(?P<bairro>[^,]*)?,?\s*(?P<cidade>[^,]+?)\s*,\s*(?P<estado>[A-Z]{2})$'
    # Tenta fazer o match do endereço com o padrão
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
      
# Como usar     
#logradouro, numero, bairro, cidade, estado = parse_address("Rua dos Beija Flores, 130 - Alphaville Lagoa Dos Ingleses, Nova Lima - MG")
      
      
""" Funcao que moreov parte do texto """ 
def remover_parte_texto(texto, parte_a_remover):
    """Remove a parte especificada da string e retorna o restante."""
    return texto.replace(parte_a_remover, "").strip()  
  
  
""" Extari a data do formato exrenso """  
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
         
           