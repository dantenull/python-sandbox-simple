import os
import subprocess
import tempfile
import logging
import re

from fastapi import FastAPI, APIRouter, Request
from pydantic import BaseModel

from .logger_utils import setup_logging

app = FastAPI()
setup_logging()
logger = logging.getLogger('app')


@app.get('/api/health')
def health_check():
    return {'status': 'healthy'}


class RunCodeData(BaseModel):
    code: str
    # timeout: int = 60
    get_result: bool = False


@app.post('/api/run_code')
def run_code(request: Request, data: RunCodeData):
    code = data.code
    get_result = data.get_result
    timeout = 60
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        code = code.strip()
        if get_result:
            code = f"""
import sys
sys.path.append('D:/code/python_sandbox/src')
import saver

result = saver.safe_run({repr(code)}, get_result={get_result})
if result:
    print(f'|final_result:{{result}}|')
"""
        else:
            code = f"""
import sys
sys.path.append('D:/code/python_sandbox/src')
import saver

saver.safe_run({repr(code)}, get_result={get_result})
"""
        f.write(code)
        code_file = f.name
    
    try:
        # 准备沙箱命令
        cmd = [
            './.venv_sd/Scripts/python.exe',
            code_file
        ]
        
        # 执行并捕获输出
        process = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=tempfile.gettempdir()
        )
        stdout = process.stdout.strip()
        if get_result and stdout:
            p = r'\|final_result:(.*?)\|'
            m = re.search(p, stdout)
            if m:
                stdout = m.group(1)
        result = {
            'success': process.returncode == 0,
            'stdout': stdout,
            'stderr': process.stderr,
            'returncode': process.returncode
        }
        logger.info(f'run_code result: {result}')
        return result
    except subprocess.TimeoutExpired:
        return {
            'success': False,
            'stdout': '',
            'stderr': f'Execution timeout after {timeout} seconds',
            'returncode': -1
        }
    except Exception as e:
        logger.error(f'run_code error', exc_info=True)
        return {
            'success': False,
            'stdout': '',
            'stderr': f'Internal error: {str(e)}',
            'returncode': -2
        }
    finally:
        # 清理临时文件
        if os.path.exists(code_file):
            os.unlink(code_file)


@app.post('/api/run_code_and_get_result')
def run_code_and_get_result(request: Request, data: RunCodeData):
    code = data.code
    timeout = 60
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        code = code.strip()
        code = f"""
import sys
sys.path.append('/app/src')
import saver

result = saver.safe_run_and_get_result({repr(code)})
if result:
    print(f'|final_result:{{result}}|')
"""
        f.write(code)
        code_file = f.name
    
    try:
        # 准备沙箱命令
        cmd = [
            './.venv_sd/Scripts/python.exe',
            code_file
        ]
        
        # 执行并捕获输出
        process = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=tempfile.gettempdir()
        )
        stdout = process.stdout.strip()
        if stdout:
            p = r'\|final_result:(.*?)\|'
            m = re.search(p, stdout)
            if m:
                stdout = m.group(1)
        
        result = {
            'success': process.returncode == 0,
            'stdout': stdout,
            'stderr': process.stderr,
            'returncode': process.returncode
        }
        logger.info(f'run_code_and_get_result result: {result}')
        return result
    except subprocess.TimeoutExpired:
        return {
            'success': False,
            'stdout': '',
            'stderr': f'Execution timeout after {timeout} seconds',
            'returncode': -1
        }
    except Exception as e:
        logger.error(f'run_code_and_get_result error', exc_info=True)
        return {
            'success': False,
            'stdout': '',
            'stderr': f'Internal error: {str(e)}',
            'returncode': -2
        }
    finally:
        # 清理临时文件
        if os.path.exists(code_file):
            os.unlink(code_file)


