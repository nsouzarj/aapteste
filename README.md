# PROJETO DE SCRAP ZAP IMOVEIS

## Script voltado para fazer scrap do site http://www.zapimoveis.com.br
- Autores: Nelson Seixas/ Atilano/ Roberta

- Data Criação: 16/10/2024

- Empresa: mspbrasil.com.br 

# :hammer: Instruções de uso

- Instale o python mas recente na sua maquina do site https://www.python.org/downloads

- Baixe o google com drive mais atual do site es no projetocoloque a pasta no seu  lugar de preferência exemplo: C:\Program Files\Google\Chrome\Application  onde fica o google chome instalado.


 do zapimoveis.py dever ser alterada conforme onde você descompactou o arquivo zip.  

- Instale as seguinte libs do python usando pip 
    - pip install selenium
    - pip install openpyxl
    - pip install pandas  Observação: Creio quen não seja necessário o uso da mesma
    - pip install bs4 
    - pip install requests-cache
    - pip install pyinstaller - esse para transformar o script em um executavel podenos ser executado sem a necessidade do python instalado no local


- Para converter o scrpit em executalvel utilize o pyinstaller  

- pyinstaller.exe --hidden-import=funcoes_especificas -F zapimoveis.py, depois de compilado ele cria uma pasta chamada dist dentro do projeto o executável está nessa pasta.

### Observação o script ler os links conforme a busca e colcoa no array de set(), esse array e ilimitado pela memória ram da maquina. 

- A planilha xlsx é criada onde esta o executavel ou script, caso queira mudar procure o trecho de código   workbook.save("C:\Users\User\Documents\zapimoveis\listadeimoveis.xlsx")  e modifique o caminho conforme sua necessidade, os registro sao salvos na planilha a cada 50 a cada lida da lista armazenada assim garante que os dados serão salvos na planilha excel.

### Qualquer dúvida estamos a sua disposição para esclarecimentos.

### Como exeutar o projeto 

- Baixe o program do git est ana pasta dist 

- A execução: 

zapimoveis.exe 'C:\Users\User\Documents\zapimoveis' 'C:\Program Files\Google\Chrome\Application\chromedriver.exe' 'https://www.zapimoveis.com.br/aluguel/imoveis/mg+belo-horizonte/?__ab=sup-hl-pl:newC,exp-aa-test:B,super-high:new,off-no-hl:new,pos-zap:new,new-rec:b,lgpd-ldp:test&transacao=aluguel&onde=,Minas%20Gerais,Belo%20Horizonte,,,,,city,BR%3EMinas%20Gerais%3ENULL%3EBelo%20Horizonte,-19.919052,-43.938669,&pagina=' 'aluguel' '25'

- 1) Primeiro parametro: Onde vai ser salvo o arquivo ou plaiha dos imoveis xls 

- 2) Segundo parametro: Onde esta o chomesdrive 

- 3) Terceiro parametro: O link do filtro de busca dos imoveis

- 4) Quarto parametro: Tipo de filtro 'aluguel' ou 'venda'

- 5) Quinto parametro: Numerpo de tehas para ser executado o ideal é 20







 

