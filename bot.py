import discord
from discord import app_commands
from discord.ext import commands
import requests
import os
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)

class_color = {
    "Death Knight": 0xC41F3B,
    "Demon Hunter": 0xA330C9,
    "Druid": 0xFF7D0A,
    "Evoker": 0x33937F,
    "Hunter": 0xAAD372,
    "Mage": 0x3FC7EB,
    "Monk": 0x00FF98,
    "Paladin": 0xF58CBA,
    "Priest": 0xFFFFFF,
    "Rogue": 0xFFF569,
    "Shaman": 0x0070DE,
    "Warlock": 0x8787ED,
    "Warrior": 0xC79C6E,
}

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# bot ready
@bot.event
async def on_ready():
    slash = await bot.tree.sync()
    print("Logged on as {0}!".format(bot.user))
    print(f"{len(slash)} slash commands loaded.")

# meme
@bot.tree.command(name="meme", description="Get a random meme from Reddit")
async def meme(interaction: discord.Integration):
    res = requests.get('https://meme-api.com/gimme')
    data = res.json()
    await interaction.response.send_message(data["url"])

# raiderio
@bot.tree.command(name="score", description="Get Raider.IO Mythic+ score")
async def score(interaction: discord.Integration, region: str, realm: str, name: str):
    url = f"https://raider.io/api/v1/characters/profile?access_key=RIOFhQ9geZ5cazXpVQ5X4PPKk&region={region}&realm={realm}&name={name}&fields=mythic_plus_scores_by_season:current"
    res = requests.get(url)

    if res.status_code != 200:
        await interaction.response.send_message("❌ Failed to retrieve score ❌")

    # try:
    #     data = res.json()
    #     score = data["mythic_plus_scores_by_season"][0]["scores"]["all"]
    #     msg = f"**{name.title()}** (**{realm.title()}**, **{region.upper()}**)'s current M+ score is **{score}**"
    #     await interaction.response.send_message(msg)

    try:
        data = res.json()
        score = data["mythic_plus_scores_by_season"][0]["scores"]["all"]
        char_class = data.get("class", "Unknown")
        race = data.get("race", "Unknown")
        thumbnail = data.get("thumbnail_url", "")

        embed = discord.Embed(
            title=f"**{name.title()}**'s Mythic+ Score",
            description=f"**Realm**: `{realm.title()}`\n**Region**: `{region.upper()}`",
            color=class_color.get(char_class, 0x2F3136)
        )
        embed.add_field(name="Score", value=f"**{score}**", inline=True)
        embed.add_field(name="Class / Race", value=f"{char_class} / {race}", inline=True)

        if thumbnail:
            embed.set_thumbnail(url=thumbnail)

        await interaction.response.send_message(embed=embed)

    except (KeyError, IndexError):
        return interaction.response.send_message("⚠️ Score data not found ⚠️")

bot.run(TOKEN)