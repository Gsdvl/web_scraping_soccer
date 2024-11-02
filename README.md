# sofascore_web_scrapping

## Projeto realizado para o processo seletivo da empresa THM Estatística.

O projeto consiste em um programa que realiza uma raspagem de dados do site SofaScore e, a partir disso, gera um banco de dados que possui consultas e views pré-definidas para permitir fácil visualização para o usuário. O projeto foi todo feito em Python; segue abaixo a explicação dos arquivos.

### web_scrapper.py

Esse é o arquivo responsável por fazer solicitações na API pública do SofaScore, obtida após explorar o site no modo inspeção. Recebe informações de data durante sua execução e coleta todos os dados referentes ao banco de dados desde aquele dia até o dia de ontem. Para tal, ele procura na API eventos daquela partida, pega o ID dela e busca pelas estatísticas da partida com aquele ID.

O código também salva a data mais recente de scrape em um arquivo `.txt`, para que, ao abrir, ele pegue todos os dados daquele dia até hoje, concatenando os dados antigos com os novos.

### db_manager.py

Mais simples, esse código é responsável por criar o banco de dados SQL a partir dos CSVs coletados pelo scrapper e criar consultas e views para serem vistas pela GUI. As consultas são:
- Jogos de um time
- Estatística X de um time
- Jogos de um torneio
- Times com mais gols (pode ser de um torneio específico ou qualquer um)
- Quantidade de cartões que certo time tomou em jogos (feito a partir de uma view que filtra isso)

### gui.py

Esse código é responsável por criar a interface com a qual o usuário irá interagir, permitindo escolher a chamada e resetar os dados a partir de uma data específica.

### main.py

O código principal que executa tudo a partir de subprocessos.
