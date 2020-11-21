from discord import File
from redbot.core import commands
from . import clearsky, txtparser


class Weather(commands.Cog):
    """My custom cog"""

    # @commands.command()
    # async def weather2(self, ctx):
    #     """This does stuff!"""
    #     # Your code will go here
    #     a = await source.getWeather()
    #     await ctx.send(a)

    @commands.command()
    async def weather(self, ctx):
        async with ctx.channel.typing():
            # images
            f3 = await clearsky.getWeatherImage(r"http://www.cleardarksky.com/c/GMUObVAkey.html")
            sendF3 = File(f3, filename='gmu.png')
            # await ctx.send()

            # (no) go status
            s3 = txtparser.message()
            msg = "GMU Observatory: {}".format(s3)

            await ctx.send(msg, file=sendF3)
