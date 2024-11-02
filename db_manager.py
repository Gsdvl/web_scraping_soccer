import pandas as pd
import sqlite3


conn = sqlite3.connect("Data/soccer_database.db")
cursor = conn.cursor()


files_and_tables = [
    ("Data/match_info.csv", "Info_table"),
    ("Data/match_overview.csv", "Overview_table"),
    ("Data/attack.csv", "Attack_table"),
    ("Data/duels.csv", "Duels_table"),
    ("Data/passes.csv", "Passes_table"),
    ("Data/defending.csv", "Defense_table"),
    ("Data/goalkeeping.csv", "Goalkeeping_table"),
    ("Data/shots.csv", "Shots_table"),
]


for csv_file, table_name in files_and_tables:
    try:
        df = pd.read_csv(csv_file)
        df.to_sql(table_name, conn, if_exists="replace", index=False)
        print(f"Tabela '{table_name}' carregada com sucesso.")
    except Exception as e:
        print(f"Erro ao carregar '{table_name}': {e}")


###############################################################################


def see_team_game(team):
    query = """
       SELECT * FROM Info_table WHERE home_team  = ? OR away_team = ?
    """
    cursor.execute(query, (team, team))
    results = cursor.fetchall()
    cursor.execute("PRAGMA table_info (Info_table);")
    colunas = [col[1] for col in cursor.fetchall()]
    print(results)
    return results, colunas


def see_tournament(tournament):
    query = """
        SELECT * FROM Info_table WHERE tournament = ?
    """
    cursor.execute(query, (tournament, ))
    results = cursor.fetchall()
    cursor.execute("PRAGMA table_info (Info_table);")
    colunas = [col[1] for col in cursor.fetchall()]
    print(results)
    return results, colunas


def create_view_cards():
    query = """
        CREATE VIEW IF NOT EXISTS game_cards AS
        SELECT
            i.home_team AS team,
            o.home_yellow_cards AS yellow_cards,
            o.home_red_cards AS red_cards
        FROM Overview_table o
        JOIN Info_table i ON o.match_id = i.match_id

        UNION ALL

        SELECT
            i.away_team AS team,
            o.away_yellow_cards AS yellow_cards,
            o.away_red_cards AS red_cards
        FROM Overview_table o
        JOIN Info_table i ON o.match_id = i.match_id
    """
    cursor.execute(query)
    conn.commit()


def see_cards(team):
    query = """
         SELECT *, (COALESCE(yellow_cards,0) + COALESCE(red_cards,0)) AS total_cards FROM game_cards
         WHERE team = ?
         ORDER BY Total_cards DESC
    """
    cursor.execute(query, (team,))
    results = cursor.fetchall()
    cursor.execute("PRAGMA table_info (game_cards);")
    colunas = [col[1] for col in cursor.fetchall()]
    colunas.append('total_cards')
    print(results)
    return results, colunas


def see_top_teams(tournament=''):
    colnames = ["Team", "Score"]
    condition = ''
    if tournament != '':
        condition = f"WHERE tournament = '{tournament}'"
        colnames.append(tournament)
    query = f"""
    SELECT
        home_team AS team,
        home_score AS score
    FROM
        Info_table
    {condition}
    UNION ALL
    SELECT
        away_team AS team,
        away_score AS score
    FROM
        Info_table
    {condition}

    ORDER BY score DESC
    """
    cursor.execute(query)
    results = cursor.fetchall()
    print(results)
    return results, colnames


def team_statistics(team, statistic_type):
    print(f"COLETANDO ESTATISTICAS DE {statistic_type} DO TIME: {team}")
    statistic = f"{statistic_type}_table"
    query = f"""
        SELECT i.home_team, i.away_team, s.*
        FROM {statistic} s
        JOIN Info_table i
        ON s.match_id = i.match_id
        WHERE i.home_team = ? OR i.away_team = ?
    """
    print(query)
    cursor.execute(query, (team, team))
    results = cursor.fetchall()
    print(f"RESULTADOS: {results}")
    if not results:
        print("Nenhum resultado encontrado.")
        return [], []

    cursor.execute(f"PRAGMA table_info ({statistic});")
    nomes = ['home_team', 'away_team']
    colunas = [col[1] for col in cursor.fetchall()]
    colunas = nomes + colunas
    print(f"COLUNAS: {colunas}")
    return results, colunas


def close_connection():
    conn.close()
