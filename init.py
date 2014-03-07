#!/usr/bin/python
import logging
from ghost import Ghost
from tempfile import mkstemp

def ghostCapture(screen_url,web_timeout=10):
    gh = Ghost(wait_timeout=int(web_timeout), ignore_ssl_errors=True)
    ghost_page,resources= gh.open(screen_url, auth=('none', 'none'))
    img_path=mkstemp(suffix=".png")[1]
    gh.capture_to(img_path)

    return img_path

def usage(prog):
    print("usage: %s url"%prog)

if __name__ == "__main__":
    import sys
    url=""
    try:
        url = sys.argv[1] 
    except:
        usage(sys.argv[0])
        sys.exit(1)
    print(ghostCapture(url))
