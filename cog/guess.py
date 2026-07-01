import discord
import random
from discord.ext import commands
from discord import app_commands


DEV_GUILD_ID = 1446549954268106884  # dev guild for fast sync


class Guess(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="guess", description="Guess the number (1-10)")
    @app_commands.guilds(DEV_GUILD_ID)
    async def guess(self, interaction: discord.Interaction):
        allowed_channels = [1455057800781889598]
        if interaction.channel_id not in allowed_channels:
            channel_embed = discord.Embed(
                title="Wrong channel!",
                description="Try this is #bot-commands channel!",
                color=discord.Color.red()
            )
            await interaction.followup.send(content=interaction.user.mention,embed=channel_embed, ephemeral=True)
            return
        embed = discord.Embed(
            title="🎯 Guess the Number",
            description="I'm thinking of a number between **1 and 10**.\nYou have **3 attempts**.",
            color=discord.Color.blurple()
        )
        embed.set_footer(
            text=f"Requested by {interaction.user}",
            icon_url=interaction.user.display_avatar.url
        )

        view = GuessView(author=interaction.user)

        await interaction.response.send_message(
            embed=embed,
            view=view
        )


class GuessView(discord.ui.View):
    def __init__(self, author: discord.User):
        super().__init__(timeout=30)
        self.author = author
        self.target = random.randint(1, 10)
        self.attempts = 3

        # create 10 buttons dynamically
        for i in range(1, 11):
            button = discord.ui.Button(
                label=str(i),
                style=discord.ButtonStyle.secondary
            )
            button.callback = self.make_guess_callback(i)
            self.add_item(button)

    def make_guess_callback(self, number: int):
        async def callback(interaction: discord.Interaction):
            # only command user can interact
            if interaction.user.id != self.author.id:
                await interaction.response.send_message(
                    "❌ This isn't your game lil bro",
                    ephemeral=True
                )
                return

            self.attempts -= 1

            # correct guess
            if number == self.target:
                embed = discord.Embed(
                    title="✅ Correct!",
                    description=f"You guessed it right.\nThe number was **{self.target}** 🎉",
                    color=discord.Color.green()
                )
                await interaction.response.edit_message(
                    embed=embed,
                    view=None
                )
                self.stop()
                return

            # out of attempts
            if self.attempts <= 0:
                embed = discord.Embed(
                    title="❌ Game Over",
                    description=f"You ran out of attempts.\nThe number was **{self.target}** 💀",
                    color=discord.Color.red()
                )
                await interaction.response.edit_message(
                    embed=embed,
                    view=None
                )
                self.stop()
                return

            # wrong guess but still attempts left
            hint = "📉 Too low" if number < self.target else "📈 Too high"

            embed = discord.Embed(
                title="❌ Wrong Guess",
                description=f"{hint}\nAttempts left: **{self.attempts}**",
                color=discord.Color.orange()
            )

            await interaction.response.edit_message(
                embed=embed,
                view=self
            )

        return callback

    async def on_timeout(self):
        for item in self.children:
            item.disabled = True


async def setup(bot: commands.Bot):
    await bot.add_cog(Guess(bot))
