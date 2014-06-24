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
timeout=None
def ghostCapture(screen_url,web_timeout=20):
    import time
    gh = Ghost(display=":99",wait_timeout=int(web_timeout),
               viewport_size=(x2,y2), ignore_ssl_errors=True,
               log_level=logging.FATAL)
               
    ghost_page,resources= gh.open(screen_url, 
                auth=('none', 'none'))
    
    img_path=mkstemp(suffix=".png")[1]
    gh.set_viewport_size(x2,y2)
    time.sleep(timeout)
    gh.capture_to(img_path,region=(x1,y1,x2,y2))

    return img_path

def usage(prog):
    print("usage: visit-page uri [timeout]")

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
        usage(sys.argv[0])
        sys.exit(1)
    try:
        timeout=int(sys.argv[2])
        if not( 0 < timeout < 60):
            sys.stdout.write("timeout must be between 0 and 60 seconds\n")
            usage(sys.argv[0])
            sys.exit(1)
        sys.stdout.write("Timeout set to %d seconds\n"%timeout)
    except:
        timeout=0

    sys.stdout.write("Capturing '%s'\n"%url)
    sys.stdout.flush()
    image_path=ghostCapture(url)
    import pyimgur
    im = pyimgur.Imgur(CLIENT_ID)

    uploaded = im.upload_image(image_path,title=host)
    os.remove(image_path)
    print(uploaded.link)
