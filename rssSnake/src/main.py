from urllib.request import urlopen
import xml.etree.ElementTree as XmlTree

_author_ = 'czang'
_project_ = 'rssSnake'


class Rss:

    def __init__(self, url):
        self.channel = []
        file = urlopen(url).read()
        xml = XmlTree.fromstring(file)
        self.parse(xml)

    def parse(self, xml):
        for channel in xml.iter("channel"):
            c = Channel(channel)
            c.posts = [Post(item) for item in channel.iter("item")]
            self.channel.append(c)

    def show(self):
        for c in self.channel:
            c.show()


class Channel:

    def __init__(self, channel):
        self.posts = []
        self.title = channel.find("title").text
        self.description = channel.find("description").text

    def show(self):
        print("Channel: %s\n %s" % (self.title,self.description))
        [p.show() for p in self.posts]
        print("\n")


class Post:

    def __init__(self, item):
        self.title = item.find("title").text
        self.postDate = item.find("pubDate").text
        nsDc = {'dc': 'http://purl.org/dc/elements/1.1/'}
        nsContent = {"content" : "http://purl.org/rss/1.0/modules/content/"}
        self.creator = item.find("dc:creator", nsDc).text
        self.description = item.find("description").text
        self.content = item.find("content:encoded", nsContent).text

    def show(self):
        print("\t[%s] - %s by: %s\n\t\t%s\n" % (
                self.title
                , self.postDate
                , self.creator
                , self.description
                )
              )


channels = ("http://0dev.pl/category/daj-sie-poznac-2017/feed/"
            , "https://czang.pl/blog/category/dsp2017/feed/")
for u in channels:
    Rss(u).show()
