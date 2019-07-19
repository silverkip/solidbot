import math
import re
import random
import discord
import youtube_dl
from discord.ext import commands

bot = commands.Bot(command_prefix = ';')



@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    print('---------------')
    # main
    # channel = client.get_channel(517197086425350146)
    # testburger
    testburger = bot.get_channel(597934627050749963)
    #mattChat = bot.get_channel(426613372025569280)
    await testburger.send('WIP early build. Prefix commands with ;')
    await testburger.send('Current commands are add, mult, sub, div, & pick.')
    #await mattChat.send('WIP early build. Prefix commands with ;')
    #await mattChat.send('Current commands are add/sum, multiply/mult, subtract/sub, divide/div pick/choose.')



@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    elif message.content.lower().startswith('sharena'):
        await message.channel.send('Hello!')
    await bot.process_commands(message)

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


bot.run('NjAwODc1MDU0NzMyOTM1MTY5.XS6J-g.Hi5TnhOJxJf72QLfGMIaDXagABY')