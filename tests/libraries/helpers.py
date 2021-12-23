import requests
import re
import pandas as pd
from urllib.parse import urlparse

def parse_url(input):
    return urlparse(input)

def get_host(input):
    p=re.compile('^(http|https)://(.*):.*')
    m=p.match(input)
    if m:
        return m[2]
    else:
        raise Exception('Host is not present at ' + input)
    
    
