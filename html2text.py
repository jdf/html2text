from __future__ import with_statement
from subprocess import PIPE, Popen
import re

"""
To the extent possible under law, Jonathan Feinberg  has waived all copyright
and related or neighboring rights to html2text. This work is published from United States.
"""

class TextFormatter:
    def __init__(self, process=None, lynx='/usr/bin/lynx'):
        self.lynx = lynx
        self.process = process if process else lambda t:t

    def html2text(self, unicode_html_source):
        "Expects unicode; returns unicode"
        text = Popen([self.lynx,
                      '-assume-charset=UTF-8',
                      '-display-charset=UTF-8',
                      '-dump',
                      '-stdin'],
                      stdin=PIPE,
                      stdout=PIPE).communicate(input=unicode_html_source.encode('utf-8'))[0].decode('utf-8')
        return self.process(text)

    def htmlfile2text(self, path, encoding='utf-8'):
        "Returns unicode. Attempts to decode bytes in given file as utf-8 by default."
        with open(path, "r") as f:
            return self.html2text(f.read().decode(encoding))

if __name__ == "__main__":
    import sys
    try:
        with open(sys.argv[1], "r") as f:
            text = f.read()
    except:
        text = sys.stdin.read()
    encoding = sys.argv[2] if len(sys.argv) > 2 else 'utf-8'
    unicode_html = text.decode(encoding)
    print TextFormatter().html2text(unicode_html).encode('utf-8')
