import discord
import os
from discord.ext import commands, tasks
from dotenv import load_dotenv

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
    messages = [message async for message in channel.history(limit=123)]
    for m in messages:
        print(f'{m.content}')

    deleted = await channel.purge()
    print(f'Deleted {len(deleted)} message(s)')


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

bot.run(TOKEN)
