import requests
import re
import pandas as pd
from urllib.parse import urlparse

def is_url(input):
    return urlparse(input)
    
