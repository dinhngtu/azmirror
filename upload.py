import contextlib
import subprocess
import zipfile


@contextlib.contextmanager
def create_uploader(target_url):
    rwiz = subprocess.Popen(
        ['rwiz', 'e'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    azcopy = subprocess.Popen(
        ['azcopy', 'cp', target_url],
        stdin=rwiz.stdout,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL)
    try:
        key = rwiz.stderr.readline().decode().strip()
        with zipfile.ZipFile(rwiz.stdin, mode='w') as zf:
            yield key, zf
        rwiz.stdin.close()
        if rwiz.wait():
            raise Exception('rwiz failed')
        if azcopy.wait():
            raise Exception('azcopy failed')
    except:
        rwiz.kill()
        azcopy.kill()
        raise
