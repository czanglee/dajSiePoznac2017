import sqlite3
import os.path
from pl.czang.rssSnake.data import Rss
from pl.czang.rssSnake.data import Group

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
                ,viewTime DATETIME
                ,FOREIGN KEY (channelId) REFERENCES Channel(id)
                )
            """)
        c.execute("""
            create unique index if not exists PostUniq ON Post(channelId,guid);

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

    def group_remove(self, group_id):
        if group_id == 1:
            raise Exception("You can not remove default group!")
        c = self.con.cursor()
        c.execute("delete from [Group] where id=?", (group_id,))

    def group_list(self):
        c = self.con.cursor()
        c.execute("select id,title from [Group] order by title")
        groups = []
        for row in c:
            groups.insert(groups.__len__(), Group(row[0], row[1]))
        return groups

    def channel_add(self, title, url, description, group_id):
        c = self.con.cursor()
        c.execute("""insert into Channel
            (title,url,description,tsInsert,groupId)
            values (?,?,?,datetime('now','localtime')
            ,?)""", (title, url, description, group_id))

    def channel_get_id(self, url):
        c = self.con.cursor()
        c.execute("select id from Channel where url=?", (url,))
        r = c.fetchone()
        if r is not None:
            return r[0]
        else:
            return None

    def channel_change_group(self, channel_id, group_id):
        c = self.con.cursor()
        c.execute("update Channel set groupId=? where id=?", (group_id, channel_id))

    def post_add(self,title, link, postDate, creator, description, content, guid, channel_id):
        c = self.con.cursor()
        try:
            c.execute("""insert into Post
                   (title,link,postDate,creator,description,content,guid,channelId)
                   values (?,?,?,?,?,?,?,?)""", (title, link, postDate, creator, description, content, guid, channel_id))
        except sqlite3.IntegrityError:
            pass


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
        ch = r.channel[0]
        p.channel_add(ch.title, r.url, ch.description, 2)
        c.execute("select * from Channel")
        for row in c:
            print(row)

        print("Get channel id by Url")
        channel_id = p.channel_get_id("https://czang.pl/blog/category/dsp2017/feed/")
        print(channel_id)
        print("Get channel id by not existing url")
        print(p.channel_get_id("spam"))

        print("Adding posts")
        for post in r.channel[0].posts:
            p.post_add(post.title, post.link
                       ,post.postDate, post.creator
                       , post.description, post.content
                       , post.guid, channel_id)
        c.execute("select id,title from Post where channelId=?",(channel_id,))
        for row in c.fetchall():
            print(row)

        print("Adding posts - the same again")
        for post in r.channel[0].posts:
            p.post_add(post.title, post.link
                       , post.postDate, post.creator
                       , post.description, post.content
                       , post.guid, channel_id)
        c.execute("select id,title from Post where channelId=?", (channel_id,))
        for row in c.fetchall():
            print(row)

        print("\nList groups:")
        p.group_add("remove me")
        groups = p.group_list()
        for g in groups:
            print(g)

        print("\nRemove group id=3:")
        p.group_remove(3)
        groups = p.group_list()
        for g in groups:
            print(g)

        print("\nChange Channel group")
        p.channel_change_group(1, 1)


        p.con.close()

        print("\ndeleting db file")
        if os.path.exists(db_file):
            os.remove(db_file)
        print("-" * 80 + "\nTest pl.czang.rssSnake.db finished")
    selftest()
