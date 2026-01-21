import pytest
from base import run_code, run_code_and_get_result

codes = [
    'print(1+2)',
    """
def add(a, b):
    return a + b
print('test')
r = add(1, 2)
print(r)
""",
    """
def add(a, b):
    return a + b
print('test')
__result__ = add(1, 3)
""",
]


@pytest.mark.parametrize('code', codes)
def test_code(code: str):
    resp = run_code(code)
    print(resp)
    assert resp is not None
    assert resp.get('success')
    assert resp.get('stdout')


@pytest.mark.parametrize('code', codes)
def test_code_and_get_result(code: str):
    resp = run_code_and_get_result(code)
    print(resp)
    assert resp is not None
    assert resp.get('success')
    assert resp.get('stdout')
