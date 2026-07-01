import discord
from discord.ext import commands
from discord import app_commands
import json 
import os
import random
import logging
DEV_GUILD_ID = 1446549954268106884  # your dev server ID (int)

class secretrank(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="secretrank",
        description="...."
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

        if "Lumina Explorer" in [role.name for role in interaction.user.roles]:
            try:
                with open(f"{interaction.user.id}.json") as f:
                    data = json.load(f)
                
                if data["ores_mined"] < 1000:
                    await interaction.followup.send(f"{interaction.user.mention} **Mine more! You need 1,000 ores! ⛏⚒** (Current: {data['ores_mined']})")
                elif data["lvl"] < 500:
                    await interaction.followup.send(f"{interaction.user.mention} You are not worthy of this Rank! You need to be **Level 500**! 🔱 (Current: {data['lvl']})")
                else:
                    # Rank Up Success
                    data["rank"] = '🌌 Lumina Legend 🔱'
                
                    with open(f"{interaction.user.id}.json","w") as f:
                        json.dump(data,f,indent=4)
                    
                    await interaction.followup.send(f"@everyone @here {interaction.user.mention} **Just got the Secret Rank, The secret Rank Quest will now be reset, Good luck finding out how to get the secret role again!** 🔥")
            except Exception as e:
                await interaction.followup.send(f"{interaction.user.mention}- Something went wrong please try again later!🕷", ephemeral=True)
                logging.error(f"SecretRank command error: {e}")
        else:
            await interaction.followup.send(f"{interaction.user.mention} You are not ready! ⚡ Yet.. You must be a 'Lumina Explorer' first.")

async def setup(bot: commands.Bot):
    await bot.add_cog(secretrank(bot))
