import discord
from discord.ext import commands
from discord import app_commands
import os
import json
import logging

DEV_GUILD_ID = 1446549954268106884  # your dev server ID (int)

class register(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="register",
        description="register to get access to the mining game!"
    )
    @app_commands.checks.cooldown(1, 2.0)
    @app_commands.guilds(DEV_GUILD_ID)  # instant dev sync
    async def register_command(self, interaction: discord.Interaction):
        # Defer immediately to allow processing time
        await interaction.response.defer(ephemeral=False, thinking=True)
        channel_embed = discord.Embed(
            title="Wrong channel! ✈",
            description="Try this command in #miners-guild channel! ⚡",
            color=discord.Color.dark_purple()
        )
        channel_embed.set_footer(
            icon_url=interaction.user.display_avatar.url
        )
        # Check if the command is run in the correct channel (using interaction.channel_id)
        allowed_channels = [1455195010126315655]
        if interaction.channel_id not in allowed_channels:
            channel_embed = discord.Embed(
                title="Wrong channel!",
                description="Try this is #game-commands ⛏ channel!",
                color=discord.Color.red()
            )
            await interaction.followup.send(content=interaction.user.mention,embed=channel_embed, ephemeral=True)
            return

        # The entire default_pack dictionary must be inside the command function
        default_pack = {
    "name": interaction.user.name,
    "xp": 0,
    "coins": 0,
    "lvl": 1,
    "pickaxe": {
        "name": "⛏ wooden",
        "rarity": "common",
        "price": 0,
        "can_mine": [
            "Flintstone Shard",
            "Dusty Pebblite",
            "Copper Dullcore",
            "Faded Quartz",
            "Chalk Crystal",
            "Marblenite",
            "Stonegrain Ore",
            "Dullrock Node",
            "Low-Glow Quartz"
        ]
    },
    "rank": "Novice",
    "ores_mined": 0,
    "xp_required": 20,
    "area2_unlocked": False,
    "max_stash": 20,
    "stash": {
        "**COMMON ORES**": "🟠",
        "Flintstone Shard": 0,
        "Dusty Pebblite": 0,
        "Copper Dullcore": 0,
        "Faded Quartz": 0,
        "Chalk Crystal": 0,
        "Marblenite": 0,
        "Stonegrain Ore": 0,
        "Dullrock Node": 0,
        "Low-Glow Quartz": 0,

        "**UNCOMMON ORES**": "🟡",
        "Emberstone": 0,
        "Frostiron": 0,
        "Shards of Lunite": 0,
        "Verdant Ore": 0,
        "Tide Pearl Ore": 0,
        "Shiverstone": 0,
        "Thornite": 0,
        "Rift Shard": 0,

        "**RARE ORES**": "🟢",
        "Starfall Crystal": 0,
        "Voidmetal": 0,
        "Soulstone": 0,
        "Phoenix Ore": 0,
        "Astral Sapphire Ore": 0,
        "Celestial Goldshard": 0,

        "**EPIC ORES**": "🔵",
        "Frostfire Crystal": 0,
        "Etherium": 0,
        "Radiant Aquamarine": 0,
        "Eternium": 0,

        "**LEGENDARY ORES**": "🟣",
        "Infinity Core": 0,
        "Omega Diamond": 0,
        "Genesis Ore": 0,
        "Voidheart Metal": 0,

        "**MYTHICAL ORES**": "🌌",
        "Drakonheart Core": 0,
        "Seraphic Diamond": 0,
        "Shard of the First Star": 0,
        "Divine Tempest Ore": 0,

        "**FORBIDDEN ORES**": "☠️",
        "Abysscore Ignis": 0,
        "Singularity Ore": 0
    }
}

        
        try:
            # Check for user file
            if os.path.exists(f"{interaction.user.id}.json"):
                already_register = discord.Embed(
                    title="**Already registered! ⛏**",
                    color=discord.Color.yellow()
                )
                already_register.set_footer(
                    icon_url=interaction.user.display_avatar.url
                )
                await interaction.followup.send(content=interaction.user.mention,embed=already_register, ephemeral=True)
            else:
                # Assign role
                role = discord.utils.get(interaction.guild.roles, name="Miner ⛏")
                if role:
                    await interaction.user.add_roles(role)
                
                # Create file
                with open(f"{interaction.user.id}.json", "w", encoding="utf-8") as f:
                    json.dump(default_pack, f, indent=4)
                
                # Send success message
                success_msg = discord.Embed(
                    title="**Welcome to Solentis Mines ⚔️!**",
                    description="Let’s see how fast you break that pickaxe! ⛏",
                    color=discord.Color.dark_gold()
                )
                success_msg.set_footer(
                    text="Check your inventory by typing `/inventory`!",
                    icon_url=interaction.user.display_avatar.url
                )
                success_msg.set_thumbnail(
                    url=interaction.user.display_avatar.url
                )
                await interaction.followup.send(content=interaction.user.mention,embed=success_msg)
        except Exception as e:
            await interaction.followup.send(f"{interaction.user.mention}-- Something went wrong please try again later!🕷", ephemeral=True)
            logging.error(f"Register error for {interaction.user.id}: {e}")

async def setup(bot: commands.Bot):
    await bot.add_cog(register(bot))