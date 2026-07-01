import discord
from discord.ext import commands
from discord import app_commands
import os
import json
import logging
from PIL import Image
DEV_GUILD_ID = 1446549954268106884  # your dev server ID (int)

class inv(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="inventory",
        description="check your current inventory!"
    )
    @app_commands.checks.cooldown(1,2.0)
    @app_commands.guilds(DEV_GUILD_ID)  # instant dev sync
    async def inv_command(self, interaction: discord.Interaction):
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

                inventory_msg = discord.Embed(
                    title=f"📦 **Your Inventory** 📦",
                    color=discord.Color.gold()
                )
                inventory_msg.add_field(name="⭐ Level", value=data['lvl'], inline=False)
                inventory_msg.add_field(name="🪓 Pickaxe", value=data['pickaxe']['name'], inline=False)
                inventory_msg.add_field(name="🥉 Rank", value=data['rank'].capitalize(), inline=False)
                inventory_msg.add_field(name="🎒 Max Stash", value=data['max_stash'], inline=False)
                inventory_msg.add_field(name="💰 Coins", value=f"{data.get('coins',0):,}", inline=False)
                inventory_msg.add_field(name="⭐ XP", value=f"{data['xp']}/{data['xp_required']}", inline=False) 
                
                inventory_msg.set_footer(
                    text="Type /mine to start mining",
                    icon_url=interaction.user.display_avatar.url
                )
                inventory_msg.set_thumbnail(
                    url=interaction.user.display_avatar.url
                )
                await interaction.followup.send(content=interaction.user.mention,embed=inventory_msg)
            except Exception as e:
                await interaction.followup.send(f"{interaction.user.mention}-- Error loading inventory: {e} 🕷", ephemeral=True)
                logging.error(f"Inv command error for {interaction.user.id}: {e}")
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
    await bot.add_cog(inv(bot))
