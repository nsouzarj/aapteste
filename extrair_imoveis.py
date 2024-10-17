import requests
import json

def get_ceps_por_logradouro(logradouro, numero, cidade, estado):
  """
  Busca CEPs de um logradouro e retorna o mais próximo, considerando o número.

  Args:
    logradouro: O nome do logradouro a ser pesquisado.
    numero: O número do logradouro.
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

    # Mostra o JSON na tela
    print(json.dumps(ceps, indent=4))  # Formata o JSON para melhor visualização

    # Se houver mais de um CEP, encontra o mais próximo
    if isinstance(ceps, list):
      # Encontra o CEP mais próximo com base no número
      cep_mais_proximo = encontrar_cep_mais_proximo(ceps, numero)
    else:
      cep_mais_proximo = ceps

    return cep_mais_proximo
  else:
    return None

def encontrar_cep_mais_proximo(ceps, numero):
  """
  Encontrar o CEP mais próximo com base no número do logradouro.

  Args:
    ceps: A lista de CEPs retornados pela API.
    numero: O número do logradouro.

  Returns:
    O CEP mais próximo com base no número do logradouro.
  """

  cep_mais_proximo = None
  menor_diferenca = float('inf')
  for cep in ceps:
    # Verifica se o complemento está presente e converte para inteiro
    complemento = cep.get('complemento')
    if complemento:
      try:
        complemento_int = int(complemento)
      except ValueError:
        # Se o complemento não for um número inteiro, ignora
        continue

      # Calcula a diferença absoluta entre o número e o complemento
      diferenca = abs(numero - complemento_int)
      
      # Atualiza o CEP mais próximo se a diferença for menor
      if diferenca < menor_diferenca:
        menor_diferenca = diferenca
        cep_mais_proximo = cep

  return cep_mais_proximo

# Exemplo de uso
logradouro = "Rua do Humaitá"
numero = 52
cidade = "Rio de Janeiro"
estado = "RJ"
cep_mais_proximo = get_ceps_por_logradouro(logradouro, numero, cidade, estado)

if cep_mais_proximo:
  print(f"CEP mais próximo de {logradouro} {numero}, {cidade}, {estado}: {cep_mais_proximo['cep']}")
else:
  print(f"Nenhum CEP encontrado para {logradouro} {numero}, {cidade}, {estado}.")