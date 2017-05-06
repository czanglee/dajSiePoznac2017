from urllib.request import urlopen
import xml.etree.ElementTree as XmlTree
_author_ = 'czang'
_project_ = 'rssSnake'


class Rss:
    def __init__(self, url):
        self.channel = []
        self.url = url
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
        [print(p) for p in self.posts]
        print("\n")

    def __str__(self):
        return self.title


class Post:

    def __init__(self, item):
        self.title = item.find("title").text
        self.link = item.find("link").text
        self.postDate = item.find("pubDate").text
        nsDc = {'dc': 'http://purl.org/dc/elements/1.1/'}
        nsContent = {"content" : "http://purl.org/rss/1.0/modules/content/"}
        self.creator = item.find("dc:creator", nsDc).text
        self.description = item.find("description").text
        self.content = item.find("content:encoded", nsContent).text
        self.guid = item.find("guid").text

    def __str__(self):
        return "\t[%s] - %s by: %s\n\t\t%s\n" % (
                self.title
                , self.postDate
                , self.creator
                , self.description
                )


class Group:

    def __init__(self, group_id, title):
        self.id = group_id
        self.title = title

    def __str__(self):
        return "[%s] - %s" % (self.id, self.title)


if __name__ == '__main__':
    def selftest():
        print("-" * 80 + "\nTest pl.czang.rssSnake.data")
        url = "https://czang.pl/blog/category/dsp2017/feed/"
        Rss(url).show()
        print("-" * 80 + "\nTest pl.czang.rssSnake.data finished")
    selftest()
