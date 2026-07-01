import discord
import random
from discord.ext import commands
from discord import app_commands

DEV_GUILD_ID = 1446549954268106884  # INT, not Object

class Roll(commands.Cog):
    def __init__(self,bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="roll",description="Roll a dice 1 - 6")
    @app_commands.guilds(DEV_GUILD_ID) 
    @app_commands.checks.cooldown(1,2.0)
    async def roll(self,interaction: discord.Interaction):
        allowed_channels = [1455057800781889598]
        if interaction.channel_id not in allowed_channels:
            channel_embed = discord.Embed(
                title="Wrong channel!",
                description="Try this is #bot-commands channel!",
                color=discord.Color.red()
            )
            await interaction.followup.send(content=interaction.user.mention,embed=channel_embed, ephemeral=True)
            return
        chance = random.randint(1,6)
        if chance <= 2:
            color = discord.Color.red()
        elif chance <= 4:
            color = discord.Color.gold()
        else:
            color = discord.Color.green()

        if chance == 6:
            reaction = "🔥 Critical Roll!"
        elif chance == 1:
            reaction = "💀 Disaster!"
        else:
            reaction = "Not bad!"
        
        embed = discord.Embed(
            title=f"🎲 Dice rolled",
            description=f"You got {chance}\n{reaction}",
            color=color
        )
        embed.set_footer(
            text=f"Requested by",
            icon_url=interaction.user.display_avatar.url
        )
        view = Rollbuttonview(author=interaction.user)
        await interaction.response.send_message(content=interaction.user.mention,embed=embed,view=view)
    
class Rollbuttonview(discord.ui.View):
    def __init__(self,author: discord.User):
        super().__init__(timeout=30)
        self.author = author

    @discord.ui.button(label="🎲 Roll again ?",style=discord.ButtonStyle.green)
    async def roll_again(self,interaction: discord.Interaction,button: discord.ui.Button):
        allowed_channels = [1455057800781889598]
        if interaction.channel_id not in allowed_channels:
            channel_embed = discord.Embed(
                title="Wrong channel!",
                description="Try this is #bot-commands channel!",
                color=discord.Color.red()
            )
            await interaction.followup.send(content=interaction.user.mention,embed=channel_embed, ephemeral=True)
            return
        if interaction.user.id != self.author.id :
            await interaction.response.send_message(f"This button isnt for you!")
            return
        
        chance = random.randint(1,6)

        if chance <= 2:
            color = discord.Color.red()
        elif chance <= 4:
            color = discord.Color.gold()
        else:
            color = discord.Color.green()

        if chance == 6:
            reaction = "🔥 Critical Roll!"
        elif chance == 1:
            reaction = "💀 Disaster!"
        else:
            reaction = "Not bad!"

        embed = discord.Embed(
            title="🎲 Dice Roll",
            description=f"You rolled **{chance}**\n{reaction}",
            color=color
        )
        embed.set_footer(text=f"Requested by {interaction.user}\n 2sec cooldown!", icon_url=interaction.user.display_avatar.url)
        await interaction.response.edit_message(embed=embed,view=self)


async def setup(bot: commands.Bot):
    await bot.add_cog(Roll(bot))