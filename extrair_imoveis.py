import re

def parse_address(address):
    # Substitui o hífen por uma vírgula para facilitar a separação
    address = address.replace("-", ",")
    
    # Regex pattern para capturar os componentes do endereço
    pattern = r'^(?P<logradouro>[^,]+),?\s*(?P<numero>\d*)?\s*,?\s*(?P<bairro>[^,]*)?,?\s*(?P<cidade>[^,]+?)\s*,\s*(?P<estado>[A-Z]{2})$'
    
    # Tenta fazer o match do endereço com o padrão
    match = re.match(pattern, address.strip())
    
    if match:
        logradouro = match.group("logradouro").strip() if match.group("logradouro") else "inexistente"
        numero = match.group("numero").strip() if match.group("numero") else "inexistente"
        bairro = match.group("bairro").strip() if match.group("bairro") else "inexistente"
        cidade = match.group("cidade").strip() if match.group("cidade") else "inexistente"
        estado = match.group("estado").strip() if match.group("estado") else "inexistente"
       
        if cidade=='':
           cidade = bairro
           bairro=''   
        # Retorna como uma tupla
        return (logradouro, numero, bairro, cidade, estado)
    else:
        return ("inexistente", "inexistente", "inexistente", "inexistente", "inexistente")

# Exemplo de endereço no novo formato
address = "Balneario Água Limpa, Nova Lima - MG"

# Analisando o endereço e imprimindo o resultado
parsed = parse_address(address)
logradouro, numero, bairro, cidade, estado = parsed

print(f"Logradouro: {logradouro}")
print(f"Número: {numero}")
print(f"Bairro: {bairro}")
print(f"Cidade: {cidade}")
print(f"Estado: {estado}")
