import discord
from discord.ext import commands
from discord import app_commands
import json
import os
import random
import logging
DEV_GUILD_ID = 1446549954268106884  # your dev server ID (int)

class Buyrank(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="buyrank",
        description="Buy a rank!"
    )
    @app_commands.checks.cooldown(1,2.0)
    @app_commands.guilds(DEV_GUILD_ID)  # instant dev sync
    async def buyRank(self,interaction: discord.Interaction, rank_name: str):
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

        msg = rank_name.strip().lower()
        lumina_ranks = {
            "lumina explorer": 1000000,
            "prospector": 3000000,
            "lumina elite": 10000000,
            "overseer": 15000000
        }

        try:
            if os.path.exists(f"{interaction.user.id}.json"):
                with open(f"{interaction.user.id}.json","r",encoding="utf-8") as f:
                    data = json.load(f)
                    current_rank = data["rank"].strip().lower().replace("⚓", "").replace("!", "")
                    coins = data["coins"]
                
                if msg not in lumina_ranks:
                    rank_not_available = discord.Embed(
                        title="Rank not available! ⚔",
                        color=discord.Color.red()
                    )
                    rank_not_available.set_footer(
                        icon_url=interaction.user.display_avatar.url
                    )
                    await interaction.followup.send(content=interaction.user.mention,embed=rank_not_available, ephemeral=True)
                    return

                if current_rank == msg:
                    rank_already_available = discord.Embed(
                        title="Rank already owned! ⚔",
                        color=discord.Color.red()
                    )
                    rank_already_available.set_footer(
                        icon_url=interaction.user.display_avatar.url
                    )
                    await interaction.followup.send(content=interaction.user.mention,embed=rank_already_available, ephemeral=True)
                    return

                price = lumina_ranks[msg]
                if coins >= price:
                
                    # Check for rank progression (e.g. can't buy Elite without Explorer/Prospector first, if that's the intention)
                    # NOTE: I am not adding explicit progression checks, assuming they can buy any rank listed.
                
                    new_rank = msg.capitalize() + "⚓"
                    coins -= price
                    data["coins"] = coins
                    data["rank"] = new_rank
                
                    with open(f"{interaction.user.id}.json","w",encoding="utf-8") as f_update:
                        json.dump(data,f_update,indent=4)
                    
                    success_embed = discord.Embed(
                        title=f"Rank Unlocked! **{new_rank}**",
                        color=discord.Color.dark_gold()
                    )
                    success_embed.set_footer(
                        icon_url=interaction.user.display_avatar.url
                    )
                    await interaction.followup.send(content=interaction.user.mention,embed=success_embed)
                else:
                    no_coins = discord.Embed(
                        title="Not enough coins! 💸",
                        description="Grind more brokie.....",
                        color=discord.Color.red()
                    )
                    no_coins.set_footer(
                        icon_url=interaction.user.display_avatar.url
                    )
                    await interaction.followup.send(content=interaction.user.mention,embed=no_coins, ephemeral=True)
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
            await interaction.followup.send(f"{interaction.user.mention} - Something went wrong, please try again later! 🕷", ephemeral=True)
            logging.error(f"Error in buy rank command: {e}")

async def setup(bot: commands.Bot):
    await bot.add_cog(Buyrank(bot))
