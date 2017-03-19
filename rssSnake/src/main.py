from urllib.request import urlopen
import xml.etree.ElementTree as ET

_author_ = 'czang'
_project_ = 'rssSnake'

url = "https://czang.pl/blog/category/dsp2017/feed/"
print('get data from: '+ url)
req = urlopen(url)
xmlData = req.read()
xml = ET.fromstring(xmlData)
for channel in xml.iter("channel"):
    print("Channel: "+channel.find("title").text)
    for item in channel.iter("item"):
        print("Post: "+item.find("title").text
                + " - " + item.find("pubDate").text
              )
