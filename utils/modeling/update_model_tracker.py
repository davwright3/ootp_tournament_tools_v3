import os
import json
import datetime
from utils.config_utils.load_save_settings import get_setting

def update_model_tracker(
        model_name,
        model_type,
        trny_name
):
    target_folder = f'{get_setting("InitialTargetDirs", "starting_target_folder")}/models'

    json_filepath = f'{target_folder}/model_tracking.json'

    if os.path.exists(json_filepath) and os.path.isfile(json_filepath):
        with open(json_filepath, 'r') as f:
            model_data = json.load(f)
    else:
        model_data = {}

    if model_data is None:
        model_data = {}

    model_data[f'current_{model_name}'] = model_type
    model_data[f'current_{model_name}_runtime'] = datetime.datetime.now().isoformat()
    if trny_name is not None:
        model_data[f'current_{model_name}_tourney_name'] = trny_name
    else:
        model_data[f'current_{model_name}_tourney_name'] = 'Unknown'

    with open(json_filepath, 'w', encoding='utf-8') as f:
        json.dump(model_data, f, indent=4, sort_keys=True)

