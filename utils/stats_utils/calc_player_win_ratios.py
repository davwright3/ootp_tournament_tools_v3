"""Modules for returning a dataframe with player win ratios."""
import pandas as pd
from scipy.spatial.distance import num_obs_dm

from utils.data_utils.data_store import data_store
from utils.data_utils.card_list_store import card_list_store
import math


def calc_player_win_ratios(
        num_teams,
        games_per_round,
        games_per_finals,
        min_apps=20,
        min_rating=40,
        max_rating=105,
        position_select=None,
        player_search_term=None
):
    print('Calculating player win ratios...')
    print('num_teams', num_teams)
    print('games_per_round', games_per_round)
    print('games_per_finals', games_per_finals)


    stats = data_store.get_data().copy()
    total_trny = stats['Trny'].nunique()
    print(f'Total trny: {total_trny}')
    num_rounds = int(math.log2(num_teams))
    req_wins_per_round = {}
    for rnd in range(1, num_rounds):
        req_wins_per_round[rnd + 1] = (rnd) * math.ceil(games_per_round / 2)
    req_wins_per_round[num_rounds + 1] = req_wins_per_round[next(reversed(req_wins_per_round))] + math.ceil(games_per_finals /2)
    print(req_wins_per_round)

    teams_in_round = {}
    teams_in_round[1] = num_teams
    for rnd in range(1, num_rounds + 1):
        teams_in_round[rnd + 1] = teams_in_round[rnd] / 2

    total_teams_in_rnd = {}
    for rnd in range(0, num_rounds + 1):
        total_teams_in_rnd[rnd + 1] = total_trny * teams_in_round[rnd + 1]

    print(total_teams_in_rnd)

    # TODO Get team wins per tournament: get just the team, tournament and wins
    # TODO Copy those wins to individual players in the original frame
    # TODO Crate columns for each round

    team_wins_df = stats.copy()[['ORG', 'Trny', 'W']].groupby(['ORG', 'Trny']).sum().reset_index()

    players = stats.copy()[['CID', 'ORG', 'Trny']]
    players['App'] = 1
    result = players.merge(team_wins_df, on=['ORG', 'Trny'], how='left')

    for rnd in req_wins_per_round.keys():
        result[f'R{rnd}'] = (result['W'] >= req_wins_per_round[rnd])

    result = result.drop(columns=['ORG', 'Trny', 'W'])

    result = result.groupby(['CID'], as_index=False).sum()
    for rnd in req_wins_per_round.keys():
        result[f'R{rnd}%'] = round((result[f'R{rnd}'] / result['App']) * 100, 1)

    keys = list(total_teams_in_rnd.keys())
    for rnd in keys[1:]:
        result[f'R{rnd}% T'] = round((result[f'R{rnd}'] / total_teams_in_rnd[rnd] * 100), 1)

    result = result.rename(columns={f'R{keys[-1]}' : 'CH', f'R{keys[-2]}' : 'F', f'R{keys[-3]}': 'SF'})
    result = result.rename(columns={f'R{keys[-1]}%': 'CH%', f'R{keys[-2]}%': 'F%',
                                    f'R{keys[-3]}%': 'SF%'})
    result = result.rename(columns={f'R{keys[-1]}% T': 'CH% T', f'R{keys[-2]}% T': 'F% T',
                                    f'R{keys[-3]}% T': 'SF% T'})

    result = result.sort_values(by=['App'], ascending=False)
    result = result[result['App'] >= min_apps]

    cards = card_list_store.get_card_list().copy()
    if position_select is not None and position_select != 'All':
        if position_select == 'Pitcher Role':
            cards = cards[cards['Position'] == 1]
        else:
            cards = cards[cards[position_select] == 1]

    cards = cards[['Card ID', '//Card Title', 'Card Value']]
    cards = cards.rename(columns={'Card ID': 'CID', '//Card Title': 'Title', 'Card Value': 'Val'})

    cards = cards[cards['Val'].between(min_rating, max_rating)]

    if player_search_term is not None:
        cards = cards[cards['Title'].str.contains(player_search_term, case=False)]

    final_result = pd.merge(cards, result, on='CID', how='inner')
    final_result = final_result[['Title', 'Val', 'App', 'SF', 'F', 'CH', 'SF%', 'F%',
                                 'CH%', 'SF% T', 'F% T', 'CH% T']]

    # print(final_result.head(30))

    return final_result