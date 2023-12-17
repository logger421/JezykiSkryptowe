import discord
import requests
from dotenv import dotenv_values

rasa_url = "http://localhost:5005/webhooks/rest/webhook"


async def send_message_to_rasa(message, user_message):
    payload = {"sender": message.author, "message": user_message}
    try:
        response = requests.post(rasa_url, json=payload)

        await message.channel.send(response)
    except Exception as e:
        print(e)


def run_discord_bot():
    config = dotenv_values(".env")
    intents = discord.Intents.default()
    intents.members = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'We have logged in as {client.user}')

    @client.event
    async def on_message(message):
        # break infinite loop
        if message.author == client.user:
            return

        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print(f'{username} typed: {user_message}, on channel: {channel}')

        await send_message_to_rasa(message, user_message)

    client.run(config["DISCORD_TOKEN"])
