import discord
from discord.ext import commands
from discord import app_commands
import random

DEV_GUILD_ID = 1446549954268106884  # your dev server ID (int)

class rate(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="rate",
        description="rate a person!"
    )
    @app_commands.guilds(DEV_GUILD_ID)  # instant dev sync
    async def example(self, interaction: discord.Interaction,member: discord.Member):
        allowed_channels = [1455057800781889598]
        if interaction.channel_id not in allowed_channels:
            channel_embed = discord.Embed(
                title="Wrong channel!",
                description="Try this is #bot-commands channel!",
                color=discord.Color.red()
            )
            await interaction.followup.send(content=interaction.user.mention,embed=channel_embed, ephemeral=True)
            return
        rating = random.randint(0, 11)

        if member:
            # Simplified response for length
            messages = {
                0: f"{rating}/10 - This is not a rating, this is a violation of the Geneva Convention 💀",
                1: f"{rating}/10 - This ain’t even a rating, this is a warning label ⚠",
                2: f"{rating}/10 - You exist… technically 🙏",
                3: f"{rating}/10 - You got potential, but it’s on airplane mode ✈",
                4: f"{rating}/10 - Mid with commitment issues 👽",
                5: f"{rating}/10 - Perfectly balanced… between 'nah' and 'who asked' 😭",
                6: f"{rating}/10 - Slightly above mid, like reheated fries 🍟",
                7: f"{rating}/10 - You’re cool, but don’t get confident yet buddy 😏",
                8: f"{rating}/10 - Lowkey fire, but still has buffering moments 🔄",
                9: f"{rating}/10 - Almost elite, one small glow-up away from domination 😤",
                10: f"{rating}/10 - Main character energy, plot armor included 🗿",
                11: f"{rating}/10 - Unreal. Devs forgot to nerf you 🔥",
            }
            msg = f"{messages.get(rating, 'Error')} {member.mention}"
        else:
            msg = f"{interaction.user.mention} - Rate what? Air? Oxygen DLC? 🙏"

        embed = discord.Embed(
            title=f"Lets see....! 👀",
            description=f"{msg}",
            color=discord.Color.dark_blue()
        )
        embed.set_footer(
            text="Requested by",
            icon_url=interaction.user.display_avatar.url
        )
        await interaction.response.send_message(content=interaction.user.mention,embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(rate(bot))
