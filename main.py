import discord
from discord.ext import commands
from config import settings_ds

bot = commands.Bot(command_prefix=settings_ds['prefix'])
a = dict()


@bot.command()
async def test(ctx):
    await ctx.send(f'Hello, {ctx.message.author.mention}!')


@bot.command()
async def afk(ctx, time: int):
    await ctx.send(f'Hello, {ctx.message.author.mention}! Ваше время до AFK {time} минут')


@bot.command()
async def nc(ctx, name):
    a = await ctx.guild.create_voice_channel(str(name))
    print(a.id)


@bot.command()
async def dc(ctx, name):
    channel = discord.utils.get(ctx.guild.channels, name=name)

    if channel:
        await channel.delete()


bot.run(settings_ds['token'])
