import requests
import os
import json

def get_data_from_hoyolab(hoyo_uid, hoyo_token, hoyo_tmid):
    headers = {
        'x-rpc-language': 'en-us',
        'Cookie': f'ltoken_v2={hoyo_token}; ltmid_v2={hoyo_tmid};'
    }

    url = f'https://bbs-api-os.hoyolab.com/game_record/card/wapi/getGameRecordCard?uid={hoyo_uid}'
    
    response = requests.get(url=url, headers=headers)
    if response.status_code != 200:
        print(f"Error: API request failed with status code {response.status_code}")
        return None

    try:
        json_data = response.json()
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON response")
        return None

    if 'data' not in json_data or 'list' not in json_data['data']:
        print("Error: Unexpected JSON structure")
        return None

    return_list = []
    for game in json_data['data']['list']:
        game_data = [game['game_name']]
        game_data.append(str(game['level']))
        for item in game['data']:
            game_data.append(item['value'])
        return_list.append(game_data)

    return return_list

def update_gist(gh_api_url, gh_token, gist_id, hoyo_data):
    if not hoyo_data:
        print("Error: No data to update gist")
        return

    padding = ' '
    str_hoyo_data = ''
    for game in hoyo_data:
        game_name = game[0]
        level = game[1]
        active_days = game[2]
        characters = game[3]
        achievements = game[4]
        extra_stat = game[5] if len(game) > 5 else ""

        str_hoyo_data += f'🎮 {game_name}\n'\
            f'⚔️ Lv.{level.rjust(3, padding)}'\
            f'🤝 {characters.rjust(3, padding)} chars'\
            f'🕹️ {active_days.rjust(4, padding)} days'\
            f'🏆 {achievements.rjust(4, padding)} achvmnts'
        
        if extra_stat:
            str_hoyo_data += f'🌟 {extra_stat}'
        
        str_hoyo_data += '\n\n'

    data = {
        'description': '🎮 HoYoverse gameplay stats',
        'files': {'🎮 HoYoverse gameplay stats': {'content': str_hoyo_data}}
    }

    try:
        response = requests.patch(
            url=f'{gh_api_url}/gists/{gist_id}',
            headers={
                'Authorization': f'token {gh_token}',
                'Accept': 'application/json'
            },
            json=data
        )
        response.raise_for_status()
        print("Gist updated successfully!")
    except requests.exceptions.RequestException as e:
        print(f"Error updating gist: {e}")

if __name__ == '__main__':
    hoyo_uid = os.environ['HOYO_UID']
    hoyo_token = os.environ['HOYO_TOKEN']
    hoyo_tmid = os.environ['HOYO_TMID']
    gh_token = os.environ['GH_TOKEN']
    gist_id = os.environ['GIST_ID']
    gh_api_url = 'https://api.github.com'

    hoyo_data = get_data_from_hoyolab(hoyo_uid, hoyo_token, hoyo_tmid)
    if hoyo_data:
        update_gist(gh_api_url, gh_token, gist_id, hoyo_data)
    else:
        print("Failed to retrieve data from HoYoLab")
