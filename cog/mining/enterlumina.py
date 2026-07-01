import discord
from discord.ext import commands
from discord import app_commands
import json 
import os
import logging
import random
DEV_GUILD_ID = 1446549954268106884  # your dev server ID (int)

class enterlumina(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="enterlumina",
        description="Enter the Lumina Tunnels!"
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
                with open(f"{interaction.user.id}.json","r",encoding="utf-8") as f:
                    data = json.load(f)
                    ores_mined = data["ores_mined"]
                    lvl = data["lvl"]
                    coins = data["coins"]
                    pick_rarity = data["pickaxe"]["rarity"]

                    requirments_false = []
                
                    # Requirements Check
                    if ores_mined < 100:
                        requirments_false.append(f"• You should have at least mined **100** ores to enter Lumina Tunnels🌠 (Current: {ores_mined})")
                
                    if coins < 1000000:
                        requirments_false.append(f"• You at least need **1,000,000** coins to enter Lumina Tunnels!🌠 (Current: {coins:,})")
                
                    if pick_rarity in ["common","uncommon"]:
                        requirments_false.append(f"• You should have at least a **rare** rarity pickaxe to enter Lumina Tunnels 🌠 (Current: {pick_rarity.capitalize()})")

                    if lvl < 100:
                        requirments_false.append(f"• You at least need to be level **100** or more to enter Lumina Tunnels 🌠 (Current: {lvl})")
                
                
                    if not requirments_false: # All requirements met
                        if data["area2_unlocked"] == True:
                            already_in = discord.Embed(
                                title="Your already in Lumina tunnels!",
                                color=discord.Color.blue()
                            )
                            already_in.set_footer(
                                icon_url=interaction.user.display_avatar.url
                            )
                            await interaction.followup.send(content=interaction.user.mention,embed=already_in,ephemeral=True)
                            return
                        
                        role = discord.utils.get(interaction.guild.roles, name="Lumina Explorer")
                        if role:
                            data["coins"] -= 1000000
                            data["area2_unlocked"] = True
                            data["rank"] = "Lumina Explorer 🌠!"
                        
                            with open(f"{interaction.user.id}.json","w",encoding="utf-8") as f:
                                json.dump(data,f,indent=4)
                            
                            await interaction.user.add_roles(role)
                            welcome_embed = discord.Embed(
                                title="Welcome! to **Lummina tunnels**",
                                color=discord.Color.dark_gold()
                            )
                            welcome_embed.set_footer(
                                icon_url=interaction.user.display_avatar.url,
                                text="Luminna tunnels are waiting for you 🌠"
                            )
                            welcome_embed.set_thumbnail(
                                url=interaction.user.display_avatar.url
                            )
                            await interaction.followup.send(content=interaction.user.mention,embed=welcome_embed)
                            await interaction.user.send(
                                f"⚔ **Rank Up!** Welcome, Miner ⛏\n\n"
                                f"The Lumina Tunnels recognize your skill…\n"
                                f"***Only the worthy can unlock the secret rank. Mine 1000 ores and try the command: `/secretRank` 🔥***"
                                )
                        else:
                            await interaction.followup.send(f"{interaction.user.mention} - Technical issue: 'Lumina Explorer' role not found. Contact a Caretaker to report bug.", ephemeral=True)
                    else:
                        requirments_msg = f"{interaction.user.mention} - **Lumina Tunnels Entry Requirements Not Met:**\n" + "\n".join(requirments_false)
                        await interaction.followup.send(requirments_msg)
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
            logging.error(f"Enter lumina error: {e}")

async def setup(bot: commands.Bot):
    await bot.add_cog(enterlumina(bot))
