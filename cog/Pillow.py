from PIL import Image
import aiohttp
import io
import discord
from discord.ext import commands
from discord import app_commands
import logging

DEV_GUILD_ID = 1446549954268106884


class Pillow(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="pillow",
        description="Test command for pillow module!"
    )
    @app_commands.checks.cooldown(1, 2.0)
    @app_commands.guilds(DEV_GUILD_ID)
    async def pillow(self, interaction: discord.Interaction):
        await interaction.response.defer()

        try:
            avatar_url = interaction.user.display_avatar.url

            async with aiohttp.ClientSession() as session:
                async with session.get(avatar_url) as resp:
                    avatar_bytes = await resp.read()

            avatar_img = Image.open(io.BytesIO(avatar_bytes))
            avatar_img = avatar_img.resize((255, 255))

            buffer = io.BytesIO()
            avatar_img.save(buffer, format="PNG")
            buffer.seek(0)

            file = discord.File(buffer, filename="avatar.png")

            embed = discord.Embed(
                title="Pillow testing!",
                color=discord.Color.red()
            )
            embed.set_image(url="attachment://avatar.png")

            await interaction.followup.send(
                content=interaction.user.mention,
                embed=embed,
                file=file
            )

        except Exception as e:
            logging.exception("Pillow command error")


async def setup(bot: commands.Bot):
    await bot.add_cog(Pillow(bot))
