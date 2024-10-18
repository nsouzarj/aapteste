# PROJETO DE SCRAP ZAP IMOVEIS

## Script voltado para fazer scrap do site http://www.zapimoveis.com.br
- Autor: Nelson Seixas

- Data Criação: 16/10/2024

- Empresa: mspbrasil.com.br 

# :hammer: Instruções de uso

- Instale o python mas recente na sua maquina do site https://www.python.org/downloads

- Baixe o chomedriver mais atual do site https://googlechromelabs.github.io/chrome-for-testing/#stable descompacte o aruivo zip e coloqye na pasta onde está instalado o google chome no meu caso "C:\Program Files\Google\Chrome\Application\chromedriver.exe". 

- Instale as seguinte libs do python usando pip 
    - pip install selenium
    - pip install openpyxl
    - pip install pandas  Observação: Crio não ser necessário
    - pip install bs4 
    - pip pyinstaller - esse para tranaforma o script em um executavel


- Para converter o scrpit em executalvel utilize o pyinstaller  

- pyinstaller.exe --hidden-import=funcoes_especificas -F zapimoveis.py, depois de compilado ele cria uma pasta chamada dist dentro do projeto o executavel esta nessa pasta.

### Observação o script ler os link conforme a busca e colcoa no array de set(), esse array e limitado pela memoria da maquina. 

- A planilha xmls é criada onde esta o executavel ou script, caso queira mudar procrure o trecho de código   workbook.save("imoveis.xlsx")  na linha 284 e modifique o caminho conforme sua necessidade os registro sao salvos a cada 50 pagina de detalhes lida.

### Qualquer dúvida estamos a disposição para esclarecimentos 





 

