import re
from ..base import Pipe


parts = [
    r'(?P<host>\S+)',                   # host %h
    r'\S+',                             # indent %l (unused)
    r'(?P<user>\S+)',                   # user %u
    r'\[(?P<time>.+)\]',                # time %t
    r'"(?P<request>.*)"',               # request "%r"
    r'(?P<status>[0-9]+)',              # status %>s
    r'(?P<size>\S+)',                   # size %b (careful, can be '-')
    r'"(?P<referrer>.*)"',              # referrer "%{Referer}i"
    r'"(?P<agent>.*)"',                 # user agent "%{User-agent}i"
]

pattern = re.compile(r'\s+'.join(parts)+r'\s*\Z')


class HttpElfParser(Pipe):
    """Parse raw http log (in Extended Log Format) to log event.
    """
    def notify(self, logline):
        if logline.event_type == 'raw_log':
            d = pattern.match(logline.payload).groupdict()
            self.emit('parsed_log', d)


