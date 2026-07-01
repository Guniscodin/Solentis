import discord
from discord.ext import commands
from discord import app_commands

DEV_GUILD_ID = 1446549954268106884  # optional for testing

class Ban(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="ban",
        description="Ban a member from the server"
    )
    @app_commands.checks.cooldown(1,3.0)
    @app_commands.describe(
        member="The member to ban",
        reason="Optional reason for banning",
        delete_days="Delete messages from the past X days (0-7)"
    )
    async def ban(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str = None,
        delete_days: int = 0
    ):
        
        # Permissions check
        if not interaction.guild.me.guild_permissions.ban_members:
            await interaction.response.send_message(
                "❌ I don't have permission to ban members!",
                ephemeral=True
            )
            return
        if not interaction.user.guild_permissions.ban_members:
            await interaction.response.send_message(
                "❌ You don't have permission to ban members!",
                ephemeral=True
            )
            return

        # Safety checks
        if member == interaction.user:
            await interaction.response.send_message(
                "❌ You can't ban yourself!",
                ephemeral=True
            )
            return
        if member == interaction.guild.owner:
            await interaction.response.send_message(
                "❌ You can't ban the server owner!",
                ephemeral=True
            )
            return
        if delete_days < 0 or delete_days > 7:
            await interaction.response.send_message(
                "❌ Delete days must be between 0 and 7",
                ephemeral=True
            )
            return

        try:
            await member.ban(reason=reason, delete_message_days=delete_days)
        except discord.Forbidden:
            await interaction.response.send_message(
                "❌ I cannot ban this member (missing permissions)",
                ephemeral=True
            )
            return

        # Success embed
        embed = discord.Embed(
            title="⛔ Member Banned",
            description=f"{member.mention} has been banned from the server.",
            color=discord.Color.dark_red()
        )
        if reason:
            embed.add_field(name="Reason", value=reason, inline=False)
        if delete_days:
            embed.add_field(name="Deleted Messages", value=f"{delete_days} days", inline=False)
        embed.set_footer(text=f"Action by {interaction.user}")

        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Ban(bot))
