import sqlite3


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


if __name__ == '__main__':
    def selftest():
        print("-" * 80 + "\nTest pl.czang.rssSnake.db")

        p = Persistence("rssSnake.db")
        c = p.con.cursor()
        c.execute("select * from [Group]")
        print(c.fetchone())

        print("-" * 80 + "\nTest pl.czang.rssSnake.db finished")
    selftest()
