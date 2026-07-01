import discord
from discord.ext import commands
from discord import app_commands
import json
import random
import dataloader
import os
import logging
DEV_GUILD_ID = 1446549954268106884  # your dev server ID (int)

class sellall(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="sellall",
        description="Sell all your ores!"
    )
    @app_commands.checks.cooldown(1,2.0)
    @app_commands.guilds(DEV_GUILD_ID)  # instant dev sync
    async def example(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False, thinking=True)

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
            if os.path.exists(f"{interaction.user.id}.json"):
                total_amount_to_send = 0
            
                with open(f"{interaction.user.id}.json","r",encoding="utf-8") as f:
                    data = json.load(f)
                    stash_all_ores = data["stash"]
                    coins = data["coins"]
                
                    # Calculate sales and update coins
                    for ore, amount in stash_all_ores.items():
                        if not isinstance(amount,(int,float)):
                            continue
                        if ore not in dataloader.all_ores:
                            continue
                    
                        current_ore = dataloader.all_ores[ore]
                        current_ore_value = current_ore["value"]
                        total_amount = current_ore_value * amount
                        coins += total_amount
                        total_amount_to_send += total_amount
                
                    data["coins"] = coins

                    # Reset stash (after calculating total)
                    for ores, amounts in stash_all_ores.items():
                        if isinstance(amounts, (int, float)):
                            stash_all_ores[ores] = 0

                    random_xp = random.randint(1,500)
                    data["stash"] = stash_all_ores
                    data["xp"] += random_xp
                
                with open(f"{interaction.user.id}.json","w",encoding="utf-8") as f_final:
                    json.dump(data,f_final,indent=4)
                
                main_embed = discord.Embed(
                    title="Stash sold 💰📦!",
                    description=f"You earned **{total_amount_to_send:,}** Coins 💸 \n\n And a total of **{random_xp} Xp 🍀**",
                    color=discord.Color.dark_red()
                )
                main_embed.set_footer(
                    text="Great! keep on mining ⛏",
                    icon_url=interaction.user.display_avatar.url
                )
                main_embed.set_thumbnail(
                    url=interaction.user.display_avatar.url
                )

                await interaction.followup.send(content=interaction.user.mention,embed=main_embed)

            else:
                register_embed = discord.Embed(
                    title="**Join The Mines! ⛏⚒!**",
                    description="To use this command please register using `/register`! And join the mines",
                    color=discord.Color.gold()
                )
                register_embed.set_footer(
                    text="Join now!",
                    icon_url=interaction.user.display_avatar.url
                )
                register_embed.set_thumbnail(
                    url=interaction.user.display_avatar.url
                )
                await interaction.followup.send(content=interaction.user.mention,embed=register_embed, ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"{interaction.user.mention}- Something went wrong please try again later!🕷", ephemeral=True)
            logging.error(f"Sell all error: {e}")
            print(f"sell all command error {e}")

async def setup(bot: commands.Bot):
    await bot.add_cog(sellall(bot))
