import os
import time
from typing import Final

import discord
from discord.ext import commands
from dotenv import load_dotenv

# Disclaimer: Due to there being a limit to how many times you can edit/send a message in discord per second,
# I have set it to wait 1 second everytime it edits a message.
cooldown: int = 1

# Put here the path to the text directory where you generated the text.
file_path = "text"

# BOT SETUP: Get bot token from .env file
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)



# BOT STARTUP
@bot.event
async def on_ready() -> None:
    print(f'{bot.user} is now running!')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")

    except Exception as e:
        print(f"Error syncing commands: {e}" )



# HANDLING INCOMING MESSAGES
@bot.event
async def on_message(message) -> None:
    if message.author == bot.user:
        return


    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)

    print(f'[{channel}] {username}: "{user_message}"')



# BAD APPLE COMMAND
@bot.tree.command(name="badapple", description="Play Bad Apple")
async def bad_apple(message: discord.Interaction):

    # PLAY THE FIRST FRAME
    frame = open(file_path + "/frame0.txt", 'r')
    msg = await message.channel.send("```" + frame.read() + "```")
    time.sleep(cooldown)
    frame.close()

    # START ON FRAME 43
    count = 0
    while count < len(os.listdir(file_path)):
        print("CURRENT FRAME: " + str(count))
        frame = open(file_path + "/frame" + str(count) + ".txt", 'r')
        text = "```" + frame.read() + "```" # sets text as monospace
        await msg.edit(content=text)
        time.sleep(cooldown)
        frame.close()
        count += 1

    await message.channel.send("DONE")



# MAIN ENTRY POINT
def main() -> None:
    bot.run(token=TOKEN)



if __name__ == '__main__':
    main()
