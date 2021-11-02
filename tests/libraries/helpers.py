import requests
import re
import pandas as pd
from urllib.parse import urlparse

def parse_url(input):
    return urlparse(input)
    
