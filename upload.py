# Copyright (C) 2019  Dinh Ngoc Tu
#
# This file is part of azmirror.
#
# azmirror is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# azmirror is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with azmirror.  If not, see <https://www.gnu.org/licenses/>.

import contextlib
import subprocess
import zipfile


@contextlib.contextmanager
def create_uploader(target_url, encrypt):
    if encrypt:
        rwiz = subprocess.Popen(
            ['rwiz', 'e'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
    azcopy = subprocess.Popen(
        [
            'azcopy',
            'copy',
            '--log-level',
            'NONE',
            '--content-type',
            'application/octet-stream',
            target_url
        ],
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
