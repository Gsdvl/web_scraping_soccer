import requests
from datetime import datetime, timedelta
import re
import os
import copy
import numpy as np
import pandas as pd
import argparse


date = []
error_msg = "{'error': {'code': 404, 'message': 'Not Found'}}{'error': {'code': 404, 'message': 'Not Found'}}"
data_path = 'Data/'

def normal_case_to_snake_case(text):
    # Remove espaços extras e converte para snake_case
    return re.sub(r'\s+', '_', text.strip()).lower()


match_info_keys = ['match_id', 'home_team', 'away_team', 'year', 'tournament', 'season', 'home_score', 'away_score']
match_info_dict = dict.fromkeys(match_info_keys)
match_info = []

match_overview_keys = ['match_id',
                       'home_ball_possession', 'away_ball_possession',
                       'home_big_chances', 'away_big_chances',
                       'home_total_shots', 'away_total_shots',
                       'home_goalkeeper_saves', 'away_goalkeeper_saves',
                       'home_corner_kicks', 'away_corner_kicks',
                       'home_fouls', 'away_fouls',
                       'home_passes', 'away_passes',
                       'home_tackles', 'away_tackles',
                       'home_free_kicks', 'away_free_kicks',
                       'home_yellow_cards', 'away_yellow_cards']
match_overview_dict = dict.fromkeys(match_overview_keys)
match_overview = []

shots_keys = ['match_id',
              'home_total_shots', 'away_total_shots',
              'home_shots_on_target', 'away_shots_on_target',
              'home_hit_woodwork', 'away_hit_woodwork',
              'home_shots_off_target', 'away_shots_off_target',
              'home_blocked_shots', 'away_blocked_shots',
              'home_shots_inside_box', 'away_shots_inside_box',
              'home_shots_outside_box', 'away_shots_outside_box']
shots_dict = dict.fromkeys(shots_keys)
shots = []

attack_keys = ['match_id',
               'home_big_chances_scored', 'away_big_chances_scored',
               'home_offsides', 'away_offsides']
attack_dict = dict.fromkeys(attack_keys)
attack = []

passes_keys = ['match_id',
               'home_accurate_passes', 'away_accurate_passes',
               'home_final_third_entries', 'away_final_third_entries',
               'home_long_balls', 'away_long_balls',
               'home_crosses', 'away_crosses']
passes_dict = dict.fromkeys(passes_keys)
passes = []

duels_keys = ['match_id',
              'home_dispossessed', 'away_dispossessed']
duels_dict = dict.fromkeys(duels_keys)
duels = []

defending_keys = ['match_id',
                  'home_total_tackles', 'away_total_tackles',
                  'home_interceptions', 'away_interceptions',
                  'home_recoveries', 'away_recoveries',
                  'home_clearances', 'away_clearances']
defending_dict = dict.fromkeys(defending_keys)
defending = []

goalkeeping_keys = ['match_id',
                    'home_total_saves', 'away_total_saves',
                    'home_goal_kicks', 'away_goal_kicks']
goalkeeping_dict = dict.fromkeys(goalkeeping_keys)
goalkeeping = []


def dates_from_date(year, month, day):
    start_date = datetime(year, month, day)
    end_date = datetime.now() - timedelta(days=1)

    temp_date = start_date
    while temp_date <= end_date:
        date.append(temp_date.strftime('%Y-%m-%d'))
        temp_date += timedelta(days=1)


def get_info_page(date):
    print(f"COLENDO PÁGINA DA DATA: {date}")
    try:
        print("Pagina obtida, salvando...")
        resp = requests.get(f'https://www.sofascore.com/api/v1/sport/football/scheduled-events/{date}')
        if resp.status_code == 200:
            return resp.json()
        else:
            print(f"Erro ao obter página: {resp.status_code}")
            return error_msg
    except Exception as e:
        print(f"Erro ao tentar acessar a página: {e}")
        return error_msg


def get_statistics_page(id):
    try:
        print("Pagina obtida, salvando...")
        resp = requests.get(f'https://www.sofascore.com/api/v1/event/{id}/statistics')
        if resp.status_code == 200:
            return resp.json()
        else:
            print(f"Erro ao obter página: {resp.status_code}")
            return error_msg
    except Exception as e:
        print(f"Erro ao tentar acessar a página: {e}")
        return error_msg


def get_event_info(page):
    for event in page["events"]:
        if 'error' not in page and event['status']['type'] == 'finished':
            match_info_dict = {}

            id = event['id']

            home_team = event.get('homeTeam', {}).get('name', "Time da casa não disponível")
            away_team = event.get('awayTeam', {}).get('name', "Time de fora não disponível")

            year = event.get('season', {}).get('year', "Ano não disponível")
            season = event.get('season', {}).get('name', "Temporada não disponível")
            tournament = event.get('tournament', {}).get('name', "Nome do torneio indisponível")
            home_score = event.get('homeScore', {}).get('current', "Pontuação do time da casa não disponível")
            away_score = event.get('awayScore', {}).get('current', "Pontuação do time rival não disponível")

            match_info_dict['match_id'] = id
            match_info_dict['home_team'] = home_team
            match_info_dict['away_team'] = away_team
            match_info_dict['year'] = year
            match_info_dict['tournament'] = tournament
            match_info_dict['season'] = season
            match_info_dict['home_score'] = home_score
            match_info_dict['away_score'] = away_score

            print(match_info_dict)
            print('=================================================')
            statistics_page = get_statistics_page(id)
            print(f"ID DA PAGINA: {id}")
            if 'error' not in statistics_page:
                get_statistics(statistics_page, id)
            # print('=========================================================')
            match_info.append(copy.deepcopy(match_info_dict))



def process_statistics(category, stats_list, dict, id):
    stats_dict = copy.deepcopy(dict)
    for item in category['statisticsItems']:
        #print("NOME DO ITEM A SER COLETADO:"+item['name'])
        key_home = 'home_' + normal_case_to_snake_case(item['name'])
        key_away = 'away_' + normal_case_to_snake_case(item['name'])
        stats_dict[key_home] = item['home']
        stats_dict[key_away] = item['away']
        stats_dict['match_id'] = id
    stats_list.append(stats_dict)
    #print(item['name'] + ' collected')


def get_statistics(page, id):
    for category in page['statistics'][0]['groups']:
        if category['groupName'] == 'Match overview':
            #print("Coletando overview")
            process_statistics(category, match_overview, match_overview_dict, id)
        elif category['groupName'] == 'Shots':
            #print("Coletando chutes...")
            process_statistics(category, shots, shots_dict, id)
        elif category['groupName'] == 'Attack':
            #print("Coletando ataques...")
            process_statistics(category, attack, attack_dict, id)
        elif category['groupName'] == 'Passes':
            #print("Coletando passes")
            process_statistics(category, passes, passes_dict, id)
        elif category['groupName'] == 'Duels':
            #print("Coletando duelos...")
            process_statistics(category, duels, duels_dict, id)
        elif category['groupName'] == 'Defending':
            #print("Coletando defesas...")
            process_statistics(category, defending, defending_dict, id)
        elif category['groupName'] == 'Goalkeeping':
            #print("Coletando informações do goleiro...")
            process_statistics(category, goalkeeping, goalkeeping_dict, id)
        else:
            print("Unknown category collected")


def export_data(data, path):
    if not isinstance(data, pd.DataFrame):
        data = pd.DataFrame(data)
    data = data.drop_duplicates()
    data.to_csv(path, index=False)
    print("dados salvos")


def save_all_data():
    export_data(match_info, 'Data/match_info.csv')
    export_data(match_overview, 'Data/match_overview.csv')
    export_data(shots, 'Data/shots.csv')
    export_data(attack, 'Data/attack.csv')
    export_data(duels, 'Data/duels.csv')
    export_data(passes, 'Data/passes.csv')
    export_data(defending, 'Data/defending.csv')
    export_data(goalkeeping, 'Data/goalkeeping.csv')


def gather_data(year, month, day):
    dates_from_date(year,month, day)
    for date_idx in range(0, len(date)):
        get_event_info(get_info_page(date[date_idx]))
    if os.path.isdir(data_path) and not os.listdir(data_path):
        save_all_data()
    else:
        update_data()


def register_last_gathering(date):
    path = 'gathering_log.txt'

    if os.path.exists(path):
        os.remove(path)

    with open(path, 'w') as arquivo:
        arquivo.write(f'{date.year}\n')
        arquivo.write(f'{date.month}\n')
        arquivo.write(f'{date.day}\n')


def get_last_gathering():
    path = 'gathering_log.txt'
    data = datetime.now()
    if os.path.exists(path):
        with open(path, 'r') as arquivo:
            linhas = arquivo.readlines()[:3]
            data.year = int(linhas[0].strip())
            data.month = int(linhas[1].strip())
            data.day = int(linhas[2].strip())

    return data


def update_data():
    match_info_old = pd.read_csv('Data/match_info.csv')
    match_overview_old = pd.read_csv('Data/match_overview.csv')
    shots_old = pd.read_csv('Data/shots.csv')
    attack_old = pd.read_csv('Data/attack.csv')
    duels_old = pd.read_csv('Data/duels.csv')
    passes_old = pd.read_csv('Data/passes.csv')
    defending_old = pd.read_csv('Data/defending.csv')
    goalkeeping_old = pd.read_csv('Data/goalkeeping.csv')

    match_info_df = pd.DataFrame(match_info)
    match_overview_df = pd.DataFrame(match_overview)
    shots_df = pd.DataFrame(shots)
    attack_df = pd.DataFrame(attack)
    duels_df = pd.DataFrame(duels)
    passes_df = pd.DataFrame(passes)
    defending_df = pd.DataFrame(defending)
    goalkeeping_df = pd.DataFrame(goalkeeping)

    export_data(pd.concat([match_info_old, match_info_df]), 'Data/match_info.csv')
    export_data(pd.concat([match_overview_old, match_overview_df]), 'Data/match_overview.csv')
    export_data(pd.concat([shots_old, shots_df]), 'Data/shots.csv')
    export_data(pd.concat([attack_old, attack_df]), 'Data/attack.csv')
    export_data(pd.concat([duels_old, duels_df]), 'Data/duels.csv')
    export_data(pd.concat([passes_old, passes_df]), 'Data/passes.csv')
    export_data(pd.concat([defending_old, defending_df]), 'Data/defending.csv')
    export_data(pd.concat([goalkeeping_old, goalkeeping_df]), 'Data/goalkeeping.csv')

    return print("data updated")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Script para raspar dados do Sofascore")
    parser.add_argument('--year', type=int, default=2024, help="Ano da data de raspagem")
    parser.add_argument('--month', type=int, default=10, help="Mês da data de raspagem")
    parser.add_argument('--day', type=int, default=1, help="Dia da data de raspagem")

    args = parser.parse_args()
    date_to_scrape = datetime(args.year, args.month, args.day)

    if os.path.isdir(data_path) and not os.listdir(data_path):
        gather_data(date_to_scrape.year, date_to_scrape.month, date_to_scrape.day)
        register_last_gathering(date_to_scrape)
    else:
        last_update = get_last_gathering()
        print("Coletando novos dados")
        gather_data(last_update.year, last_update.month, last_update.day)
