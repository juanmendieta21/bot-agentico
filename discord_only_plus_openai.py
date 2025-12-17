from dotenv import load_dotenv
from openai import OpenAI
import discord
import os
import asyncio

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
oa_client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# ask openai  respond like a asistant
def call_openai(question):
    completion = oa_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", 
            "content": f"Respond maxmimun 1000 caracters like a helpful IA developer assistant to the following question: {question}"}
        ]
    )
    response = completion.choices[0].message.content
    print(response)
    return response


#set up intents and client
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# event for when the bot is ready
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')    

# event for when a message is received
@client.event
async def on_message(message):
  
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('$question'):
        print(f"Message: {message.content}")
        message_content = message.content.split("$question")[1]
        print(f"Question: {message_content}")
        try:
            response = await asyncio.to_thread(call_openai, message_content)
        except Exception as e:
            await message.channel.send("Error al consultar al servicio: " + str(e))
            return
        print(f"Assistant: {response}")
        print("---")
        await message.channel.send(response)


client.run(os.getenv("TOKEN"))