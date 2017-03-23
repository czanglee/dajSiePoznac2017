from urllib.request import urlopen
import xml.etree.ElementTree as XmlTree

_author_ = 'czang'
_project_ = 'rssSnake'


class Rss:
    channel = []

    def __init__(self, url):
        req = urlopen(url)
        file = req.read()
        xml = XmlTree.fromstring(file)
        self.parse(xml)

    def parse(self, xml):
        for channel in xml.iter("channel"):
            c = Channel(channel.find("title").text)
            for item in channel.iter("item"):
                c.posts.append(
                    Post(item.find("title").text,
                         item.find("pubDate").text
                         )
                )
            self.channel.append(c)

    def show(self):
        for c in self.channel:
            c.show()


class Channel:
    title = None
    posts = []

    def __init__(self, title):
        self.title = title

    def show(self):
        print("Channel: "+self.title)
        for p in self.posts:
            p.show()


class Post:
    title = None
    postDate = None

    def __init__(self, title, postdate):
        self.title = title
        self.postDate = postdate

    def show(self):
        print("\t" + self.title + " - from: " + self.postDate)

##jedziemy z koksem
saved = ("http://0dev.pl/category/daj-sie-poznac-2017/feed/",
         "https://czang.pl/blog/category/dsp2017/feed/")
print(saved)
for u in saved:
    print(u + "\n")
    r = Rss(u)
    r.show()
