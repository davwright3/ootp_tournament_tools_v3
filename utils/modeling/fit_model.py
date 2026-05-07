"""Module for fitting walks model to card list"""
import numpy as np
import joblib
from utils.config_utils.load_save_settings import get_target_data_folder


def fit_model(df, model_name, header_name, player_type):
    target_folder = get_target_data_folder()

    left_model = joblib.load(f'{target_folder}/models/{model_name}_model_left.pkl')
    left_scaler = joblib.load(f'{target_folder}/models/{model_name}_scaler_left.pkl')

    right_model = joblib.load(f'{target_folder}/models/{model_name}_model_right.pkl')
    right_scaler = joblib.load(f'{target_folder}/models/{model_name}_scaler_right.pkl')

    features_file = joblib.load(f'{target_folder}/models/{model_name}_features.pkl')

    if player_type == 'bat':
        left_mask = df['Bats'].isin([1, 3])
        right_mask = df['Bats'].isin([2, 3])
    else:
        left_mask = df['Throws'].isin([1])
        right_mask = df['Throws'].isin([2])

    df[header_name] = np.nan
    features = features_file

    valid_left_players = df.loc[left_mask, features].dropna().index
    valid_right_players = df.loc[right_mask, features].dropna().index

    if not valid_left_players.empty:
        x_new_left = df.loc[valid_left_players, features]
        x_new_left_scaled = left_scaler.transform(x_new_left)
        df.loc[valid_left_players, header_name] = left_model.predict(x_new_left_scaled)

    if not valid_right_players.empty:
        x_new_right = df.loc[valid_right_players, features]
        x_new_right_scaled = right_scaler.transform(x_new_right)
        df.loc[valid_right_players, header_name] = right_model.predict(x_new_right_scaled)

    return df

