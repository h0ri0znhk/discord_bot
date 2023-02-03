import discord
import os
import logging
from discord.ext import commands, tasks
from dotenv import load_dotenv

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

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
    load_dotenv()
    void = os.getenv('VOID_CHANNEL')
    hole = os.getenv('BLACKHOLE_CHANNEL')

    void_channel = bot.get_channel(int(void))
    hole_channel = bot.get_channel(int(hole))

    # get message list
    # messages = [message async for message in void_channel.history(limit=999)]
    # for m in messages:
    #     print(f'{m.content}')

    deleted = await void_channel.purge()
    for message in deleted:

        # build an id - username dict
        users_mentions = {}
        for mention in message.mentions:
            users_mentions[mention.id] = mention.name+'#'+mention.discriminator

        clean_message = message.content

        # convert all mentions to human-readable names (instead of raw id's)
        for key in users_mentions:
            clean_message = clean_message.replace(str(key), users_mentions[key])

        await hole_channel.send(f'**{message.author.name}#{message.author.discriminator}** '
                                f'posted ```{clean_message}```')
    print(f'redirected {len(deleted)} message(s) in {void_channel.name}')


@bot.command()
async def meets(ctx):
    load_dotenv()
    category_string = os.getenv('CATEGORY')

    for category in ctx.message.guild.categories:
        meetup_channel_list = []
        if category.name == category_string:
            channels = category.channels
            for c in channels:
                meetup_channel_list.append(c.name)
            resp = '\n'.join(meetup_channel_list)
            await ctx.send(resp)

bot.run(TOKEN, log_handler=handler)
