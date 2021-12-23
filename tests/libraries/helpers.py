import requests
import re
import pandas as pd
from urllib.parse import urlparse


def parse_url(input):
    return urlparse(input)


def get_db_host(input):
    p = re.compile('^(http|https):\/\/([^:/]+):?([0-9]{1,6})?.*')
    m = p.match(input)
    if m:
        if m.lastindex == 3:
            return m[2], m[3]
        return m[2], 80
    else:
        raise Exception('Host is not present at ' + input)
