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
async def cc(ctx, name, _type_="common"):
    """
    /create_channel <Channel Name> <>
    """
    name = name[:100]
    if str(_type_) == "private":
        overwrites = {
            ctx.guild.default_role: disnake.PermissionOverwrite(view_channel=False),
            ctx.author: disnake.PermissionOverwrite(view_channel=True, manage_channels=True, mute_members=True,
                                                    deafen_members=True, move_members=True),
        }
        channel = await ctx.guild.create_voice_channel(str(name), overwrites=overwrites)
    else:
        channel = await ctx.guild.create_voice_channel(str(name))
    if ctx.author.voice is None:
        await ctx.send(f'{ctx.author.mention}, так как вы не находитесь ни в одном голосовом канале, '
                       f'я не могу самостоятельно переместить вас в созданный канал. Если в канала под названием "{str(name)}" никто не зайдёт, '
                       f'то он будет удален через 10 секунд.')
        await asyncio.sleep(10)
        if len(channel.members) == 0:
            await channel.delete()
            return
    else:
        await ctx.send(f'It works.')
        await ctx.message.author.move_to(channel)

    def check(a, b, c):
        return len(channel.members) == 0

    await bot.wait_for('voice_state_update', check=check)
    await channel.delete()


@bot.event
async def on_presence_update(before, after):
    channel = before.guild.get_channel(1010499309386608680)
    if disnake.Status.idle == after.status:
        await asyncio.sleep(a[before.id] if before.id in a else 60)
        if disnake.Status.idle == after.status:
            await before.move_to(channel, reason=None)


bot.run(settings_ds['token'])
