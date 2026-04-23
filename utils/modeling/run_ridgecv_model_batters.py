from os import mkdir
import pandas as pd
from utils.modeling.update_model_tracker import update_model_tracker
from pathlib import Path
from sklearn.linear_model import RidgeCV
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib
from utils.data_utils.data_store import data_store
from utils.data_utils.card_list_store import card_list_store
from utils.modeling.model_stat_calcs import run_model_calcs
from utils.config_utils.load_save_settings import get_setting


def run_ridgecv_model(
        passed_stat_columns,
        passed_card_columns,
        model_calc_name,
        target_name,
        model_headers,
        alpha_params,
        cv_params,
        use_batted_ball_type=False
):
    """
    Method for running and saving RidgeCV model.

    Required headers are Card ID/CID, and Bats

    """
    # TODO set up dataframes to prep for modeling
    # TODO run model (start with babip, then set up for inputs via arguments)
    # TODO Arguments needed: Card headers, stat headers, output file paths, method to run
    # TODO print results to command line for testing
    # TODO set up saving of the model using joblib

    use_batted_ball_type = use_batted_ball_type
    # Get the loaded data file
    data = data_store.get_data().copy()
    cards = card_list_store.get_card_list().copy()

    stat_columns = passed_stat_columns
    card_columns = passed_card_columns

    data = data[stat_columns]
    data = data.groupby('CID', as_index=False).sum()
    data = data[data['PA'] >= 50]

    cards = cards[card_columns]
    cards = cards.rename(columns={'Card ID': 'CID', '//Card Title': 'Title'})
    if 'BattedBallType' in cards.columns:
        cards['BattedBallType'] = cards['BattedBallType'].map({0: 'N', 1: 'GB', 2: 'FB', 3: 'LD'})
        cards = pd.get_dummies(cards, columns=['BattedBallType'], drop_first=True)
    cards['Bats'] = cards['Bats'].map({1: 'L', 2: 'R', 3: 'S'})

    # Use methods to get required stats and then merge the ratings with the target stats
    stats = run_model_calcs(data, model_calc_name)
    final_df = pd.merge(cards, stats[['CID', target_name]], on='CID')

    model_df = final_df.copy()

    # Split into three dataframes for left, right and switch
    model_df_left = model_df[model_df['Bats'].isin(['L', 'S'])]
    model_df_right = model_df[model_df['Bats'].isin(['R', 'S'])]

    # Run the left model
    x_model_left = model_df_left[model_headers]
    y_model_left = model_df_left[target_name]

    x_train_left, x_test_left, y_train_left, y_test_left = train_test_split(x_model_left, y_model_left, test_size=0.3, random_state=31)
    left_scalar = StandardScaler()
    x_train_left_scaled = left_scalar.fit_transform(x_train_left)
    x_test_left_scaled = left_scalar.transform(x_test_left)

    left_model = RidgeCV(alphas=alpha_params, cv=cv_params)
    left_model.fit(x_train_left_scaled, y_train_left)

    y_pred_left = left_model.predict(x_test_left_scaled)
    left_model_score = left_model.score(x_test_left_scaled, y_test_left)

    left_model_coeffs = left_model.coef_.flatten()
    for name, importance in zip(x_model_left.columns, left_model_coeffs):
        print(f'{name}: {importance}')
    print('Left model score: ', left_model_score)

    # Run right model
    x_model_right = model_df_right[model_headers]
    y_model_right = model_df_right[target_name]

    x_train_right, x_test_right, y_train_right, y_test_right = train_test_split(x_model_right, y_model_right, test_size=0.3, random_state=32)
    right_scalar = StandardScaler()
    x_train_right_scaled = right_scalar.fit_transform(x_train_right)
    x_test_right_scaled = right_scalar.transform(x_test_right)

    right_model = RidgeCV(alphas=alpha_params, cv=cv_params)
    right_model.fit(x_train_right_scaled, y_train_right)

    y_pred_right = right_model.predict(x_test_right_scaled)
    right_model_score = right_model.score(x_test_right_scaled, y_test_right)
    print("Right model score: ", right_model_score)




    # Save models
    target_folder = f'{get_setting("InitialTargetDirs", "starting_target_folder")}/models'
    if not Path(target_folder).exists():
        mkdir(target_folder)

    left_model_target = f'{target_folder}/{model_calc_name}_model_left.pkl'
    left_scaler_target = f'{target_folder}/{model_calc_name}_scaler_left.pkl'
    right_model_target = f'{target_folder}/{model_calc_name}_model_right.pkl'
    right_scaler_target = f'{target_folder}/{model_calc_name}_scaler_right.pkl'
    joblib.dump(left_model, left_model_target)
    joblib.dump(left_scalar, left_scaler_target)
    joblib.dump(right_model, right_model_target)
    joblib.dump(right_scalar, right_scaler_target)

    update_model_tracker(model_calc_name, 'ridgecv')


