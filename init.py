#!/usr/bin/python
import logging
from ghost import Ghost
from urlparse import urlparse

from tempfile import mkstemp

CLIENT_ID = "a7c30de4f98751b"
x1=0
y1=0
x2=1280
y2=1280
def ghostCapture(screen_url,web_timeout=20):

    gh = Ghost(display=":99",wait_timeout=int(web_timeout),viewport_size=(x2,y2), ignore_ssl_errors=True,log_level=logging.FATAL)
    ghost_page,resources= gh.open(screen_url, auth=('none', 'none'))

    img_path=mkstemp(suffix=".png")[1]
    gh.set_viewport_size(x2,y2)
    gh.capture_to(img_path,region=(x1,y1,x2,y2))

    return img_path

def usage(prog):
    print("usage: %s uri"%prog)

if __name__ == "__main__":
    import sys,os
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
    os.remove(image_path)
    print(uploaded.link)
