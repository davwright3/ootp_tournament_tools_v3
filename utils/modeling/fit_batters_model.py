"""Module for fitting walks model to card list"""
import numpy as np
import joblib
from utils.config_utils.load_save_settings import get_target_data_folder


def fit_batters_model(df, model_name, header_name):
    target_folder = get_target_data_folder()

    walks_left_model = joblib.load(f'{target_folder}/models/{model_name}_model_left.pkl')
    walks_left_scaler = joblib.load(f'{target_folder}/models/{model_name}_scaler_left.pkl')

    walks_right_model = joblib.load(f'{target_folder}/models/{model_name}_model_right.pkl')
    walks_right_scaler = joblib.load(f'{target_folder}/models/{model_name}_scaler_right.pkl')

    features_file = joblib.load(f'{target_folder}/models/{model_name}_features.pkl')

    left_mask = df['Bats'].isin([1, 3])
    right_mask = df['Bats'].isin([2, 3])

    df[header_name] = np.nan
    features = features_file

    valid_left_walks = df.loc[left_mask, features].dropna().index
    valid_right_walks = df.loc[right_mask, features].dropna().index

    if not valid_left_walks.empty:
        x_new_left = df.loc[valid_left_walks, features]
        x_new_left_scaled = walks_left_scaler.transform(x_new_left)
        df.loc[valid_left_walks, header_name] = walks_left_model.predict(x_new_left_scaled)

    if not valid_right_walks.empty:
        x_new_right = df.loc[valid_right_walks, features]
        x_new_right_scaled = walks_right_scaler.transform(x_new_right)
        df.loc[valid_right_walks, header_name] = walks_right_model.predict(x_new_right_scaled)

    return df

