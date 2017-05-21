from optparse import OptionParser
import webbrowser
import sys
from db import Persistence
from rss import Rss

class Cmd:
    db_file = "rssSnake.db"

    def __init__(self):

        parser = OptionParser(description='rssSnake by czang.pl.')
        parser.add_option("-a", "--add"
                          , action="callback", callback=Cmd.channel_add
                          , type="string", dest="url"
                          , help="add new channel")
        parser.add_option("-v", "--view"
                          , action="callback", callback=Cmd.custom_view
                          , help="view all/channel/group")
        parser.add_option("-s", "--search"
                          , action="callback", callback=Cmd.search
                          , type="string", dest="search"
                          , help="search in posts")
        parser.add_option("-r" , "--remove"
                          , action="callback", callback=Cmd.remove
                          , help="Remove messages/channel/group...")
        parser.add_option("-e", "--export"
                          , action="callback", callback=Cmd.export_channels
                          , type="string", dest="filename"
                          , help="export channel list to OPML")
        parser.add_option("-i", "--import"
                          , action="callback", callback=Cmd.import_channels
                          , type="string", dest="filename"
                          , help="import channel list from OPML")
        parser.parse_args()



    @classmethod
    def channel_add(cls, option, opt, value, parser):
        print("Adding channel: %s" % (value,))
        p = Persistence(Cmd.db_file)
        r = Rss(value)
        ch = r.channel[0]
        p.channel_add(ch.title, r.url, ch.description, 1)
        print("Channels:")
        p.channel_list_print()

    @classmethod
    def custom_view(cls, option, opt, value, parser):
        print("Select what do you want to see:\n"
              "1. All messages\n"
              "2. Messages from a group\n"
              "3. Messages from a channel\n"
              )
        choice = None
        while choice not in range(1, 4):
            try:
                print("Please type your choice: ")
                choice = sys.stdin.read(1)
                choice = int(choice)
            except ValueError:
                pass
        print("your choice is: %i" % (choice,))
        p = Persistence(Cmd.db_file)
        p.channels_update()

        if choice == 1:
            print("Printing all messages")
            posts = p.post_get_all()
            for p in posts:
                print(p)

    @classmethod
    def search(cls, option, opt, value, parser):
        print("Searching for: %s" % (value,))

    @classmethod
    def import_channels(cls, option, opt, value, parser):
        print("Importing from: %s" % (value,))

    @classmethod
    def export_channels(cls, option, opt, value, parser):
        print("Importing from: %s" % (value,))

    @classmethod
    def remove(cls, option, opt, value, parser):
        print("Which messages do you want to remove:\n"
              "1. From group\n"
              "2. From channel\n"
              "3. Older than...\n"
              "4. Remove channel....\n"
              "5. Remove group....\n"
              )
        choice = None
        while choice not in range(1, 6):
            try:
                print("Please type your choice: ")
                choice = sys.stdin.read(1)
                choice = int(choice)
            except ValueError:
                print("Wrong choice!")
                choice = None
        print("your choice is: %i" % (choice,))

    @classmethod
    def open_in_browser(cls, url):
        """open URL in WebBrowser

            It's special method for CLT who said
            me that command line RSS reader is useless.
            Although it's command line program,
            you can open RSS message in your favorite browser :P
        """
        webbrowser.open_new_tab(url)


if __name__ == '__main__':
    def selftest():
        print("Test pl.czang.rssSnake.cmd\n"+"-" * 80)
        c = Cmd()


        #print("Open czang.pl in browser"); Cmd.open_in_browser("https://czang.pl");

        print("-" * 80 + "\nTest pl.czang.rssSnake.cmd finished")
    selftest()
