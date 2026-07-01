import discord
from discord.ext import commands
from discord import app_commands
import json
import logging
import random
import os
DEV_GUILD_ID = 1446549954268106884  # your dev server ID (int)

class oresmined(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="oresmined",
        description="Check the amount of ores you mined!"
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
                with open(f"{interaction.user.id}.json","r",encoding="utf-8")as f:
                    data = json.load(f)
                    ores_mined = data["ores_mined"]
                    main_embed = discord.Embed(
                        title="You have mined a total of...",
                        description=f"⭐ {ores_mined} ores",
                        color=discord.Color.gold()
                    )
                    main_embed.set_footer(
                        text="Start mining by typing `/mine` ",
                        icon_url=interaction.user.display_avatar.url
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
            logging.error(f"Ores mined command error: {e}")

async def setup(bot: commands.Bot):
    await bot.add_cog(oresmined(bot))
