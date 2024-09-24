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

    return json_data['data']['list']

def format_game_stats(game):
    game_id = game['game_id']
    game_name = game['game_name']
    level = game['level']
    
    stats = {item['name']: item['value'] for item in game['data']}
    
    def get_stat(cn_key, en_key):
        return stats.get(cn_key) or stats.get(en_key) or "N/A"

    if game_id == 2:  # Genshin Impact
        return f"🎮 {game_name}\n"\
               f"⚔️ Lv.{level}\n"\
               f"🕹️ Active Days: {get_stat('活跃天数', 'Active Days')}\n"\
               f"🤝 Characters: {get_stat('获得角色数', 'Characters')}\n"\
               f"🏆 Achievements: {get_stat('成就达成数', 'Achievements')}\n"\
               f"🌟 Spiral Abyss: {get_stat('深境螺旋', 'Spiral Abyss')}\n"
    
    elif game_id == 1:  # Honkai Impact 3rd
        return f"🎮 {game_name}\n"\
               f"⚔️ Lv.{level}\n"\
               f"🕹️ Total Check-ins: {get_stat('累计登舰', 'Total Check-ins')}\n"\
               f"🛡️ Battlesuits: {get_stat('装甲数', 'Battlesuits')}\n"\
               f"👗 Outfits: {get_stat('服装数', 'Outfits')}\n"\
               f"🌀 Quantum Singularity: {get_stat('量子流形', 'Quantum Singularity')}\n"
    
    elif game_id == 6:  # Honkai: Star Rail
        return f"🎮 {game_name}\n"\
               f"⚔️ Lv.{level}\n"\
               f"🕹️ Active Days: {get_stat('活跃天数', 'Active Days')}\n"\
               f"🤝 Characters: {get_stat('已解锁角色', 'Characters')}\n"\
               f"🏆 Achievements: {get_stat('达成成就数', 'Achievements')}\n"\
               f"🎁 Chests Opened: {get_stat('战利品开启', 'Chests Opened')}\n"
    
    elif game_id == 8:  # Zenless Zone Zero
        return f"🎮 {game_name}\n"\
               f"⚔️ Lv.{level}\n"\
               f"🕹️ Active Days: {get_stat('活跃天数', 'Days Active')}\n"\
               f"🏆 Achievements: {get_stat('达成成就数', 'No. of Achievements Earned')}\n"\
               f"🤝 Agents: {get_stat('已解锁角色', 'Agents Recruited')}\n"\
               f"🐰 Bangboo: {get_stat('战利品开启', 'Bangboo Obtained')}\n"
    
    else:  # Generic format for unknown games
        return f"🎮 {game_name}\n"\
               f"⚔️ Lv.{level}\n"\
               + "\n".join(f"{key}: {value}" for key, value in stats.items())

def update_gist(gh_api_url, gh_token, gist_id, hoyo_data):
    if not hoyo_data:
        print("Error: No data to update gist")
        return

    str_hoyo_data = ""
    for game in hoyo_data:
        str_hoyo_data += format_game_stats(game) + "\n"

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
