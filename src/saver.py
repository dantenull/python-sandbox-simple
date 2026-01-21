not_allowed_builtins = [
    'open',
    'dir',
    'compile',
    'exec',
    'eval',
    'execfile',
    'runfile',
    'input',
    'file',
    'exit',
    'quit',
]

safe_builtins = {}
for b in __builtins__:
    if b in not_allowed_builtins:
        continue
    safe_builtins[b] = __builtins__[b]

not_allowed_modules = [
    'os',
    'subprocess',
    'socket',
    'gc',
    'shutil',
    'platform',
    'urllib',
    'ftplib',
    'smtplib',
    'pickle',
    'marshal',
    'shelve',
    'ctypes',
    'resource',
    'fcntl',
    'pty',
    'termios',
    '_pickle',
    '_socket',
    '_ctypes',
]


def safe_import(name, *args, **kwargs):
    if name in not_allowed_modules:
        raise ImportError(f"Importing module {name} is not allowed")
    return __import__(name, *args, **kwargs)


safe_builtins['__import__'] = safe_import


def safe_run(code: str, get_result: bool = False):
    safe_globals = {
        '__builtins__': safe_builtins,
    }
    safe_locals = {}
    code_process = f"""
import sys
sys.setrecursionlimit(1000)

{code}
"""
    exec(code_process, safe_globals, safe_locals)
    if not get_result:
        return
    if not safe_locals:
        return
    print(f'safe_locals: {safe_locals}')
    if '__result__' in safe_locals:
        result = safe_locals['__result__']
    else:
        result = list(safe_locals.values())[-1]
    return result


# def safe_run_and_get_result(code: str):
#     safe_globals = {
#         '__builtins__': safe_builtins,
#     }
#     safe_locals = {}
#     code_process = f"""
# import sys
# sys.setrecursionlimit(1000)

# {code}
# """
#     exec(code_process, safe_globals, safe_locals)
#     if not safe_locals:
#         return
#     if '__result__' in safe_locals:
#         result = safe_locals['__result__']
#     else:
#         result = list(safe_locals.values())[-1]
#     return result
