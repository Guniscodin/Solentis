import discord
from discord.ext import commands
from discord import app_commands
import random
DEV_GUILD_ID = 1446549954268106884  # your dev server ID (int)

class dare(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="dare",
        description="Get a random Dare"
    )
    @app_commands.checks.cooldown(1,2.0)
    @app_commands.guilds(DEV_GUILD_ID)  # instant dev sync
    async def dare(self,interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False, thinking=True)
        allowed_channels = [1455057800781889598]
        if interaction.channel_id not in allowed_channels:
            channel_embed = discord.Embed(
                title="Wrong channel!",
                description="Try this is #bot-commands channel!",
                color=discord.Color.red()
            )
            await interaction.followup.send(content=interaction.user.mention,embed=channel_embed, ephemeral=True)
            return
        try:
            with open("dares.txt", "r", encoding="utf-8") as f:
                dares = [line.strip() for line in f.readlines()]

                embed_file_empty = discord.Embed(
                    title="Error ☠",
                    description="Uh I think the dares file is empty, contact a Caretaker for a solution 😉",
                    color=discord.Color.red()
                )
                embed_file_empty.set_footer(
                    icon_url=interaction.user.display_avatar.url
                )
                if not dares:
                    await interaction.followup.send(content=interaction.user.mention,embed=embed_file_empty, ephemeral=True)
                    return
            random_dare = random.choice(dares)
            embed = discord.Embed(
                title="The dare is....",
                description=f"{random_dare}",
                color=discord.Color.dark_gold()
            )
            embed.set_footer(
                icon_url=interaction.user.display_avatar.url
            )
            view = againdare(author=interaction.user)
            await interaction.followup.send(content=interaction.user.mention,embed=embed,view=view)
        except Exception as e:
            await interaction.followup.send(f'❌ An error occurred: {e}', ephemeral=True)
            print(e)

class againdare(discord.ui.View):
    def __init__(self,author: discord.User):
        super().__init__(timeout=30)
        self.author = author
    @discord.ui.button(label="Roll again?",emoji="🎲",style=discord.ButtonStyle.primary)
    async def dare(self,interaction: discord.Interaction,button: discord.ui.Button):
        await interaction.response.defer(ephemeral=False, thinking=True)
        allowed_channels = [1455057800781889598]
        if interaction.channel_id not in allowed_channels:
            channel_embed = discord.Embed(
                title="Wrong channel!",
                description="Try this is #bot-commands channel!",
                color=discord.Color.red()
            )
            await interaction.followup.send(content=interaction.user.mention,embed=channel_embed, ephemeral=True)
            return
        try:
            with open("dares.txt", "r", encoding="utf-8") as f:
                dares = [line.strip() for line in f.readlines()]
            
                if not dares:
                    await interaction.followup.send(f"{interaction.user.mention} - Uh I think the dares file is empty, contact a Caretaker for a solution 😉", ephemeral=True)
                    return
            random_dare = random.choice(dares)
            embed = discord.Embed(
                title="The dare is....",
                description=f"{random_dare}",
                color=discord.Color.dark_gold()
            )
            embed.set_footer(
                icon_url=interaction.user.display_avatar.url
            )
            await interaction.followup.send(content=interaction.user.mention,embed=embed,view=self)
        except Exception as e:
            await interaction.followup.send(f'❌ An error occurred: {e}', ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(dare(bot))
