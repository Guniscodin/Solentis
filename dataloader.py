import json

try:
    with open("pickaxe.json", "r", encoding="utf-8") as f_pick:
        data_pick = json.load(f_pick)
    with open("ores.json", "r", encoding="utf-8") as f_ores:
        ore_data = json.load(f_ores)
    with open("shop.json", "r", encoding="utf-8") as f_shop:
        shop = json.load(f_shop)

    all_shop_items = {}
    shop_items_name = []
    for shop_item in shop:
        item = shop_item["item"]
        all_shop_items[item["name"]] = shop_item
        shop_items_name.append({"name": item["name"], "price": item["price"]})

    all_picks = {}
    for pick_list in data_pick.values():
        for each_pick in pick_list:
            all_picks[each_pick["name"]] = each_pick

    all_ores = {}
    for rarity, sub in ore_data.items():
        for level in ["low", "high"]:
            for ore in sub[level]:
                all_ores[ore["name"]] = ore

    with open("oresNames.json") as f:
        picks = json.load(f)

    common_low = picks["common"]["low"]
    common_high = picks["common"]["high"]
    uncommon_low = picks["uncommon"]["low"]
    uncommon_high = picks["uncommon"]["high"]
    rare_low = picks["rare"]["low"]
    rare_high = picks["rare"]["high"]
    epic_low = picks["epic"]["low"]
    epic_high = picks["epic"]["high"]
    legendary_low = picks["legendary"]["low"]
    legendary_high = picks["legendary"]["high"]
    mythical_low = picks["mythical"]["low"]
    mythical_high = picks["mythical"]["high"]
    forbidden_low = picks["forbidden"]["low"]
    forbidden_high = picks["forbidden"]["high"]
    
except FileNotFoundError as e:
    print(f"CRITICAL ERROR: Missing necessary JSON file: {e}. Bot may not function correctly.")
    # You might want to exit here or handle it differently