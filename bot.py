import discord
import requests
import json

def get_meme():
    response = requests.get('https://meme-api.com/gimme')
    json_data = json.loads(response.text)
    return json_data['url']

def get_raiderio_score(region, realm, name):
    url = f"https://raider.io/api/v1/characters/profile?access_key=RIOFhQ9geZ5cazXpVQ5X4PPKk&region={region}&realm={realm}&name={name}&fields=mythic_plus_scores_by_season:current"
    response = requests.get(url)

    if response.status_code != 200:
        return "Failed."
    
    data = response.json()

    try:
        score = data["mythic_plus_scores_by_season"][0]["scores"]["all"]
        return f"{name} ({realm}, {region})'s current M+ score is {score}"
    except (KeyError, IndexError):
        return "Failed."

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
        print('Start working! ')

    async def on_message(self, message):
        if message.author == self.user:
            return
        if message.content.startswith('$meme'):
            await message.channel.send(get_meme())
        if message.content.startswith('$score'):
            try:
                _, region, realm, name = message.content.split()
                result = get_raiderio_score(region, realm, name)
            except ValueError:
                result = "Please enter `$score Region Realm Name`"
            await message.channel.send(result)

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run('MTM1NzU4MjM3Njc2MjQ3NDY4OQ.GTDLSG.1pdIuUlpdm2S4VtxZ16R1ruuLiCznKBY8bFKGU')