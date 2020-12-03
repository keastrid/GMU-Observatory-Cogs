import asyncio
import requests

from discord import File
from redbot.core import commands
from . import clearsky, txtparser


class Weather(commands.Cog):
    """Weather cog for pulling data from ClearDarkSky"""

    @commands.command()
    async def weatherimage(self, ctx):
        async with ctx.channel.typing():
            s = requests.Session()

            # images
            hasImg, img, imgURL = await clearsky.getWeatherImage(s, r"http://www.cleardarksky.com/c/GMUObVAkey.html")
            await asyncio.sleep(2)
            # await ctx.send()

            # (no) go status
            s3 = txtparser.message(s)
            msg = "GMU Observatory: {}".format(s3)

            if not hasImg:
                await ctx.send("Failed to download image. Please try again later.")
            else:
                sendF3 = File(img, filename='forecast.png')
                await ctx.send(msg, file=sendF3)

    @commands.command()
    async def weather(self, ctx):
        async with ctx.channel.typing():
            s = requests.Session()

            # images
            hasImg, img, imgURL = await clearsky.getWeatherImage(s, r"http://www.cleardarksky.com/c/GMUObVAkey.html")
            await asyncio.sleep(2)
            # await ctx.send()

            # (no) go status
            s3 = txtparser.message(s)
            msg = "GMU Observatory: {}".format(s3)

            if not hasImg:
                await ctx.send(msg + "\nImage failed to download, defaulting to embed...\n"
                                     "The embed seen may not reflect the image at the time of this command.\n" +
                               "{}".format(imgURL))
            else:
                sendF3 = File(img, filename='forecast.png')
                await ctx.send(msg, file=sendF3)
