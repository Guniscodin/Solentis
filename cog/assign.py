import discord
from discord.ext import commands
from discord import app_commands
import logging

DEV_GUILD_ID = 1446549954268106884  # your dev server ID (int)

class Assign(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="assign",
        description="Assign or toggle a role for a member"
    )
    @app_commands.describe(
        member="The member to assign/remove the role",
        role_name="Enter the role name"
    )
    @app_commands.checks.cooldown(1, 2.0)
    @app_commands.guilds(DEV_GUILD_ID)  # instant dev sync
    async def assign(self, interaction: discord.Interaction, member: discord.Member, role_name: str):

        await interaction.response.defer(ephemeral=True, thinking=True)
        
        try:
            # Check bot permissions
            if not interaction.guild.me.guild_permissions.manage_roles:
                embed = discord.Embed(
                    title="❌ I don't have permission to manage roles!",
                    color=discord.Color.red()
                )
                embed.set_footer(text=f"Requested by {interaction.user}", icon_url=interaction.user.display_avatar.url)
                await interaction.followup.send(embed=embed, ephemeral=True)
                return

            # Check user permissions
            if not interaction.user.guild_permissions.manage_roles:
                embed = discord.Embed(
                    title="❌ You don't have permission to manage roles!",
                    color=discord.Color.red()
                )
                embed.set_footer(text=f"Requested by {interaction.user}", icon_url=interaction.user.display_avatar.url)
                await interaction.followup.send(embed=embed, ephemeral=True)
                return

            # Find role by name
            role = discord.utils.get(interaction.guild.roles, name=role_name)
            if not role:
                embed = discord.Embed(
                    title="❌ Role not found in server",
                    color=discord.Color.red()
                )
                embed.set_footer(text=f"Requested by {interaction.user}", icon_url=interaction.user.display_avatar.url)
                await interaction.followup.send(embed=embed, ephemeral=True)
                return

            # Check hierarchy
            if role >= interaction.guild.me.top_role:
                embed = discord.Embed(
                    title="❌ I cannot assign a role higher or equal to my top role",
                    color=discord.Color.red()
                )
                embed.set_footer(text=f"Requested by {interaction.user}", icon_url=interaction.user.display_avatar.url)
                await interaction.followup.send(embed=embed, ephemeral=True)
                return

            # Optional: check user hierarchy (cannot assign roles higher than themselves)
            if role >= interaction.user.top_role and interaction.user != interaction.guild.owner:
                embed = discord.Embed(
                    title="❌ You cannot assign a role higher or equal to your top role",
                    color=discord.Color.red()
                )
                embed.set_footer(text=f"Requested by {interaction.user}", icon_url=interaction.user.display_avatar.url)
                await interaction.followup.send(embed=embed, ephemeral=True)
                return

            # Assign or toggle
            if role in member.roles:
                await member.remove_roles(role)
                embed = discord.Embed(
                    title=f"🔹 Role {role.name} removed from {member.display_name}",
                    color=discord.Color.orange()
                )
            else:
                await member.add_roles(role)
                embed = discord.Embed(
                    title=f"✅ Role {role.name} assigned to {member.display_name}",
                    color=discord.Color.green()
                )

            embed.set_footer(text=f"Action by {interaction.user}", icon_url=interaction.user.display_avatar.url)
            await interaction.followup.send(embed=embed, ephemeral=True)

        except Exception as e:
            await interaction.followup.send(f"❌ An error occurred: {e}", ephemeral=True)
            logging.error(e)


async def setup(bot: commands.Bot):
    await bot.add_cog(Assign(bot))
