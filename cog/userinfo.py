import discord
from discord.ext import commands
from discord import app_commands
import logging

DEV_GUILD_ID = 1446549954268106884  # dev server ID

class UserInfo(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="userinfo",
        description="Get detailed information about a server member"
    )
    @app_commands.describe(
        member="The member you want information about"
    )
    @app_commands.checks.cooldown(1,3.0)
    @app_commands.guilds(DEV_GUILD_ID)
    async def userinfo(self, interaction: discord.Interaction, member: discord.Member):
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
            embed = discord.Embed(
                title=f"👤 User Info - {member.display_name}",
                color=discord.Color.green()
            )
            
            embed.set_thumbnail(url=member.display_avatar.url)
            
            embed.add_field(name="User ID", value=member.id, inline=True)
            embed.add_field(name="Nickname", value=member.display_name, inline=True)
            embed.add_field(name="Account Created", value=member.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
            embed.add_field(name="Joined Server", value=member.joined_at.strftime("%Y-%m-%d %H:%M:%S") if member.joined_at else "Unknown", inline=False)
            embed.add_field(name="Top Role", value=member.top_role.mention, inline=True)
            embed.add_field(name="Roles", value=", ".join([role.mention for role in member.roles if role != interaction.guild.default_role]), inline=False)
            
            embed.set_footer(text=f"Requested by {interaction.user}", icon_url=interaction.user.display_avatar.url)
            
            await interaction.response.send_message(embed=embed, ephemeral=False)
        except Exception as e:
            logging.error(e)
            await interaction.response.send_message(f"❌ An error occurred: {e}", ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(UserInfo(bot))
