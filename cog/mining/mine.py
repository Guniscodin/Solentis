import discord
from discord.ext import commands
from discord import app_commands
import random
import json
import logging
import os
import dataloader

DEV_GUILD_ID = 1446549954268106884


# =========================
# VIEW
# =========================
class MineAgainView(discord.ui.View):
    def __init__(self, cog, user_id: int):
        super().__init__(timeout=60)
        self.cog = cog
        self.user_id = user_id
        self._cd = commands.CooldownMapping.from_cooldown(
            1, 2.0, commands.BucketType.user
        )

    @discord.ui.button(label="Mine Again ⛏", style=discord.ButtonStyle.green)
    async def mine_again(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message(
                "This isn't your mining session!", ephemeral=True
            )
            return

        bucket = self._cd.get_bucket(interaction.user)
        retry_after = bucket.update_rate_limit()
        if retry_after:
            await interaction.response.send_message(
                f"Slow down! Wait {retry_after:.1f}s.", ephemeral=True
            )
            return

        await interaction.response.defer()

        embed, view, level_up_msg = await self.cog.mine_logic(interaction.user)

        await interaction.edit_original_response(
            content=interaction.user.mention,
            embed=embed,
            view=view
        )

        if level_up_msg:
            try:
                await interaction.user.send(level_up_msg)
            except:
                pass


# =========================
# COG
# =========================
class Mine(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.yield_multiplier = 1.0

    # -------- ORE ROLLING --------
    def get_weighted_ore(self, pick_data, ores_data, luck=0):
        rarity_weights = {
            "common": 600,
            "uncommon": 240,
            "rare": 100,
            "epic": 40,
            "legendary": 15,
            "mythical": 4,
            "forbidden": 1,
        }

        luck_exponent = 1 - (luck / (luck + 100))
        can_mine = pick_data.get("can_mine", [])

        pool = []
        weights = []

        for rarity, base_weight in rarity_weights.items():
            if rarity not in ores_data:
                continue

            available = []
            for tier in ("low", "high"):
                for ore in ores_data[rarity].get(tier, []):
                    if ore["name"] in can_mine:
                        available.append(ore)

            if not available:
                continue

            weight = base_weight if rarity == "common" else base_weight ** luck_exponent

            for ore in available:
                pool.append(ore)
                weights.append(weight)

        if not pool:
            return random.choice(ores_data["common"]["low"])

        return random.choices(pool, weights=weights, k=1)[0]

    # -------- CORE MINING LOGIC --------
    async def mine_logic(self, user: discord.User):
        user_id = str(user.id)
        user_file = f"{user_id}.json"

        if not os.path.exists(user_file):
            raise RuntimeError("User not registered")

        with open(user_file, "r", encoding="utf-8") as f:
            user_data = json.load(f)

        ores_data = dataloader.ore_data
        pickaxes = dataloader.data_pick

        pick_name = user_data.get("equipped_pickaxe", "⛏ wooden")
        pick_data = None

        for rarity in pickaxes:
            for p in pickaxes[rarity]:
                if p["name"] == pick_name:
                    pick_data = p
                    break

        if not pick_data:
            pick_data = pickaxes["common"][0]

        luck = user_data.get("luck", 0)
        ore = self.get_weighted_ore(pick_data, ores_data, luck)

        chest_msg = ""
        if random.random() < 0.03:
            bonus = int(random.randint(500, 2000) * self.yield_multiplier)
            user_data["coins"] += bonus
            chest_msg = f"\n🎁 **Bonus Chest:** +🪙 {bonus}"

        sell_value = int(ore.get("sell_value", ore["value"]) * self.yield_multiplier)
        xp_gain = int(ore["xp"] * self.yield_multiplier)

        user_data["coins"] += sell_value
        user_data["xp"] += xp_gain

        level_up_msg = None
        xp_req = user_data.get("xp_required", 100)

        if user_data["xp"] >= xp_req:
            user_data["lvl"] += 1
            user_data["xp"] -= xp_req
            user_data["xp_required"] = int(xp_req * 1.5)
            level_up_msg = f"🎊 **LEVEL UP!** You reached level **{user_data['lvl']}**!"

        with open(user_file, "w", encoding="utf-8") as f:
            json.dump(user_data, f, indent=4)

        embed = discord.Embed(
            title="⛏ Mining Results",
            description=f"You mined **{ore['name']}**!{chest_msg}",
            color=discord.Color.gold()
        )

        embed.add_field(name="Rarity", value=ore["rarity"], inline=True)
        embed.add_field(name="Sell Value", value=f"🪙 {sell_value}", inline=True)
        embed.add_field(name="XP Gained", value=f"✨ {xp_gain}", inline=True)
        embed.set_footer(
            text=f"XP: {user_data['xp']}/{user_data['xp_required']} | Luck: {luck}"
        )

        view = MineAgainView(self, user.id)
        return embed, view, level_up_msg

    # -------- SLASH COMMAND --------
    @app_commands.command(name="mine", description="Start mining for ores!")
    @app_commands.checks.cooldown(1, 2.0)
    @app_commands.guilds(DEV_GUILD_ID)
    async def mine_command(self, interaction: discord.Interaction):
        allowed_channels = [1455195010126315655]
        if interaction.channel_id not in allowed_channels:
            await interaction.response.send_message(
                "Wrong channel!", ephemeral=True
            )
            return

        await interaction.response.defer(thinking=True)

        try:
            embed, view, level_up_msg = await self.mine_logic(interaction.user)
            await interaction.followup.send(
                content=interaction.user.mention,
                embed=embed,
                view=view
            )

            if level_up_msg:
                try:
                    await interaction.user.send(level_up_msg)
                except:
                    pass

        except Exception as e:
            logging.error(f"Mining Error: {e}")
            await interaction.followup.send(
                "Something went wrong while mining.", ephemeral=True
            )


async def setup(bot):
    await bot.add_cog(Mine(bot))
