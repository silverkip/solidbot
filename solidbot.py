import math
import re
import random
import discord
import requests
from discord.ext import commands

bot = commands.Bot(command_prefix = ';')



@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    print('---------------')
#    await send_bot_message()

# async def send_bot_message():
#     while True:
#         text = input('Send message: ').split(' ', 1)
#         channelID = int(text[0])
#         messageText = text[1]
#         try: 
#             channel = bot.get_channel(channelID)
#             await channel.send(messageText)
#         except Exception:
#             raise





"""
    Custom text modules
"""
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    elif message.content.lower().startswith('sharena'):
        if any(x in message.content.lower() for x in ['the mission', 'above all', 'most important']):
            with open('./assets/audio/VOICE_Alfonse_Prince_of_Askr_SKILL_1.wav', 'rb') as fp:
                await message.channel.send(file=discord.File(fp, 'ABOVE_ALL.wav'))
        elif re.search('^sharena,?\ destroy', message.content.lower()):
            with open('./assets/images/sharena-destroy.png', 'rb') as fp:
                await message.channel.send('__**With pleasure.**__', file=discord.File(fp, 'ladies_first.png'))
    elif message.content.lower() == 'what' and message.author == 68568019751673856:
        with open('./assets/audio/VOICE_Julia_Nagas_Blood_MAP_2.wav', 'rb') as fp:
            await message.channel.send(file=discord.File(fp, 'what.wav'))
    await bot.process_commands(message)





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
    Voice modules
"""
@bot.command()
async def join(ctx):
    """Joins voice channel of current user."""
    try: 
        if not discord.opus.is_loaded():
            discord.opus.load_opus('libopus.so.1')
        userVoice = ctx.author.voice.channel
        await userVoice.connect()
    except Exception as e:
        await ctx.send('Unable to join voice channel.')
        print(e)
        return

@bot.command(aliases=['leave'])
async def stop(ctx):
    """Disconnects from current voice channel."""
    try: 
        if not discord.opus.is_loaded():
            discord.opus.load_opus('libopus.so.1')
        userVoice = ctx.author.voice.channel
        for vc in bot.voice_clients:
            if vc.guild == ctx.guild:
                await vc.disconnect()
    except Exception as e:
        await ctx.send('Unable to leave voice channel.')
        print(e)
        return





"""
    Cleanup modules
"""
@bot.event
async def on_disconnect():
    print('{0.user} is disconnecting.'.format(bot))
    await bot.close()





bot.run('NjAwODc1MDU0NzMyOTM1MTY5.XS6J-g.Hi5TnhOJxJf72QLfGMIaDXagABY')