#!/usr/bin/python
import logging
from ghost import Ghost
from urlparse import urlparse

from tempfile import mkstemp

CLIENT_ID = "a7c30de4f98751b"

def ghostCapture(screen_url,web_timeout=10):

    gh = Ghost(display=":99",viewport_size=(800,600),wait_timeout=int(web_timeout), ignore_ssl_errors=True,log_level=logging.FATAL)
    ghost_page,resources= gh.open(screen_url, auth=('none', 'none'))
    img_path=mkstemp(suffix=".png")[1]
    gh.capture_to(img_path)

    return img_path

def usage(prog):
    print("usage: %s uri"%prog)

if __name__ == "__main__":
    import sys
    url=None
    host=None
    try:
        url = sys.argv[1] 
        if not url.startswith("http"):
            url="http://"+url
        host=urlparse(url).netloc
    except Exception,e:
        print(e)
        usage(sys.argv[0])
        sys.exit(1)
    print("Capturing '%s'"%url)
    image_path=ghostCapture(url)
    import pyimgur
    im = pyimgur.Imgur(CLIENT_ID)

    uploaded = im.upload_image(image_path,title=host)
    print(uploaded.link)
