import discord
from discord.ext import commands
from discord import app_commands
import os
import json
import logging
DEV_GUILD_ID = 1446549954268106884  # your dev server ID (int)

class pickstats(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="pickstats",
        description="Check your current pickaxes stats!"
    )
    @app_commands.checks.cooldown(1,2.0)
    @app_commands.guilds(DEV_GUILD_ID)  # instant dev sync
    async def pickstats(self,interaction: discord.Interaction):
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

        if os.path.exists(f"{interaction.user.id}.json"):
            try:
                with open(f"{interaction.user.id}.json", "r", encoding="utf-8") as f:
                    data = json.load(f)
            
                pick = data["pickaxe"]
                can_mine = pick["can_mine"]
                Name = pick["name"]
                rarity = pick["rarity"]
                value = pick["price"]
                main_embed = discord.Embed(
                    title="Here are your pickaxes stats!",
                    color=discord.Color.gold()
                )
                main_embed.add_field(
                    name="**Name** :", value=f"{Name}" , inline=False
                )
                main_embed.add_field(
                    name="**Rarity** :",value=f"✨ {rarity}",inline=False
                )
                main_embed.add_field(
                    name="**Value** :",value=f"💲 {value:,}"
                )
                main_embed.set_footer(
                    text="For more info check your Dm 📧",
                    icon_url=interaction.user.display_avatar.url
                )
                await interaction.followup.send(
                    content=interaction.user.mention,
                    embed=main_embed
                )
                pretty_list = "\n".join([f"- {ore}" for ore in can_mine])
                dm_embed = discord.Embed(
                    title="Your pickaxe can mine!",
                    description=f"{pretty_list}",
                    color=discord.Color.red()
                )
                await interaction.user.send(content=interaction.user.mention,embed=dm_embed)
        
            except discord.Forbidden:
                dm_closed = discord.Embed(
                    title="YourDm is closed!",
                    description="I cant sen you the full list of mineable ores! 😞",
                    color=discord.Color.dark_red()
                )
                await interaction.followup.send(content=interaction.user.mention,embed=dm_closed, ephemeral=True)
            except Exception as e:
                await interaction.followup.send(f"{interaction.user.mention}-- Something went wrong please try again later!🕷", ephemeral=True)
                logging.error(f"Pickstats command error for {interaction.user.id}: {e}")
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

async def setup(bot: commands.Bot):
    await bot.add_cog(pickstats(bot))
