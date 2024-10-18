# PROJETO DE SCRAP ZAP IMOVEIS

## Script voltado para fazer scrap do site http://www.zapimoveis.com.br
- Autor: Nelson Seixas

- Data Criação: 16/10/2024

- Empresa: mspbrasil.com.br 

# :hammer: Instruções de uso

- Instale o python mas recente na sua maquina do site https://www.python.org/downloads

- Baixe o chomedriver mais atual do site https://googlechromelabs.github.io/chrome-for-testing/#stable descompacte o arquivo zip e coloque na pasta onde está instalado o google chome no meu caso "C:\Program Files\Google\Chrome\Application\chromedriver.exe". 

- Instale as seguinte libs do python usando pip 
    - pip install selenium
    - pip install openpyxl
    - pip install pandas  Observação: Creio quen não seja necessário o uso da mesma
    - pip install bs4 
    - pip pyinstaller - esse para tranaforma o script em um executavel


- Para converter o scrpit em executalvel utilize o pyinstaller  

- pyinstaller.exe --hidden-import=funcoes_especificas -F zapimoveis.py, depois de compilado ele cria uma pasta chamada dist dentro do projeto o executável está nessa pasta.

### Observação o script ler os links conforme a busca e colcoa no array de set(), esse array e limitado pela memória ram da maquina. 

- A planilha xmls é criada onde esta o executavel ou script, caso queira mudar procure o trecho de código   workbook.save("imoveis.xlsx")  na linha 284 e modifique o caminho conforme sua necessidade, os registro sao salvos na planilha a cada 50 processos do mesmo assim garante que os dados serão salvos na planilha excel.

### Qualquer dúvida estamos a sua disposição para esclarecimentos.





 

