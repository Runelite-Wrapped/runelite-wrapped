import discord
from discord.ext import commands
from yeelight import Bulb

TOKEN = 'MTA5MzQyNjQ4MDYxMDAyMTQ0OA.G1JUcC.Gbz2s1AuNll4Qj4PDFCJVcUh1u33iEzDRhPKow'
bulb_ip = '192.168.86.81'

intents = discord.Intents.default()
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents)

bulb = Bulb(bulb_ip)


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


@bot.command()
async def on(ctx):
    bulb.turn_on()
    await ctx.send('Turning Yeelight on.')


@bot.command()
async def off(ctx):
    bulb.turn_off()
    await ctx.send('Turning Yeelight off.')

if __name__ == '__main__':
    bot.run(TOKEN)
