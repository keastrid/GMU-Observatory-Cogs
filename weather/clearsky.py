import asyncio

import requests
from io import BytesIO
import re

vienna = r"http://www.cleardarksky.com/c/VnnVAkey.html"
center = r"http://www.cleardarksky.com/c/CntrvllVAkey.html"
base = r"http://www.cleardarksky.com"
imgUrlTemp = r"http://www.cleardarksky.com/c/{}csk.gif"

byteSizeThreshold = 2000

debug = False  # TODO DO NOT COMMIT THIS AS TRUE


# returns (hasImage, image bytes, imgURL)
async def getWeatherImage(s: requests.sessions, url: str):
    imgUrl = "Default Image URL"
    out = None
    status = False

    if idSearch := re.search(r"/c/([A-Za-z0-9]+)key.html", url):
        imgUrl = imgUrlTemp.format(idSearch.group(1))
    else:
        print("getWeatherImage: No valid URL found for image")
        status = False

    # pull image
    r = s.get(imgUrl, stream=True)

    out = BytesIO(r.content)

    if r.status_code != 200 and out.__sizeof__() < byteSizeThreshold:
        print("getWeatherImage: Image failed to download!")
        status = False

    return *outputImage(out, status), imgUrl  # I hope the * unpacks correctly


def outputImage(imgBytes: BytesIO, status: bool):
    if debug and not status:
        f = open("testImage.png", "wb")
        f.write(imgBytes.read())
        f.close()
    return status, imgBytes


if debug:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(getWeatherImage(requests.session(), "http://www.cleardarksky.com/c/GMUObVAkey.html"))
    loop.close()
