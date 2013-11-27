#!/usr/bin/env python

import giphypop
import BaseHTTPServer
import time
import threading
import warnings

warnings.simplefilter("ignore", UserWarning)

class MyRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass

    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; encoding=utf-8")
            self.end_headers()
            self.wfile.write("""<!DOCTYPE html>
<head>
<title>gifs</title>
</head>
<body>
<p><a href="/f">NOPE</a>
<p>
%s
</body>""" % "\n".join('<a href="/g/%d"><img src="%s" width="%dpx" height="%dpx"></a>' % (i, u, w, h) for (i, (_, (u, w, h))) in enumerate(self.server.urls)))
        elif self.path.startswith("/f") or self.path.startswith("/g/"):
            if self.path[1] == "g":
                try:
                    self.server.chosen = int(self.path[3:])
                except:
                    pass
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; encoding=utf-8")
            self.end_headers()
            self.wfile.write("Close this window.")
            self.server.done = True
        else:
            self.send_error(404)

def server_thread(httpd, on_finished):
    while not httpd.done:
        httpd.handle_request()
    on_finished(httpd.urls[httpd.chosen][0] if httpd.chosen != -1 else None)

def run_server(server_class=BaseHTTPServer.HTTPServer,
               handler_class=MyRequestHandler,
               urls=[],
               on_finished=None):
    server_address = ('', 0)
    httpd = server_class(server_address, handler_class)
    httpd.done = False
    httpd.chosen = -1
    httpd.urls = urls
    t = threading.Thread(target=server_thread, args=(httpd, on_finished))
    t.start()
    return "http://%s:%d/" % httpd.server_address

def search_gifs(words, callback):
    g = giphypop.Giphy()
    urls=[(res.media_url, (res.fixed_width.url, res.fixed_width.width, res.fixed_width.height)) for res in g.search(phrase=" ".join(words))]
    if urls:
        return run_server(urls=urls, on_finished=callback)
    else:
        callback(None)
        return None

if __name__ == '__main__':
    import sys
    import webbrowser
    done = False
    def cb(url):
        global done
        done = True
        if url:
            print url
    url = search_gifs(sys.argv[1:], cb)
    if url:
        webbrowser.open_new(url)
        while not done:
            time.sleep(1)
