# sofascore_web_scrapping #

## Projeto realizado para o processo seletivo da empresa THM Estatistica. ##

O projeto consiste em um programa que realiza uma raspagem de dados do site sofascore \n
e a partir disso, gera um banco de dados, que possui consultas e views predefinidas \n
para permitir facil visualização para o usuário.
O projeto foi todo feito em python, segue abaixo a explicação dos arquivos.

#### web_scrapper.py ####
Esse é o arquivo responsável por fazer solicitações na API pública do sofascore, obtida após \n
explorar o site no modo inspeção.
Recebe informações de data durante a sua execução, e coleta todos os dados referentes ao banco de dados\n
desde aquela dia até o dia de ontem, para tal, ele procura na API eventos daquela partida, pega o ID dela, \n
e busca pelas estatisticas da partida com aquele ID

O código também salva quando foi a data mais recente de scrape em um txt, para ao abrir, pegar todos os dados \n
daquele dia até hj, e concatenando os dados antigos com os novos

#### db_manager.py ####
Mais simples, esse código é responsável por criar o banco de dados sql a partir dos CSVs coletados pelo scrapper \n
e criar consultas e views para serem vistas pela GUI, as consultas são
Jogos de um time
Estatistica X de um time
Jogos de um torneio
Times com mais gols (pode ser de um torneio especifico ou qualquer um)
Quantidade de cartões que certo time tomou em jogos (feito a partir de uma view que filtra isso)

#### gui.py #### 
Esse código é responsável por criar a interface com a qual o usuário irá interagir, permitindo ele escolher a chamada,
e resetar os dados a partir de uma data específica.

#### main.py ####
O código príncipal que executa tudo a partir de subprocessos
