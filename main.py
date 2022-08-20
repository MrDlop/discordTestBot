import asyncio

import disnake
from disnake.ext import commands
from config import settings_ds

intent = disnake.Intents.all()
bot = commands.Bot(command_prefix=settings_ds['prefix'], intents=intent)


@bot.command()
async def test(ctx):
    """
    Test text message
    :param ctx:
    :return:
    """
    await ctx.send(f'Hello, {ctx.message.author.mention}!')


@bot.command()
async def afk(ctx, time: int):
    """
    AFK personal settings
    :param ctx:
    :param time: time - AFK
    :return:
    """
    await ctx.send(f'Hello, {ctx.message.author.mention}! Ваше время до AFK {time} минут')


@bot.command()
async def create_channel(ctx, name):
    """
    Create user channel
    :param ctx:
    :param name: name channel
    :return:
    """
    channel = await ctx.guild.create_voice_channel(name)
    if not (ctx.message.author.voice is None):
        await ctx.message.author.move_to(channel)
    else:
        await ctx.send(f'Move to some voice channel')
        await asyncio.sleep(10)
        if len(channel.members) == 0:
            await channel.delete()
        return

    def check(a, b, c):
        return len(channel.members) == 0

    await bot.wait_for('voice_state_update', check=check)
    await channel.delete()


bot.run(settings_ds['token'])
