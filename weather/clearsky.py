import requests
from bs4 import BeautifulSoup
from io import BytesIO

vienna = r"http://www.cleardarksky.com/c/VnnVAkey.html"
center = r"http://www.cleardarksky.com/c/CntrvllVAkey.html"
base = r"http://www.cleardarksky.com"


def getWeatherImage(url: str):
    # prep image retrieval
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    imgTag = soup.find(id='csk_image')
    imgUrl = r"http://www.cleardarksky.com/c/GMUObVAcsk.gif"#base + imgTag.get('src')

    # pull image
    r = requests.get(imgUrl, stream=True)

    return BytesIO(r.content)
