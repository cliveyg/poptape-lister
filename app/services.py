# app/services.py
import requests
import json
from flask import current_app as app

# -----------------------------------------------------------------------------

def call_requests(url, headers):
    r = requests.get(url, headers=headers)
    return r

# -----------------------------------------------------------------------------

