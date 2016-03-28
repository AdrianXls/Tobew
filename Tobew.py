import datetime
import logging
import time

import json
import os
import discord
import pafy
import requests
import soundcloud
from bs4 import BeautifulSoup

start_time = time.time()

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='tobew.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

client = discord.Client()


def load_credentials():
    with open('credentials.json') as f:
        return json.load(f)


@client.event
async def on_ready():
    print('Connected!')
    print('Username: ' + client.user.name)
    print('ID: ' + client.user.id)


@client.event
async def on_message(message):
    if message.channel.is_private is not True:
        if message.content.startswith('!hello'):
            await command_hello(message)
        elif message.content.startswith('!define'):
            await command_define(message)
        elif message.content.startswith('!bda'):
            await command_bda(message)
        elif message.content.startswith('!abuse'):
            await command_abuse(message)
        elif message.content.startswith('!song'):
            await command_add_song(message)
        elif message.content.startswith('!topic'):
            await command_topic(message)
        elif message.content.startswith('!server'):
            await command_server(message)
        elif message.content.startswith('!slap'):
            await command_slap(message)
        elif message.content.startswith('!help'):
            await command_help(message)
        elif message.content.startswith('!user'):
            await command_user(message)
        elif message.content.startswith('!about'):
            await command_about(message)
        elif message.content.startswith('!debug'):
            if message.author.id == '98468948634271744':
                await command_debug(message)
        elif message.content.startswith('┬─┬ ノ( ゜-゜ノ)'):
            await command_tableflip(message)


async def command_hello(message):
    await client.send_message(message.channel, 'Hello {0.author.mention}! I\'m a friendly bot.'.format(message))


async def command_bda(message):
    await client.send_message(message.channel, 'http://betterdiscord.net/home/')


async def command_define(message):
    try:
        saved_word = message.content[len('!define '):]
        split_word = saved_word.split()
        define_word = requests.get("http://www.urbandictionary.com/define.php?term={}".format(saved_word))
        soup = BeautifulSoup(define_word.content, "html.parser")
        meaning = soup.find("div", attrs={"class": "meaning"}).text
        no_definition = soup.find("p").text
        msg = '{0.author.mention}, here is what Urban Dictionary knows about the {1} \"{2}\": {3}Example: {4}'
        if no_definition == "There aren't any definitions for {} yet.".format(saved_word):
            await client.send_message(message.channel, 'Sorry, there\'s no definition.')

        elif len(split_word) > 1:
            example = soup.find("div", attrs={"class": "example"}).text
            await client.send_message(message.channel, msg.format(message, "phrase", saved_word, meaning, example))

        elif len(split_word) == 1:
            example = soup.find("div", attrs={"class": "example"}).text
            await client.send_message(message.channel, msg.format(message, "word", saved_word, meaning, example))

    except discord.errors.HTTPException:
        await client.send_message(message.channel, 'Character limit hit!')


async def command_abuse(message):
    await client.send_message(message.channel, 'https://i.imgur.com/pNVE5nr.jpg')


async def command_add_song(message):
    if message.content[len('!song '):25:1] == "https://www.youtube":
        saved_url = message.content[len('!song '):]
        video = pafy.new(saved_url)
        await client.send_message(discord.Object(105572103561977856), '{} {}'.format(saved_url, video.title))

    elif message.content[len('!song '):24:1] == "https://soundcloud":
        saved_url = message.content[len('!song '):]
        soundcloud_client = soundcloud.Client(client_id="aca0717cc59f9b05c3932b5718f2f4f7")
        track = soundcloud_client.get('/resolve', url=str(saved_url))
        await client.send_message(discord.Object(105572103561977856), '{} {}'.format(saved_url, track.title))


async def command_topic(message):
    args = message.content.split()
    if len(args) >= 2:
        if message.author.id == '98468948634271744':
            args = message.content
            await client.edit_channel(message.channel, topic=args[len('!topic set '):])
            await client.send_message(message.channel, 'Channel topic has been set.')

    else:
        await client.send_message(message.channel, 'The topic for this channel is: {}'.format(message.channel.topic))


async def command_server(message):
    server = message.channel.server
    online = str(len([m.status for m in server.members if str(m.status) == "online" or str(m.status) == "idle"]))
    await client.send_message(message.channel,
                              '**Server name:** {}\n'
                              '**Server ID:** {}\n'
                              '**Server icon:** {}\n'
                              '**Server region:** {}\n'
                              '**Server created on:** {}\n'
                              '**Members:** {}/{}'.format(
                                  message.channel.server.name,
                                  message.channel.server.id,
                                  message.channel.server.icon_url,
                                  message.channel.server.region,
                                  message.channel.server.created_at,
                                  online,
                                  str(len(message.channel.server.members))))


async def command_slap(message):
    try:
        member = discord.utils.find(lambda m: m.name == message.content[len('!slap '):], message.channel.server.members)
        await client.send_message(message.channel,
                                  '*slaps {} around a bit with a large trout.*'.format(member.mention))
    except (AttributeError, IndexError):
        await client.send_message(message.channel, 'User was not found.')


async def command_help(message):
    await client.send_message(message.author,
                              '**!hello**\n'
                              '**!user** - Returns info of the desired user.\n'
                              '**!bda**\n'
                              '**!define** - Uses Urban Dictionary to fetch a definition for the desired word.\n'
                              '**!abuse**\n'
                              '**!song** - Adds a song to the <#105572103561977856> channel.\n'
                              '**!topic**\n'
                              '**!server** - Prints some basic info of the server.\n'
                              '**!slap**\n'
                              '**!about**\n'
                              '**!help**')


async def command_user(message):
    try:
        member = discord.utils.find(lambda m: m.name == message.content[len('!user '):], message.channel.server.members)
        await client.send_message(message.channel,
                                  '**Username:** {}\n'
                                  '**ID:** {}\n'
                                  '**Discriminator:** {}\n'
                                  '**Avatar:** {}\n'
                                  '**Joined at:** {}\n'
                                  '**Status:** {}'.format(member.name, member.id, member.discriminator,
                                                          member.avatar_url,
                                                          member.joined_at, member.status))
    except AttributeError:
        await client.send_message(message.channel, 'User was not found.')


async def command_about(message):
    uptime = str(datetime.timedelta(seconds=int(time.time() - start_time)))
    await client.send_message(message.channel, '**About me:**\n'
                                               'Author: Toosmo (Discord ID: 98468948634271744)\n'
                                               'Library: discord.py {} (Python)\n'
                                               'Uptime: **{} days, {} minutes and {} seconds**'
                              .format(discord.__version__, uptime[:1], uptime[2:4], uptime[5:7]))


async def command_debug(message):
    args = message.content[len('!debug '):].strip('` ')
    try:
        result = eval(args)
        await client.send_message(message.channel, '```Python\n{}\n```'.format(result))
    except Exception as e:
        result = '{0.__name__}: {1}'.format(type(e), e)
        await client.send_message(message.channel, '```Python\n{}\n```'.format(result))
        
async def command_tableflip(message):
    await client.send_message(message.channel,
                              '( ° ͜ʖ͡°)╭∩╮')

local = 0

if local == 0:
    client.run(os.environ['USER'], os.environ['PASSWORD'])
elif local == 1:
    credentials = load_credentials()
    client.run(credentials['email'], credentials['password'])
