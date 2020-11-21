import requests
import re
from datetime import datetime, timedelta
import pytz
from typing import List

url = r"https://www.cleardarksky.com/txtc/GMUObVAcsp.txt"
tz = pytz.timezone("US/Eastern")
today = datetime.now(tz).replace(hour=10, minute=0)
tomorrow = today + timedelta(days=1)


# pull the site's text
def getSiteData(url2: str):
    page = requests.get(url2)
    return page.text


def parseSiteData(data: str):
    blocks = re.findall(r"(\"[0-9-\s:]+\",[\s0-9]+,[\s0-9]+,[\s0-9]+,[(\s0-9)|None]+,[\s0-9]+,[\s0-9]+,[\s0-9]+)", data,
                        re.MULTILINE)
    dBlocks = re.findall(r'("[0-9-\s:]+",[\s0-9.-]+,[\s0-9.-]+,[\s0-9.-]+\))', data,
                         re.MULTILINE)
    blockData = []
    dBlockData = []
    for block in blocks:
        blockData.append(parseBlockData(block))
    for dBlock in dBlocks:
        dBlockData.append(parseDarknessBlocks(dBlock))
    relevantData = [d for d in mergeListMaps(blockData, dBlockData) if today < d["date"] < tomorrow]
    goodTimes = [d["date"] for d in filterTonight(relevantData)]
    print(goodTimes)
    ranges = checkRanges(goodTimes)
    print(ranges)
    msg = ""
    for r in ranges:
        if r:
            (start, end) = r
            msg += " ({} to {})".format(start.strftime("%H:%M"), end.strftime("%H:%M"))
    if msg != "":
        msg = "Observing is a GO! Found the following acceptable time range(s) (24Hr time):\n" \
              + msg.replace(") (", "), (")
    else:
        msg = "Observing is a NO GO! No 3 hour time window could be composed!"
    return msg


# Get all contiguous time ranges that are no less than 3 hours long
def checkRanges(ts: List[datetime]) -> List[List[datetime]]:
    if not ts:
        return []
    c = ts[0]
    pointer = 0

    ps: List[List[datetime]]
    ps = [[]]

    for t in ts:
        if not ps[pointer]:
            ps.append([])
        if (t-c).total_seconds() == 3600:
            ps[pointer].append(t)
        else:
            if ps[pointer]:
                pointer += 1
        c = t
    return [p[::len(p)-1] for p in ps if len(p) >= 3]


# Filter weather conditions
def filterTonight(data: list):
    ts = [b for b in data if 5 < b["temp"] < 18]
    cs = [b for b in ts if b["cloud"] >= 3]
    ws = [b for b in cs if b["wind"] > 1]
    hs = [b for b in ws if b["hum"] < 13]
    return hs


# Merge list of nights with the weather data, discarding daytime
def mergeListMaps(blocks: list, dBlocks: list):
    dates = [dBlock["date"] for dBlock in dBlocks if dBlock["isNight"]]
    bs = [b for b in blocks if b["date"] in dates]
    return bs


# Block Format: Local Time	cloud2	trans2	seeing2	smoke	wind2	hum2	temp2
# For meaning of the numeric forecast
# values, see https://www.cleardarksky.com/t/*_forecast_scale.txt, where * is cloud2,trans2,seeing2,wind2,
# hum2 or temp2.
def parseBlockData(block: str):
    block = block.replace('"', '')
    block = block.replace('\t', '')
    block = block.replace('None', '0')  # treat no data as no weather
    (date, cloud, trans, see, smoke, wind, hum, temp) = block.split(",")
    dateP = datetime.strptime(date, "%Y-%m-%d %X")
    # print(dateP.replace(tzinfo=tz) > today)
    data = {"cloud": int(cloud), "trans": int(trans), "see": int(see), "smoke": int(smoke), "wind": int(wind),
            "hum": int(hum), "temp": int(temp), "date": dateP.replace(tzinfo=tz)}
    return data


# sky darkness
# Local time	limiting_magnitude	sun_altitude	moon_altitude
def parseDarknessBlocks(dBlock: str):
    dBlock = dBlock.replace('"', '')
    dBlock = dBlock.replace('\t', '')
    dBlock = dBlock.replace(')', '')
    (date, limitMag, sunAlt, moonAlt) = dBlock.split(",")
    dateP = datetime.strptime(date, "%Y-%m-%d %X")
    data = {"date": dateP.replace(tzinfo=tz), "isNight": (float(limitMag) >= 2.1)}
    return data


def message():
    global url
    global tz
    global today
    global tomorrow
    url = r"https://www.cleardarksky.com/txtc/GMUObVAcsp.txt"
    tz = pytz.timezone("US/Eastern")
    today = datetime.now(tz).replace(hour=10, minute=0)
    tomorrow = today + timedelta(days=1)
    data = getSiteData(url)
    return parseSiteData(data)

print(message())