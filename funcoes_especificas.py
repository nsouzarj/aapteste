import requests, time, re


""" Traz cep do logradouro da api  https://viacep.com.br/ """
def get_ceps_por_logradouro(logradouro, numero=None, cidade=None, estado=None):
  
  # Faz a requisição à API do ViaCEP
  url = f"https://viacep.com.br/ws/{estado}/{cidade}/{logradouro}/json/"
  response = requests.get(url)
  time.sleep(2)

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
    return "Indefinido"
 

def parse_address(address):
    # Substitui o hífen por uma vírgula para facilitar a separação
    address = address.replace(" - ", ",")
    # Divide o endereço em partes usando a vírgula como delimitador
    partes = [parte.strip() for parte in address.split(",")]

    # Inicializa as variáveis com valores padrão
    logradouro = "inexistente"
    numero = "inexistente"
    bairro = "inexistente"
    cidade = "inexistente"
    estado = "inexistente"

    # Verifica se há pelo menos duas partes (cidade e estado)
    if len(partes) >= 2:
        # O primeiro elemento é sempre o logradouro
        logradouro_completo = partes[0].strip()
        
        # O último elemento é sempre o estado
        estado = partes[-1].strip()
        
        # A penúltima parte é sempre a cidade
        cidade = partes[-2].strip()
        
        numero = partes[1].strip()

        # Verifica se há um número logo após o logradouro
        logradouro_partes = logradouro_completo.split()
        
        if len(logradouro_partes) > 1 and logradouro_partes[-1].isdigit():
            numero = logradouro_partes.pop()  # Remove e atribui como número
        
        # Recria o logradouro sem o número
        logradouro = ' '.join(logradouro_partes)

        # Se houver mais de três partes, a antepenúltima pode ser um bairro
        if len(partes) > 3:
            bairro = partes[-3].strip() 
            if bairro.isdigit():
              bairro="inexistente"       
        if not numero.isdigit():
              numero="inexistente"
    
    return (logradouro, numero, bairro, cidade, estado)
# Como usar & tipo de endereços     # 
#logradouro, numero, bairro, cidade, estado = parse_address("Avenida Presidente Dutra, 1100 - Centro, Itaperuna - RJ")
# AQUI SAO OS TIPOS DE ENDEREÇO como exemplo
# Rua Gama, 116 - Condominio Quintas do Sol, Nova Lima - MG
# Rua dos Beija-Flores - Alphaville Lagoa Dos Ingleses, Nova Lima - MG
# 
# Vila del Rey, 300 Nova Lima - MG
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
      
      
    """ Separa precos de compra e venda """
         
    
    
def separar_precos(texto):
    # Dividir o texto em linhas
    linhas = texto.split('\n')
    # Verificar se o texto é "Sob consulta"
   
    if texto=='':
       return {
            'Venda': "",
            'Aluguel': ""
        }
   
    # Verificar se o texto é "Valor sob consulta"
    if texto.strip() == "Valor sob consulta":
        return {
            'Venda': "Valor sob consulta",
            'Aluguel': "Valor sob consulta"
        }
        
    
    # Inicializar um dicionário para armazenar os preços
    precos = {}
    
    # Iterar sobre as linhas e extrair os preços
    for i in range(0, len(linhas), 2):
        tipo = linhas[i].strip()  # Tipo (Venda ou Aluguel)
        valor = linhas[i + 1].strip() if i + 1 < len(linhas) else ""  # Valor correspondente
        
        # Verificar se o tipo é válido e se o valor não está vazio
        if tipo in ["Venda", "Aluguel"] and valor:
            # Remover o símbolo 'R$' e formatar o valor
            valor_formatado = valor.replace('R$', '').strip()
            # Armazenar no dicionário
            precos[tipo] = valor_formatado
    
    # Retornar valores ou "" caso não existam
    return {
        'Venda': precos.get('Venda', ""),
        'Aluguel': precos.get('Aluguel', "")
    }

# Exemplo de uso
    