import pandas as pd
from utils.data_utils.data_store import data_store
from utils.data_utils.card_list_store import card_list_store


def generate_strikeouts_by_avoid_k_df():
    cards = card_list_store.get_card_list()[['Card ID', '//Card Title', 'Avoid Ks']].copy()
    cards = cards.rename(columns={'Card ID': 'CID', '//Card Title': 'Title'})

    data = data_store.get_data()[['CID', 'PA', 'K']].copy()
    data = data.groupby(['CID']).sum()
    data = data[data['PA'] > 600]
    data['K/600'] = round((data['K'] / data['PA']) * 600, 2)

    data = pd.merge(cards, data, how='inner', on=['CID'])

    final_df = data[['Avoid Ks', 'K/600', 'Title']]
    return final_df