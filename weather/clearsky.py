import asyncio

import requests
from bs4 import BeautifulSoup
from io import BytesIO

vienna = r"http://www.cleardarksky.com/c/VnnVAkey.html"
center = r"http://www.cleardarksky.com/c/CntrvllVAkey.html"
base = r"http://www.cleardarksky.com"


async def getWeatherImage(s: requests.sessions, url: str):
    # prep image retrieval
    page = s.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    imgTag = soup.find(id='csk_image')
    imgUrl = r"http://www.cleardarksky.com/c/GMUObVAcsk.gif"#base + imgTag.get('src')

    # pull image
    r = s.get(imgUrl, stream=True)

    return BytesIO(r.content)

# loop = asyncio.get_event_loop()
# loop.run_until_complete(getWeatherImage("http://www.cleardarksky.com/c/GMUObVAcsk.gif"))
# loop.close()