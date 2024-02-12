import json
import os
import pandas as pd
import requests
import traceback

from tqdm import tqdm

import stream_sc

def create_dir(path):
    if os.path.isdir(path):
        pass
    else:
        os.makedirs(path)

def export_json(data, path):
    # Skip if no data exists
    if not data:
        return

    with open(path, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def get_roll_assignments_and_groups():
    # Import CSV (video GUIDs)
    df = pd.read_csv(f"./input/videos.csv")
    s = stream_sc.Stream()

    exist_as_file = True
    for row_value in tqdm(df['guid']):
        try:
            export_file_path_rolls = f"{os.environ['OUTPUT_DIR_ROLL_ASSIGNMENTS']}/{row_value}.json"
            if os.path.isfile(export_file_path_rolls) and exist_as_file:
                with open(export_file_path_rolls) as f:
                    r_rolls = json.load(f)
            else:
                r_rolls = s.get_roll_assignments(row_value)
                export_json(r_rolls, export_file_path_rolls)

            if r_rolls is None:
                continue

            for roll in r_rolls['value']:
                if all([
                    roll['principal']['type'] == 'StreamGroup',
                    roll['principal']['mail'] == None
                ]):
                    print(f"[Debug] StreamOnlyGroup founded. id={roll['principal']['id']}; name={roll['principal']['name']}")
                    create_dir(f"{os.environ['OUTPUT_DIR_STREAM_GROUP']}/{roll['principal']['id']}")
                    group_id = roll['principal']['id']
                    # Get group owners info
                    export_file_path_group_owners = f"{os.environ['OUTPUT_DIR_STREAM_GROUP']}/{roll['principal']['id']}/owners.json"
                    if not os.path.isfile(export_file_path_group_owners) and exist_as_file:
                        r_group_owners = s.get_group_owners(group_id)
                        export_json(r_group_owners, export_file_path_group_owners)
                    # Get group contributors info
                    export_file_path_group_contributors = f"{os.environ['OUTPUT_DIR_STREAM_GROUP']}/{roll['principal']['id']}/contributors.json"
                    if not os.path.isfile(export_file_path_group_contributors) and exist_as_file:
                        r_group_contributors = s.get_group_contributors(group_id)
                        export_json(r_group_contributors, export_file_path_group_contributors)
                    # Get group viewers info
                    export_file_path_group_viewers = f"{os.environ['OUTPUT_DIR_STREAM_GROUP']}/{roll['principal']['id']}/viewers.json"
                    if not os.path.isfile(export_file_path_group_viewers) and exist_as_file:
                        r_group_viewers = s.get_group_viewers(group_id)
                        export_json(r_group_viewers, export_file_path_group_viewers)


        except KeyboardInterrupt:
            Exception('KeyboardInterrupt')
            return
        except:
            traceback.print_exc()
            print(f'[Error] Processing interrupted. video_id={row_value}')


def main():
    create_dir(os.environ['OUTPUT_DIR_ROLL_ASSIGNMENTS'])
    create_dir(os.environ['OUTPUT_DIR_STREAM_GROUP'])

    get_roll_assignments_and_groups()

if __name__ == '__main__':
    main()

