import re
import locale
from datetime import datetime

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

# Exemplo de uso
texto = "Anúncio criado em 26 de junho de 2024, atualizado há 2 dias."
data_resultado = extrair_e_formatar_data(texto)
print(data_resultado)  # 