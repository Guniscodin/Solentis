import discord
import random
import logging
from discord.ext import commands
from discord.ext import tasks
from discord.ui import button, view
from discord import app_commands
from dotenv import load_dotenv
import os
import json
from copy import deepcopy
import asyncio
import sys
# --- CONFIGURATION & SETUP ---

# IMPORTANT: You need the 'discord.Object' to sync guild commands
DEV_GUILD = discord.Object(id=1446549954268106884) 
sys.path.append(os.path.dirname(__file__))
import dataloader
load_dotenv()
handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
Token = os.getenv("DISCORD_TOKEN")
bot = commands.Bot(command_prefix="?", intents=intents) 
async def setup_hook():
    # 1️⃣ LOAD COGS FIRST
    await bot.load_extension("cog.roll")
    await bot.load_extension("cog.userinfo")
    await bot.load_extension("cog.serverinfo")
    await bot.load_extension("cog.Pillow")
    await bot.load_extension("cog.ban")
    await bot.load_extension("cog.kick")
    await bot.load_extension("cog.guess")
    await bot.load_extension("cog.timeout")
    await bot.load_extension("cog.rate")
    await bot.load_extension("cog.clear")
    await bot.load_extension("cog.coinflip")
    await bot.load_extension("cog.assign")
    await bot.load_extension("cog.truth")
    await bot.load_extension("cog.dare")
    await bot.load_extension("cog.mining.register")
    await bot.load_extension("cog.mining.inventory")
    await bot.load_extension("cog.mining.pickstats")
    await bot.load_extension("cog.mining.xpcheck")
    await bot.load_extension("cog.mining.stash")
    await bot.load_extension("cog.mining.sellall")
    await bot.load_extension("cog.mining.buyrank")
    await bot.load_extension("cog.mining.enterlumina")
    await bot.load_extension("cog.mining.secretrank")
    await bot.load_extension("cog.mining.sellthis")
    await bot.load_extension("cog.mining.oresmined")
    await bot.load_extension("cog.mining.buypick")
    await bot.load_extension("cog.mining.mine")

    # 2️⃣ THEN SYNC SLASH COMMANDS
    synced = await bot.tree.sync(guild=DEV_GUILD)
    print(f"[OK] Synced {len(synced)} guild command(s)")

bot.setup_hook = setup_hook

async def main():
    async with bot:
        await bot.load_extension("cog.roll")
        await bot.load_extension("cog.userinfo")
        await bot.load_extension("cog.serverinfo")
        await bot.load_extension("cog.Pillow")
        await bot.load_extension("cog.guess")
        await bot.load_extension("cog.timeout")
        await bot.load_extension("cog.ban")
        await bot.load_extension("cog.clear")
        await bot.load_extension("cog.kick")
        await bot.load_extension("cog.rate")
        await bot.load_extension("cog.coinflip")
        await bot.load_extension("cog.assign")
        await bot.load_extension("cog.truth")
        await bot.load_extension("cog.dare")
        await bot.load_extension("cog.mining.register")
        await bot.load_extension("cog.mining.inventory")
        await bot.load_extension("cog.mining.pickstats")
        await bot.load_extension("cog.mining.xpcheck")
        await bot.load_extension("cog.mining.stash")
        await bot.load_extension("cog.mining.sellall")
        await bot.load_extension("cog.mining.buyrank")
        await bot.load_extension("cog.mining.enterlumina")
        await bot.load_extension("cog.mining.secretrank")
        await bot.load_extension("cog.mining.sellthis")
        await bot.load_extension("cog.mining.oresmined")
        await bot.load_extension("cog.mining.buypick")
        await bot.load_extension("cog.mining.mine")
        await bot.start()

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

# --- EVENTS ---

@bot.event 
async def on_member_join(member):
    channel = member.guild.get_channel(1455057285364846864)
    if channel:
        # NOTE: Changed ?info to /info
        embed = discord.Embed(
            title="Welcome to Solace!",
            description="You can type /serverinfo for server info ℹ",
            color=discord.Color.gold()
        )
        embed.set_thumbnail(
            url=member.guild.icon.url
        )
        embed.set_footer(
            text="Welcome to solace check out #bot-commands!",
            icon_url=member.display.url
        )
        await channel.send(embed)

@bot.event
async def on_command_error(ctx, error):
    # This event handler is for old prefix commands (e.g., "?command")
    # Slash command errors are handled differently (usually in command try/except blocks)
    if isinstance(error,commands.MissingRequiredArgument):
        await ctx.send(f'{ctx.author.mention} - Hey! you missed something maybe 😐 ?')
    elif isinstance(error,commands.MemberNotFound):
        await ctx.send(f'{ctx.author.mention} - Uh ? I think hes/shes not here.... 🤨 ')
    elif isinstance(error,commands.RoleNotFound):
        await ctx.send(f'{ctx.author.mention} - Which role is that ??? lol 😄 ')
    else:
        await ctx.send(f' {ctx.author.mention} Something went wrong here sorry {error}')

# --- TASK (Loop) REMAINS THE SAME ---

@tasks.loop(minutes=30)
async def update_shop():
    # ... (Your original update_shop logic remains here)
    try:
        with open("pickaxe.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        logging.error("pickaxe.json not found for update_shop")
        return

    shop_items = []
    emojis = {
        "common": "⚪",
        "uncommon": "🟢",
        "rare": "🔵",
        "epic": "🟣",
        "legendary": "🟡",
        "mythical": "🟥",
        "transcendent": "✨"
    }

    for _ in range(5):
        roll = random.randint(1, 10000)

        if roll <= 100:           # 1% chance
            rarity = "transcendent"
        elif roll <= 500:         # 4% chance
            rarity = "mythical"
        elif roll <= 1000:        # 5% chance
            rarity = "legendary"
        elif roll <= 2000:        # 10% chance
            rarity = "epic"
        elif roll <= 4000:        # 20% chance
            rarity = "rare"
        elif roll <= 7000:        # 30% chance
            rarity = "uncommon"
        else:                     # remaining 30%
            rarity = "common"   
        
        # Ensure the rarity key exists and has items
        if rarity in data and data[rarity]:
            item = random.choice(data[rarity])  
        else:
             logging.warning(f"No items found for rarity: {rarity}")
             continue


        shop_items.append({
            "rarity": rarity,
            "item": item    # storing the whole object
        })
    
    try:
        with open("shop.json","w",encoding="utf-8") as f:
            json.dump(shop_items,f,indent=4)

        # NOTE: Using bot.get_channel is safer in a task loop than relying on interaction context
        channel = bot.get_channel(1448277263907819530)
        if channel is None:
             logging.error("Shop channel not found.")
             return

        msg = "**🛒 SHOP RESET!**\n\n"
        for s in shop_items:
            rarity = s["rarity"]
            name = s["item"]["name"]
            price = s["item"]["price"]

            msg += f"{emojis[rarity]} **[{rarity.upper()}]** — `{name}` — 💰 {price:,}\n\n"

        await channel.send(msg)
    except Exception as e:
        logging.error(f"SHOP RESET ERROR : {e}")
    
    


# --- BOT RUNNING ---

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} ({bot.user.id})")
    print("Bot is ready!")
    
    # 1. Define the ID
    channel_id = 1446549955031466046
    
    # 2. Get the channel object using the ID
    channel = bot.get_channel(channel_id)
    
    # 3. Check if the channel exists, then send
    # if channel:
    #     embed = discord.Embed(
    #         title="I am Here!",
    #         description="Type `/` to see all commands",
    #         color=discord.Color.red()
    #     )
    #     await channel.send(embed=embed)
    # else:
    #     print(f"Could not find channel with ID {channel_id}")

    # Start your loop
    if not update_shop.is_running():
        update_shop.start()

async def main():
    async with bot:
        await bot.start(Token)

asyncio.run(main())

bot.run(Token, log_handler=handler, log_level=logging.DEBUG)