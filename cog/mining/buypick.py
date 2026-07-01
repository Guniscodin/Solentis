import discord
from discord.ext import commands
from discord import app_commands
import json
import os
import random
import logging
from copy import deepcopy
DEV_GUILD_ID = 1446549954268106884  # your dev server ID (int)

class buypick(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="buypick",
        description="Buy your new pickaxe !"
    )
    @app_commands.checks.cooldown(1,2.0)
    @app_commands.guilds(DEV_GUILD_ID)  # instant dev sync
    async def buy(self,interaction: discord.Interaction, item_name: str):
        await interaction.response.defer(ephemeral=False, thinking=True)
        msg = item_name.strip()
    
        allowed_channels = [1455195010126315655]
        if interaction.channel_id not in allowed_channels:
            channel_embed = discord.Embed(
                title="Wrong channel!",
                description="Try this is #game-commands ⛏ channel!",
                color=discord.Color.red()
            )
            await interaction.followup.send(content=interaction.user.mention,embed=channel_embed, ephemeral=True)
            return
    
        try:
            if not os.path.exists(f"{interaction.user.id}.json"):
                await interaction.followup.send(f"{interaction.user.mention} -- Please register using `/register` to use this command ⚒.", ephemeral=True)
                return
   
            with open(f"{interaction.user.id}.json", "r", encoding="utf-8") as f:
                data = json.load(f)
    
            coins = data["coins"]

        # Helper to clean pickaxe names (removes emojis)
            def clean_name(name):
                for icon in ["⛏","🔧","🔮","💎","🚀","🌌","🔱"]:
                    name = name.replace(icon, "")
                return name.strip().lower()

            msg_clean = clean_name(msg)
            thing = None
            price = 0

   
            # Reload shop data just in case the task ran
            with open("shop.json", "r", encoding="utf-8") as f_shop:
                shop = json.load(f_shop)

            # Find the item in the shop
            shop_item_found = None
            for shop_item in shop:
                item = shop_item["item"]
                if clean_name(item["name"]) == msg_clean:
                    shop_item_found = shop_item
                    thing = item["name"]
                    price = item["price"]
                    break

            if not thing:
                item_not_available = discord.Embed(
                    title="Item not available! ⚔",
                    color=discord.Color.red()
                )
                item_not_available.set_footer(
                    icon_url=interaction.user.display_avatar.url
                )
                await interaction.followup.send(content=interaction.user.mention,embed=item_not_available, ephemeral=True)
                return

            if price > coins:
                no_coins = discord.Embed(
                    title="Not enough coins! 💸",
                    description="Grind more brokie.....",
                    color=discord.Color.red()
                )
                no_coins.set_footer(
                    icon_url=interaction.user.display_avatar.url
                )
                await interaction.followup.send(content=interaction.user.mention,embed=no_coins, ephemeral=True)
                return

            # Execute purchase
            coins -= price
            data["coins"] = coins

            # Update pickaxe with a deep copy of the shop item's data
            if shop_item_found:
                data["pickaxe"] = deepcopy(shop_item_found["item"])
            else:
                await interaction.followup.send(f"{interaction.user.mention} -- Internal error finding item after check. Contact Caretaker.", ephemeral=True)
                return

            with open(f"{interaction.user.id}.json", "w", encoding="utf-8") as f_updated:
                json.dump(data, f_updated, indent=4)
            
            success_embed = discord.Embed(
                title=f"Just bought {thing}",
                description="Have fun mining with that pickaxe 😋!",
                color=discord.Color.dark_gold()
            )
            success_embed.set_footer(
                text="Bought by",
                icon_url=interaction.user.display_avatar.url
            )
            success_embed.set_thumbnail(
                url=interaction.user.display_avatar.url
            )

            await interaction.followup.send(content=interaction.user.mention,embed=success_embed)
        except Exception as e:
            await interaction.followup.send(f"{interaction.user.mention}- Something went wrong please try again later!🕷", ephemeral=True)
            logging.error(f"Buy command error: {e}")

async def setup(bot: commands.Bot):
    await bot.add_cog(buypick(bot))
