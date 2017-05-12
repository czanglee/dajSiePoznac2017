from pl.czang.rssSnake.data import Rss

_author_ = 'czang'
_project_ = 'rssSnake'

channels = ("http://0dev.pl/category/daj-sie-poznac-2017/feed/"
            , "https://czang.pl/blog/category/dsp2017/feed/")
for u in channels:
    Rss(u).show()
