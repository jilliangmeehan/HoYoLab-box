import requests
import os
import json
import sys

def log_message(message):
    print(message, file=sys.stderr)

def get_only_data_needed(userInfoInGame, list_to_return):
    try:
        list_to_return[-1].append(str(userInfoInGame['level']))
        for eachData in userInfoInGame['data']:
            if 'Active' in eachData['name']:
                list_to_return[-1].append(eachData['value'])
            elif 'Characters' in eachData['name']:
                list_to_return[-1].append(eachData['value'])
            elif 'Achievements' in eachData['name']:
                list_to_return[-1].append(eachData['value'])
    except KeyError as e:
        log_message(f"Error: Missing key in userInfoInGame: {e}")
        return None
    return list_to_return

def get_data_from_hoyolab(hoyo_uid, hoyo_token, hoyo_tmid):
    headers = {
        'x-rpc-language': 'en-us',
        'Cookie': f'ltoken_v2={hoyo_token}; ltmid_v2={hoyo_tmid};'
    }

    url = f'https://bbs-api-os.hoyolab.com/game_record/card/wapi/getGameRecordCard?uid={hoyo_uid}'
    
    try:
        requestData = requests.get(url=url, headers=headers)
        requestData.raise_for_status()
    except requests.exceptions.RequestException as e:
        log_message(f"Error making request to HoYoLab API: {e}")
        return None

    try:
        jsonData = requestData.json()
    except json.JSONDecodeError:
        log_message("Error: Failed to decode JSON response")
        return None

    if 'data' not in jsonData or 'list' not in jsonData['data']:
        log_message("Error: Unexpected JSON structure")
        log_message(f"JSON Data: {json.dumps(jsonData, indent=2)}")
        return None

    return_list = []
    for eachGame in jsonData['data']['list']:
        if eachGame['game_id'] == 2:
            return_list.append(['Genshin Impact'])
            return_list = get_only_data_needed(eachGame, return_list)
        elif eachGame['game_id'] == 6:
            return_list.append(['Honkai: Star Rail'])
            return_list = get_only_data_needed(eachGame, return_list)
        
        if return_list[-1] is None:
            return None

    return return_list if return_list else None

def update_gist(gh_api_url, gh_token, gist_id, hoyo_data):
    if not hoyo_data:
        log_message("Error: No data to update gist")
        return

    padding = ' '
    for i in range(1, len(hoyo_data[0])):
        len_for_padding = max(len(hoyo_data[0][i]), len(hoyo_data[1][i]))
        hoyo_data[0][i] = hoyo_data[0][i].rjust(len_for_padding, padding)
        hoyo_data[1][i] = hoyo_data[1][i].rjust(len_for_padding, padding)

    str_hoyo_data = ''
    for game in hoyo_data:
        str_hoyo_data += '🎮 ' + game[0] + '\n'\
            + ('⚔️ Lv.' + game[1]).ljust(13, padding)\
            + ('🤝 ' + game[3] + ' chars').ljust(12, padding)\
            + ('🕹️ ' + game[2] + ' days').ljust(13, padding)\
            + ('🏆 ' + game[4] + ' achvmnts').ljust(12, padding)\
            + '\n\n'

    data = {
        'description': '🎮 HoYoverse gameplay stats',
        'files': {'🎮 HoYoverse gameplay stats': {'content': str_hoyo_data}}
    }

    try:
        request = requests.patch(
            url=f'{gh_api_url}/gists/{gist_id}',
            headers={
                'Authorization': f'token {gh_token}',
                'Accept': 'application/json'
            },
            json=data
        )
        request.raise_for_status()
    except requests.exceptions.RequestException as e:
        log_message(f"Error updating gist: {e}")
        return 'Error updating gist'

if __name__ == '__main__':
    required_env_vars = ['HOYO_UID', 'HOYO_TOKEN', 'HOYO_TMID', 'GH_TOKEN', 'GIST_ID']
    missing_vars = [var for var in required_env_vars if not os.environ.get(var)]
    
    if missing_vars:
        log_message(f"Error: Missing required environment variables: {', '.join(missing_vars)}")
        sys.exit(1)

    hoyo_uid = os.environ['HOYO_UID']
    hoyo_token = os.environ['HOYO_TOKEN']
    hoyo_tmid = os.environ['HOYO_TMID']
    gh_token = os.environ['GH_TOKEN']
    gist_id = os.environ['GIST_ID']
    gh_api_url = 'https://api.github.com'

    hoyo_data = get_data_from_hoyolab(hoyo_uid, hoyo_token, hoyo_tmid)
    if hoyo_data is None:
        log_message("Error: Failed to retrieve data from HoYoLab")
        sys.exit(1)

    result = update_gist(gh_api_url, gh_token, gist_id, hoyo_data)
    if result == 'Error updating gist':
        sys.exit(1)

    log_message("Script completed successfully")
