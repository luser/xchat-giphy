__module_name__ = "giphysearch"
__module_version__ = "1.0"
__module_description__ = "Search giphy for gifs to send to your friends"

import xchat
import os
import sys
import webbrowser

sys.path.insert(0, os.path.dirname(__file__))
import gifhax

def gif_cb(word, word_eol, userdata):
    ctx = xchat.get_context()
    chan = xchat.get_info("channel")
    def cb(url):
        if url:
            ctx.command("msg %s %s" % (chan, url))
    url = gifhax.search_gifs(word[1:], cb)
    if url:
        webbrowser.open_new(url)
    return xchat.EAT_ALL

xchat.hook_command("gif", gif_cb, help="/gif <words> Search for gifs about words")
