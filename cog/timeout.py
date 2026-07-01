import discord
from discord.ext import commands
from discord import app_commands
from datetime import timedelta

DEV_GUILD_ID = 1446549954268106884  # optional for testing

class Timeout(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="timeout",
        description="Temporarily mute a member"
    )
    @app_commands.checks.cooldown(1,3.0)
    @app_commands.describe(
        member="The member to timeout",
        minutes="Duration in minutes (1-1440)",
        reason="Optional reason for timeout"
    )
    async def timeout(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        minutes: int,
        reason: str = None
    ):
        # Check bot permissions
        if not interaction.guild.me.guild_permissions.moderate_members:
            await interaction.response.send_message(
                "❌ I don't have permission to timeout members!",
                ephemeral=True
            )
            return

        # Check command user permissions
        if not interaction.user.guild_permissions.moderate_members:
            await interaction.response.send_message(
                "❌ You don't have permission to timeout members!",
                ephemeral=True
            )
            return

        # Safety checks
        if member == interaction.user:
            await interaction.response.send_message(
                "❌ You can't timeout yourself!",
                ephemeral=True
            )
            return
        if member == interaction.guild.owner:
            await interaction.response.send_message(
                "❌ You can't timeout the server owner!",
                ephemeral=True
            )
            return
        if minutes < 1 or minutes > 1440:
            await interaction.response.send_message(
                "❌ Timeout must be between 1 and 1440 minutes!",
                ephemeral=True
            )
            return

        try:
            await member.timeout(
                duration=timedelta(minutes=minutes),
                reason=reason
            )
        except discord.Forbidden:
            await interaction.response.send_message(
                "❌ I cannot timeout this member (missing permissions)",
                ephemeral=True
            )
            return

        # Success message
        embed = discord.Embed(
            title="⏱ Timeout Applied",
            description=f"{member.mention} has been timed out for **{minutes} minutes**",
            color=discord.Color.orange()
        )
        if reason:
            embed.add_field(name="Reason", value=reason, inline=False)
        embed.set_footer(text=f"Action by {interaction.user}")

        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Timeout(bot))
