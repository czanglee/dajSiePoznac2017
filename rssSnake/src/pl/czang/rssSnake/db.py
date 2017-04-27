import sqlite3
import os.path
from pl.czang.rssSnake.data import Rss

class Persistence:

    def __init__(self,fileName):
        self.con = sqlite3.connect(fileName)
        c = self.con.cursor()
        c.execute("PRAGMA foreign_keys = ON;")
        c.execute("""
            create table if not exists [Group] (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL
                ,title TEXT NOT NULL
                )
            """)
        c.execute("""
            create table if not exists Channel (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL
                ,title TEXT
                ,url TEXT
                ,description TEXT
                ,tsInsert DATETIME
                ,groupId INTEGER
                ,FOREIGN KEY (groupId) REFERENCES [Group](id)
                )
            """)
        c.execute("""
            create table if not exists Post (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL
                ,title TEXT
                ,link TEXT
                ,postDate DATETIME
                ,creator TEXT
                ,description TEXT
                ,content TEXT
                ,guid TEXT
                ,channelId INTEGER
                ,FOREIGN KEY (channelId) REFERENCES Channel(id)
                )
            """)
        c.execute("""
            insert into [Group] (id,title)
                select 1 as id,"default" as title
                where not exists (
                    select 1 from [Group] where Id=1)
            """)

    def group_add(self, title):
        c = self.con.cursor()
        c.execute("insert into [Group] (title) values (?)", (title,))

    def channel_add(self, title, url, description, group_id):
        c = self.con.cursor()
        c.execute("""insert into Channel
            (title,url,description,tsInsert,groupId)
            values (?,?,?,datetime('now','localtime')
            ,?)""", (title, url, description, group_id))


if __name__ == '__main__':
    def selftest():
        print("-" * 80 + "\nTest pl.czang.rssSnake.db")
        db_file = "rssSnake_test.db"

        print("creating database")
        p = Persistence(db_file)
        c = p.con.cursor()

        print("selecting default group")
        c.execute("select * from [Group]")
        print(c.fetchone())

        print("inserting group and selecting it")
        p.group_add("DSP2017")
        c.execute("select * from [Group] where title = 'DSP2017'")
        print(c.fetchone())

        print("inserting amd se;ectomg channel")
        r = Rss("https://czang.pl/blog/category/dsp2017/feed/")
        for ch in r.channel:
            p.channel_add(ch.title, r.url, ch.description, 2)
        c.execute("select * from Channel")
        for row in c:
            print(row)

        p.con.close()

        print("deleting db file")
        if os.path.exists(db_file):
            os.remove(db_file)
        print("-" * 80 + "\nTest pl.czang.rssSnake.db finished")
    selftest()
