import pytest
from base import run_code, run_code_and_get_result

codes = [
    'a=4;ifa == 5:',
    """
import os
os.system("echo 'hello world'")
""",
    """
with open('test.txt', 'w') as f:
    f.write('hello world')
""",
    """
import requests
resp = requests.get('http://baidu.com/')
print(resp.text)
""",
]


@pytest.mark.parametrize('code', codes)
def test_codee_and_get_result(code: str):
    resp = run_code_and_get_result(code)
    print(resp)
    assert resp is not None
    assert not resp.get('success')
