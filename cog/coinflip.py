import discord
from discord.ext import commands
from discord import app_commands
import random
DEV_GUILD_ID = 1446549954268106884  # your dev server ID (int)

class coinflip(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="coinflip",
        description="Flip a coin with a 50/50 chance for Heads or Tails"
    )
    @app_commands.checks.cooldown(1,2.0)
    @app_commands.guilds(DEV_GUILD_ID)  # instant dev sync
    async def example(self, interaction: discord.Interaction):
        allowed_channels = [1455057800781889598]
        if interaction.channel_id not in allowed_channels:
            channel_embed = discord.Embed(
                title="Wrong channel!",
                description="Try this is #bot-commands channel!",
                color=discord.Color.red()
            )
            await interaction.followup.send(content=interaction.user.mention,embed=channel_embed, ephemeral=True)
            return
        chance = random.randint(1, 10)
        result = "Heads 😃!" if chance > 5 else "Tails 😃!"
        embed = discord.Embed(
            title=f"**Flipped a coin! and got {result}**",
            color=discord.Color.brand_green()
        )
        embed.set_footer(
            icon_url=interaction.user.display_avatar.url
        )
        view = flipagain(author=interaction.user)
        await interaction.response.send_message(content=interaction.user.mention,embed=embed,view=view)

class flipagain(discord.ui.View):
    def __init__(self,author: discord.User):
        super().__init__(timeout=30)
        self.author = author
    @discord.ui.button(label="Flip again ?",emoji="⚡",style=discord.ButtonStyle.primary)
    async def example(self, interaction: discord.Interaction,button: discord.ui.Button):
        allowed_channels = [1455057800781889598]
        if interaction.channel_id not in allowed_channels:
            channel_embed = discord.Embed(
                title="Wrong channel!",
                description="Try this is #bot-commands channel!",
                color=discord.Color.red()
            )
            await interaction.followup.send(content=interaction.user.mention,embed=channel_embed, ephemeral=True)
            return
        chance = random.randint(1, 10)
        result = "Heads 😃!" if chance > 5 else "Tails 😃!"
        embed = discord.Embed(
            title=f"**Flipped a coin! and got {result}**",
            color=discord.Color.brand_green()
        )
        embed.set_footer(
            icon_url=interaction.user.display_avatar.url
        )
        await interaction.response.edit_message(content=interaction.user.mention,embed=embed,view=self)

async def setup(bot: commands.Bot):
    await bot.add_cog(coinflip(bot))
