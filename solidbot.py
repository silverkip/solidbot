import discord
import math
import re
import random
import sqlite3 
import sys
from discord.ext import commands
import asyncio
import youtube_dl

bot = commands.Bot(command_prefix = ';')



@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    print('---------------')





"""
    Custom text modules
"""
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    elif message.content.lower().startswith('sharena'):
        if any(x in message.content.lower() for x in ['the mission', 'above all', 'most important']):
            with open('D:/Programming/Discord/solidbot/assets/audio/VOICE_Alfonse_Prince_of_Askr_SKILL_1.wav', 'rb') as fp:
                await message.channel.send(file=discord.File(fp, 'ABOVE_ALL.wav'))
        elif re.search('^sharena,?\ destroy', message.content.lower()):
            with open('D:/Programming/Discord/solidbot/assets/images/sharena-destroy.png', 'rb') as fp:
                await message.channel.send('__**With pleasure.**__', file=discord.File(fp, 'ladies_first.png'))
    else:
        try:
            await bot.process_commands(message)
        except:
            raise





"""
    Arithmetic modules
"""
@bot.command(aliases=['sum'])
async def add(ctx, *args: str):
    """Adds multiple numbers together (decimal format only)."""
    try: 
        result = 0
        for i in args:
            result += float(i)
        if result == math.floor(result):                # check if float carries .000...
            result = int(result)
    except: 
        await ctx.send('Usage: ;add n1 n2 ...')
        return
    await ctx.send(result)

@bot.command(aliases=['mult'])
async def multiply(ctx, *args: str):
    """Multiplies multiple numbers together (decimal format only)."""
    try: 
        result = 1
        for i in args:
            result *= float(i)
        if result == math.floor(result):                # check if float carries .000...
            result = int(result)
    except: 
        await ctx.send('Usage: ;mult n1 n2 ...')
        return
    await ctx.send(result)

@bot.command(aliases=['sub'])
async def subtract(ctx, left: float, right: float):
    """Subtracts two numbers (decimal format only)."""
    try: 
        # input = str(left) + ', ' + str(right)
        await ctx.invoke(bot.get_command('add'), left, (right * -1))
    except: 
        await ctx.send('Usage: ;sub minuend subtrahend')
        return

@bot.command(aliases=['div'])
async def divide(ctx, left: float, right: float):
    """Divides one number by another (decimal format only)."""
    if right == 0:
        await ctx.send('Nice try!')
        return
    else:
        try: 
            await ctx.invoke(bot.get_command('multiply'), left, (1/right))
        except: 
            await ctx.send('Usage: ;div dividend divisor')
            return




"""
    RNG modules
"""
@bot.command(aliases=['pick'])
async def choose(ctx, *choices: str):
    """Chooses between multiple choices."""
    listChoices = ' '.join(choices).split(',')          # convert string into comma-separated list
    try:         
        result = random.choice(listChoices).lstrip()
    except:
        await ctx.send('Usage: ;choose thing a, thing b, ...')
        return
    await ctx.send(result)

@bot.command(aliases=['random'])
async def rng(ctx, left: int, right: int):
    """Picks a random integer between two integers."""
    try:
        randNum = random.randint(left, right)
    except:
        await ctx.send('Usage: ;rng min max')
        return
    await ctx.send(randNum)





"""
    Misc modules
"""
@bot.command()
async def time(ctx, TZ: str):
    """Returns the current time in a given time zone... except not right now"""
    return





"""
    Database modules
"""
@bot.command()
async def info(ctx, unitName: str):
    """Returns basic information about a Fire Emblem unit. THIS COMMAND IS A WORK IN PROGRESS."""
    try: 
        connection = sqlite3.connect('./data/FE4gen1.db')
    except Exception:
        raise
        return
    connection.row_factory = sqlite3.Row
    c = connection.cursor()
    query = f"SELECT * FROM Units WHERE name LIKE '{unitName}';"
    c.execute(query)
    row = c.fetchone()

    """
        THE FOLLOWING TEXT FORMATTING CURRENTLY ***ONLY*** WORKS FOR GEN1 FE4 UNITS
        THIS IS BECAUSE THE STRING FORMATTING USES SPECIFIC WIDTHS FOR SPECIFIC 
        ATTRIBUTES FROM THE QUERY RESULT. 
    """
    rowContents = ''
    for r in row:
        rowContents += str(r)
        rowContents += '\t'

    messageText = '>>> ' + str(row.keys()) + '\n' + rowContents
    await ctx.send(messageText)





"""
    Voice modules + setup
    The following voice modules are near-direct copies of basic_voice.py
"""
# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''


ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx, *, channel: discord.VoiceChannel):
        """Joins a voice channel"""

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()

    @commands.command()
    async def play(self, ctx, *, url):
        """Plays from a url (almost anything youtube_dl supports)"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('Now playing: {}'.format(player.title))

    @commands.command()
    async def stream(self, ctx, *, url):
        """Streams from a url (same as play, but doesn't predownload)"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('Now playing: {}'.format(player.title))

    @commands.command()
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send("Changed volume to {}%".format(volume))

    @commands.command()
    async def stop(self, ctx):
        """Stops and disconnects the bot from voice"""

        await ctx.voice_client.disconnect()

    # @oldplay.before_invoke
    @play.before_invoke
    @stream.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()





"""
    Cleanup modules
"""
@bot.event
async def on_disconnect():
    print('{0.user} is disconnecting.'.format(bot))
    await bot.close()





bot.add_cog(Music(bot))
bot.run('TOKEN', reconnect=True)