import asyncio

import disnake
from disnake.ext import commands
from config import settings_ds

intent = disnake.Intents.all()
bot = commands.Bot(command_prefix=settings_ds['prefix'], intents=intent)
a = dict()

@bot.command()
async def test(ctx):
    """
    Test text message
    """
    await ctx.send(f'Hello, {ctx.message.author.mention}!')


@bot.command()
async def afk(ctx, time: int):
    a[ctx.message.author.id] = time


@bot.command()
async def cc(ctx, name):
    """
    Create user channel
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


@bot.event
async def on_presence_update(before, after):
    channel = before.guild.get_channel(1010499309386608680)
    if disnake.Status.idle == after.status:
        await asyncio.sleep(a[before.id])
        if disnake.Status.idle == after.status:
            await before.move_to(channel, reason=None)


bot.run(settings_ds['token'])
