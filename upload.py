import contextlib
import subprocess
import zipfile


@contextlib.contextmanager
def create_uploader(target_url, encrypt=True):
    if encrypt:
        rwiz = subprocess.Popen(
            ['rwiz', 'e'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
    azcopy = subprocess.Popen(
        ['azcopy', 'cp', target_url],
        stdin=rwiz.stdout if encrypt else subprocess.PIPE,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL)
    try:
        if encrypt:
            key = rwiz.stderr.readline().decode().strip()
            if key.startswith('Key: '):
                key = key[len('Key: '):]
            with zipfile.ZipFile(rwiz.stdin, mode='w') as zf:
                yield zf, key
            rwiz.stdin.close()
            if rwiz.wait():
                raise Exception('rwiz failed')
        else:
            with zipfile.ZipFile(azcopy.stdin, mode='w') as zf:
                yield zf, None
            azcopy.stdin.close()
        if azcopy.wait():
            raise Exception('azcopy failed')
    except:
        if encrypt:
            rwiz.kill()
        azcopy.kill()
        raise
