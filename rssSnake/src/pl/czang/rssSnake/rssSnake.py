from pl.czang.rssSnake.data import Rss
import argparse

_author_ = 'czang'
_project_ = 'rssSnake'

parser = argparse.ArgumentParser(description='rssSnake by czang.pl.')
#https://docs.python.org/2/library/argparse.html#argparse.ArgumentParser

channels = ("http://0dev.pl/category/daj-sie-poznac-2017/feed/"
            , "https://czang.pl/blog/category/dsp2017/feed/")
for u in channels:
    Rss(u).show()
