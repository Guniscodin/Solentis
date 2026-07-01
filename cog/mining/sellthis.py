import discord
from discord.ext import commands
from discord import app_commands
import json
import os
import random
import logging
import dataloader
DEV_GUILD_ID = 1446549954268106884  # your dev server ID (int)

class sellthis(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="sellthis",
        description="Sell a specific ore! with a specific amount."
    )
    @app_commands.checks.cooldown(1,2.0)
    @app_commands.guilds(DEV_GUILD_ID)  # instant dev sync
    async def sellthis(self,interaction: discord.Interaction, ore_name: str, amount: int):
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
    
        if amount <= 0:
            embed_positive = discord.Embed(
                title="Error❌",
                description="Amount must be a positive number",
                color=discord.Color.red()
            )
            await interaction.followup.send(content=interaction.user.mention,embed=embed_positive, ephemeral=True)
            return

        ore = ore_name.strip()
    
        try:
            if os.path.exists(f"{interaction.user.id}.json"):
                with open(f"{interaction.user.id}.json","r",encoding="utf-8") as f:
                    data = json.load(f)
                    stash = data["stash"]

                    if ore not in stash or ore.startswith("**"): # Check if it's a valid sellable ore (not a category header)
                        await interaction.followup.send(f"{interaction.user.mention} -- Which ore is that? Check your stash with `/stash` 🤨 ", ephemeral=True)
                        return
                
                    if ore not in dataloader.all_ores:
                        await interaction.followup.send(f"{interaction.user.mention} -- Internal error: Ore value not found. Contact Caretaker.", ephemeral=True)
                        return

                    if stash[ore] < amount:
                        await interaction.followup.send(f"{interaction.user.mention}-- You don't even have that many bruh 😛 (You have {stash[ore]})", ephemeral=True)
                        return
                
                    # Execute sale
                    stash[ore] -= amount
                    ore_value = dataloader.all_ores[ore]["value"]
                    total_value = ore_value * amount
                    data["coins"] += total_value
                    data["stash"] = stash

                with open(f"{interaction.user.id}.json","w",encoding="utf-8") as f_update:
                    json.dump(data,f_update,indent=4)

                await interaction.followup.send(f"{interaction.user.mention}-- Sold **{amount}x {ore}**! You got a total of **{total_value:,}💸**")

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
            logging.error(f"Sell this error: {e}")

async def setup(bot: commands.Bot):
    await bot.add_cog(sellthis(bot))
