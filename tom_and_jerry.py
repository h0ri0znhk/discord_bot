import discord
import os
import logging
from discord.ext import commands, tasks
from dotenv import load_dotenv

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
VOID = os.getenv('VOID_CHANNEL')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='?', intents=intents)


@bot.listen()
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')
    task_loop.start()


@tasks.loop(seconds=30)
async def task_loop():
    channel = bot.get_channel(int(VOID))

    # get message list
    messages = [message async for message in channel.history(limit=999)]
    for m in messages:
        print(f'{m.content}')

    deleted = await channel.purge()
    print(f'Deleted {len(deleted)} message(s) in {channel.name}')


@bot.command()
async def meets(ctx):
    for category in ctx.message.guild.categories:
        meetup_channel_list = []
        if category.name == 'MEETUPS':
            channels = category.channels
            for c in channels:
                meetup_channel_list.append(c.name)
            resp = '\n'.join(meetup_channel_list)
            await ctx.send(resp)

bot.run(TOKEN, log_handler=handler)
