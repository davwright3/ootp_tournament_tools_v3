"""Module for fitting BABIP for batters."""
import pandas as pd
import os
import numpy as np
import joblib
from utils.config_utils.load_save_settings import get_setting


def fit_batters_babip_model(df):
    print('Fitting batters to BABIP model')

    target_folder = get_setting('InitialTargetDirs', 'starting_target_folder')

    babip_left_model = joblib.load(f'{target_folder}/models/babip_model_left.pkl')
    babip_left_scaler = joblib.load(f'{target_folder}/models/babip_scaler_left.pkl')

    babip_right_model = joblib.load(f'{target_folder}/models/babip_model_right.pkl')
    babip_right_scaler = joblib.load(f'{target_folder}/models/babip_scaler_right.pkl')

    left_mask = df['Bats'].isin([1, 3])
    right_mask = df['Bats'].isin([2, 4])

    df['BABIP_pred'] = np.nan
    babip_features = ['BABIP', 'BABIP vL', 'BABIP vR', 'Speed']

    valid_left_babip = df.loc[left_mask, babip_features].dropna().index
    valid_right_babip = df.loc[right_mask, babip_features].dropna().index

    if not valid_left_babip.empty:
        x_new_left = df.loc[valid_left_babip, babip_features]
        x_new_left_scaled = babip_left_scaler.transform(x_new_left)
        df.loc[valid_left_babip, 'BABIP_pred'] = babip_left_model.predict(
            x_new_left_scaled)

    if not valid_right_babip.empty:
        x_new_right = df.loc[valid_right_babip, babip_features]
        x_new_right_scaled = babip_right_scaler.transform(x_new_right)
        df.loc[valid_right_babip, 'BABIP_pred'] = babip_right_model.predict(
            x_new_right_scaled)


    df['BABIP_pred'] = round(df['BABIP_pred'], 4)

    return df


