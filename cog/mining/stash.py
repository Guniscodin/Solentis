import discord
from discord.ext import commands
from discord import app_commands
import json
import os
import logging
DEV_GUILD_ID = 1446549954268106884  # your dev server ID (int)

class stash(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="stash",
        description="Check your current stash"
    )
    @app_commands.checks.cooldown(1,2.0)
    @app_commands.guilds(DEV_GUILD_ID)  # instant dev sync
    async def stash(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True, thinking=True)

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
                with open(f"{interaction.user.id}.json", "r", encoding="utf-8") as f:
                    data = json.load(f)

                stash_ores = data["stash"]

                stash_msg = discord.Embed(
                    title="Your stash🎒",
                    color=discord.Color.red()
                )
                embeds = []

                field_count = 0
                for ore, amount in stash_ores.items():
                    if isinstance(amount, str):
                        stash_msg.add_field(
                            name=amount,value=ore,inline=False
                        )
                    else:
                        stash_msg.add_field(
                            name=ore,value=amount,inline=False
                        )
                    field_count += 1
                    if field_count >= 25:
                        stash_msg.set_footer(
                            text="Start mining! ⛏",
                            icon_url=interaction.user.display_avatar.url
                        )
                        stash_msg.set_thumbnail(
                            url=interaction.user.display_avatar.url
                        )
                        embeds.append(stash_msg)
                        stash_msg  = discord.Embed(title="Your stash🎒",color=discord.Color.dark_red())
                        field_count = 0
                if field_count > 0:
                    stash_msg.set_footer(
                        text="Start mining! ⛏",
                        icon_url=interaction.user.display_avatar.url
                    )
                    stash_msg.set_thumbnail(
                        url=interaction.user.display_avatar.url
                    )
                    embeds.append(stash_msg)

            # Send in DM due to potential message length
                for embed in embeds:
                    await interaction.user.send(embed=embed,content=interaction.user.mention)

                dm_embed = discord.Embed(
                    title="Check Your Dm! 📩",
                    color=discord.Color.dark_gold()
                )
                dm_embed.set_footer(
                    text="Requested by!",
                    icon_url=interaction.user.display_avatar.url
                )
                dm_embed.set_thumbnail(
                    url=interaction.user.display_avatar.url
                )
                await interaction.followup.send(content=interaction.user.mention,embed=dm_embed,ephemeral=True)

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

        except discord.Forbidden:
            await interaction.followup.send(f"{interaction.user.mention} -- Bro your DMs are off 💀", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"{interaction.user.mention} -- Something went wrong, please try again later! 🕷", ephemeral=True)
            logging.error(f"Stash command error: {e}")


async def setup(bot: commands.Bot):
    await bot.add_cog(stash(bot))
