import discord
from discord.ext import commands
from discord import app_commands
import logging

DEV_GUILD_ID = 1446549954268106884  # dev server ID

class Info(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="serverinfo",
        description="Get detailed information about the server"
    )
    @app_commands.guilds(DEV_GUILD_ID)
    async def serverinfo(self, interaction: discord.Interaction):
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
            guild = interaction.guild
            embed = discord.Embed(
                title=f"🌐 Server Info - {guild.name}",
                color=discord.Color.blurple()
            )
            
            embed.set_thumbnail(url=guild.icon.url if guild.icon else discord.Embed.Empty)
            
            embed.add_field(name="Server ID", value=guild.id, inline=True)
            embed.add_field(name="Owner", value=guild.owner.mention, inline=True)
            embed.add_field(name="Members", value=guild.member_count, inline=True)
            embed.add_field(name="Roles", value=len(guild.roles), inline=True)
            embed.add_field(name="Text Channels", value=len(guild.text_channels), inline=True)
            embed.add_field(name="Voice Channels", value=len(guild.voice_channels), inline=True)
            embed.add_field(name="Created On", value=guild.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
            
            embed.set_footer(text=f"Requested by {interaction.user}", icon_url=interaction.user.display_avatar.url)
            await interaction.response.send_message(embed=embed, ephemeral=False)

        except Exception as e:
            logging.error(e)
            await interaction.response.send_message(f"❌ An error occurred: {e}", ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(Info(bot))
