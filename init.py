#!/usr/bin/python
import logging
from ghost import Ghost
from urlparse import urlparse

from tempfile import mkstemp

# thanks anon dufferzafar/Python-Scripts - Imgur.py 
CLIENT_ID = "a7c30de4f98751b"
# CLIENT_SECRET = "a188f1467cf86eae0d7a03e289e922235128160b"

# some more from  uppfinnarn/imgup - imgup.py 
# CLIENT_ID = "bb26658e6ad2d9a"

def ghostCapture(screen_url,web_timeout=10):

    gh = Ghost(display=":99",viewport_size=(800,600),wait_timeout=int(web_timeout), ignore_ssl_errors=True,log_level=logging.FATAL)
    ghost_page,resources= gh.open(screen_url, auth=('none', 'none'))
    img_path=mkstemp(suffix=".png")[1]
    gh.capture_to(img_path)

    return img_path

def usage(prog):
    print("usage: %s url"%prog)

if __name__ == "__main__":
    import sys
    url=None
    host=None
    try:
        url = sys.argv[1] 
        host=urlparse(url).netloc
    except Exception,e:
        print(e)
        usage(sys.argv[0])
        sys.exit(1)

    image_path=ghostCapture(url)
    import pyimgur
    im = pyimgur.Imgur(CLIENT_ID)

    uploaded = im.upload_image(image_path,title=host)
    print(uploaded.link)
