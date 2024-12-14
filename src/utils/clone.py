import os
import shutil
import subprocess
from .decorators import async_timeout
from config import TMP_BASE_PATH, CLONE_TIMEOUT


@async_timeout(CLONE_TIMEOUT)
async def clone_repo(query: dict) -> str:
    #Clean up any existing repo 
    delete_repo(query['slug'])
    
    try:
        # Use synchronous subprocess for Windows compatibility
        result = subprocess.run(
            [
                "git",
                "clone",
                "--depth=1",
                "--single-branch",
                query['url'],
                query['local_path']
            ],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        raise Exception(f"Git clone failed: {e.stderr}")
    
def delete_repo(slug: str):
    path = f"{TMP_BASE_PATH}/{slug}"
    if os.path.exists(path):
        shutil.rmtree(path, ignore_errors=True)
