import json
import os
import pandas as pd
import requests

output_dir_roll_assignments = './output/rollAssignments'
output_dir_stream_group = './output/streamGroups'
headers = {
    'Accept': 'application/json, text/plain, */*',
    'Authorization': os.environ['HEADER_AUTHORIZATION']
}

def create_dir(path):
    if os.path.isdir(path):
        pass
    else:
        os.makedirs(path)

def create_default_output_dir():
    create_dir(output_dir_roll_assignments)
    create_dir(output_dir_stream_group)

def get_roll_assignments():
    df = pd.read_csv(f"./input/videos.csv")
    for row_value in df['guid']:
        r_rolls = requests.get(
            url=f"https://{os.environ['HEADER_AUTHORITY']}/api/videos/{row_value}/roleAssignments?$expand=Principal&adminmode=true&api-version=1.4-private",
            headers=headers
        )
        with open(f'./output/rollAssignments/{row_value}.json', 'w') as f:
            json.dump(r_rolls.json(), f, indent=2)
        print(f'rollAssignment saved. video:{row_value}')

        for roll in r_rolls.json()['value']:
            if all([
                roll['principal']['type'] == 'StreamGroup',
                roll['principal']['mail'] == None
            ]):
                print(f"StreamGroup founded. id={roll['principal']['id']};name={roll['principal']['name']}")
                create_dir(f"{output_dir_stream_group}/{roll['principal']['id']}")

                r_group_owners = requests.get(
                    url=f"https://{os.environ['HEADER_AUTHORITY']}/api/groups/{roll['principal']['id']}/owners?$top=100&$expand=Principal&adminmode=true&api-version=1.4-private",
                    headers=headers
                )
                with open(f"./output/streamGroups/{roll['principal']['id']}/owners.json", "w") as f:
                    json.dump(r_group_owners.json(), f, indent=2)
                
                r_group_contributors = requests.get(
                    url=f"https://{os.environ['HEADER_AUTHORITY']}/api/groups/{roll['principal']['id']}/contributors?$top=100&$expand=Principal&adminmode=true&api-version=1.4-private",
                    headers=headers
                )
                with open(f"./output/streamGroups/{roll['principal']['id']}/contributors.json", "w") as f:
                    json.dump(r_group_contributors.json(), f, indent=2)

                r_group_viewers = requests.get(
                    url=f"https://{os.environ['HEADER_AUTHORITY']}/api/groups/{roll['principal']['id']}/viewers?$top=100&$expand=Principal&adminmode=true&api-version=1.4-private",
                    headers=headers
                )
                with open(f"./output/streamGroups/{roll['principal']['id']}/viewers.json", "w") as f:
                    json.dump(r_group_viewers.json(), f, indent=2)

def main():
    create_default_output_dir()
    get_roll_assignments()

if __name__ == '__main__':
    main()

