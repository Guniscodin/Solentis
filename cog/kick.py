import discord
from discord.ext import commands
from discord import app_commands

DEV_GUILD_ID = 1446549954268106884  # optional for testing

class Kick(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="kick",
        description="Kick a member from the server"
    )
    @app_commands.describe(
        member="The member to kick",
        reason="Optional reason for kicking"
    )
    async def kick(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str = None
    ):
        # Check bot permissions
        if not interaction.guild.me.guild_permissions.kick_members:
            await interaction.response.send_message(
                "❌ I don't have permission to kick members!",
                ephemeral=True
            )
            return

        # Check command user permissions
        if not interaction.user.guild_permissions.kick_members:
            await interaction.response.send_message(
                "❌ You don't have permission to kick members!",
                ephemeral=True
            )
            return

        # Safety checks
        if member == interaction.user:
            await interaction.response.send_message(
                "❌ You can't kick yourself!",
                ephemeral=True
            )
            return
        if member == interaction.guild.owner:
            await interaction.response.send_message(
                "❌ You can't kick the server owner!",
                ephemeral=True
            )
            return

        try:
            await member.kick(reason=reason)
        except discord.Forbidden:
            await interaction.response.send_message(
                "❌ I cannot kick this member (missing permissions)",
                ephemeral=True
            )
            return

        # Success embed
        embed = discord.Embed(
            title="👢 Member Kicked",
            description=f"{member.mention} has been kicked from the server.",
            color=discord.Color.red()
        )
        if reason:
            embed.add_field(name="Reason", value=reason, inline=False)
        embed.set_footer(text=f"Action by {interaction.user}")

        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Kick(bot))
