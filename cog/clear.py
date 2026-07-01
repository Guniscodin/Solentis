import discord
from discord.ext import commands
from discord import app_commands
import logging

DEV_GUILD_ID = 1446549954268106884  # dev server for testing

class Clear(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="clear",
        description="Delete a number of messages from this channel"
    )
    @app_commands.describe(
        amount="Number of messages to delete (1-100)"
    )
    @app_commands.checks.cooldown(1, 3.0)
    @app_commands.guilds(DEV_GUILD_ID)
    async def clear(self, interaction: discord.Interaction, amount: int):

        await interaction.response.defer(ephemeral=True, thinking=True)

        try:
            # Permissions
            if not interaction.user.guild_permissions.manage_messages:
                embed = discord.Embed(
                    title="❌ You don't have permission to manage messages!",
                    color=discord.Color.red()
                )
                embed.set_footer(text=f"Requested by {interaction.user}", icon_url=interaction.user.display_avatar.url)
                await interaction.followup.send(embed=embed, ephemeral=True)
                return

            if not interaction.guild.me.guild_permissions.manage_messages:
                embed = discord.Embed(
                    title="❌ I don't have permission to manage messages!",
                    color=discord.Color.red()
                )
                embed.set_footer(text=f"Requested by {interaction.user}", icon_url=interaction.user.display_avatar.url)
                await interaction.followup.send(embed=embed, ephemeral=True)
                return

            # Clamp amount to 1-100
            if amount < 1 or amount > 100:
                embed = discord.Embed(
                    title="❌ You can only delete between 1 and 100 messages at once.",
                    color=discord.Color.red()
                )
                embed.set_footer(text=f"Requested by {interaction.user}", icon_url=interaction.user.display_avatar.url)
                await interaction.followup.send(embed=embed, ephemeral=True)
                return

            deleted = await interaction.channel.purge(limit=amount)
            embed = discord.Embed(
                title=f"🧹 Deleted {len(deleted)} messages",
                color=discord.Color.green()
            )
            embed.set_footer(text=f"Action by {interaction.user}", icon_url=interaction.user.display_avatar.url)
            await interaction.followup.send(embed=embed, ephemeral=True)

        except Exception as e:
            logging.error(e)
            await interaction.followup.send(f"❌ An error occurred: {e}", ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(Clear(bot))
