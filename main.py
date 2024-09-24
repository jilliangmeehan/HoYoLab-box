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
