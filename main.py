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
        # Print the entire response for debugging
        print("API Response:")
        print(json.dumps(json_data, indent=2))
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
    
    print(f"Formatting stats for {game_name}:")
    print(json.dumps(game, indent=2))
    
    stats = {item['name']: item['value'] for item in game['data']}
    
    def get_stat(keys):
        for key in keys:
            if key in stats:
                return stats[key]
        return "N/A"

    if game_id == 2:  # Genshin Impact
        return f"🎮 {game_name}\n"\
               f"⚔️ Lv.{level}\n"\
               f"🕹️ Active Days: {get_stat(['Active Days', 'Days Active', '活跃天数'])}\n"\
               f"🤝 Characters: {get_stat(['Characters', 'Characters Obtained', '获得角色数'])}\n"\
               f"🏆 Achievements: {get_stat(['Achievements', 'Achievements Unlocked', '成就达成数'])}\n"\
               f"🌟 Spiral Abyss: {get_stat(['Spiral Abyss', 'Spiral Abyss Progress', '深境螺旋'])}\n"
    
    elif game_id == 1:  # Honkai Impact 3rd
        return f"🎮 {game_name}\n"\
               f"⚔️ Lv.{level}\n"\
               f"🕹️ Total Check-ins: {get_stat(['Total Check-ins', 'Cumulative Check-in Days', '累计登舰'])}\n"\
               f"🛡️ Battlesuits: {get_stat(['Battlesuits', 'Battlesuit Count', '装甲数'])}\n"\
               f"👗 Outfits: {get_stat(['Outfits', 'Outfit Count', '服装数'])}\n"\
               f"🌀 Quantum Singularity: {get_stat(['Quantum Singularity', 'Quantum Singularity Progress', '量子流形'])}\n"
    
    elif game_id == 6:  # Honkai: Star Rail
        return f"🎮 {game_name}\n"\
               f"⚔️ Lv.{level}\n"\
               f"🕹️ Active Days: {get_stat(['Active Days', 'Days Active', '活跃天数'])}\n"\
               f"🤝 Characters: {get_stat(['Characters', 'Characters Obtained', '已解锁角色'])}\n"\
               f"🏆 Achievements: {get_stat(['Achievements', 'Achievements Unlocked', '达成成就数'])}\n"\
               f"🎁 Chests Opened: {get_stat(['Chests Opened', 'Treasures Opened', '战利品开启'])}\n"
    
    elif game_id == 8:  # Zenless Zone Zero
        return f"🎮 {game_name}\n"\
               f"⚔️ Lv.{level}\n"\
               f"🕹️ Active Days: {get_stat(['Days Active', 'Active Days', '活跃天数'])}\n"\
               f"🏆 Achievements: {get_stat(['No. of Achievements Earned', 'Achievements', '达成成就数'])}\n"\
               f"🤝 Agents: {get_stat(['Agents Recruited', 'Characters', '已解锁角色'])}\n"\
               f"🐰 Bangboo: {get_stat(['Bangboo Obtained', 'Bangboo', '战利品开启'])}\n"
    
    else:  # Generic format for unknown games
        return f"🎮 {game_name}\n"\
               f"⚔️ Lv.{level}\n"\
               + "\n".join(f"{key}: {value}" for key, value in stats.items())

# ... rest of the script remains the same
