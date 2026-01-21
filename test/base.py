import json
from typing import Optional, Dict
from fastapi.testclient import TestClient
import requests

import sys
import os
sys.path.append(os.getcwd())
from src.app import app

client = TestClient(app)


def run_code(code: str) -> Optional[Dict]:
    # resp = requests.post(
    #     'http://localhost:8009/api/run_code',
    #     json={'code': code}
    # )
    resp = client.post(
        '/api/run_code',
        json={'code': code}
    )
    if resp.status_code != 200:
        return None
    try:
        result = resp.json()
    except json.JSONDecodeError:
        return None
    return result


def run_code_and_get_result(code: str) -> Optional[Dict]:
    # resp = requests.post(
    #     'http://localhost:8009/api/run_code_and_get_result',
    #     json={'code': code}
    # )
    resp = client.post(
        '/api/run_code',
        json={'code': code, 'get_result': True}
    )
    if resp.status_code != 200:
        return None
    try:
        result = resp.json()
    except json.JSONDecodeError:
        return None
    return result
