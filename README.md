# PROJETO DE SCRAP ZAP IMOVEIS

## Script voltado para fazer scrap do site http://www.zapimoveis.com.br
- Autor: Nelson Seixas
- Data Criação: 16/10/2024

# :hammer: Instruções de uso

- Instale o python mas recente na sua maquina do site https://www.python.org/downloads

- Baixe o chomedriver mais atual do site https://googlechromelabs.github.io/chrome-for-testing/#stable desccompacte o aruivo zip e coloqye na naspata onde esta instalado o google chome no meu caso "C:\Program Files\Google\Chrome\Application\chromedriver.exe". 

- Instale as seguinte libs do pyhon usando pip 
    - pip install selenium
    - pip install openpyxl
    - pip install pandas obs: Crio não ser necessário
    - pip install bs4 
    - pip pyinstaller - esse para tranaforma o script em um executavel


- Para converter o scrpit em executalvel utilize o pyinstaller  

- pyinstaller.exe --hidden-import=funcoes_especificas -F zapimoveis.py  depois de compilado ele cria uma pasta chamada dist dentro do projeto o executavel esta nessa pasta.

### Observação o scpiit leto dos os link conforme a busca e colcoa no array de set() 

- A planilah ae criada onde esta o executavel o scriot caso queira mudar procrure na linha 284    workbook.save("imoveis.xlsx") e modifique o caminho conforme sua necessidade os registro sao são sao salvos a cada 50 registros lido.





 

