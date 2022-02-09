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


def get_subscriber_and_subscription_from_location(input):
    p = re.compile('^.*/v1/([a-zA-Z0-9]+)/subscriptions/([a-zA-Z0-9]+)/?')
    m = p.match(input)
    if m:
        if m.lastindex == 2:
            return m[1], m[2]
        raise Exception('Only match ' + m.lastindex + ' and the expected is 2')
    else:
        raise Exception('Host is not present at ' + input)