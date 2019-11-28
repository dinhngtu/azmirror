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

import configparser
import curses

from main import Main

if __name__ == "__main__":
    config = configparser.ConfigParser(interpolation=None)
    config.read('/etc/azmirror.conf')

    main = Main(
        config['DEFAULT']['root'],
        config['DEFAULT']['upload_path'],
        config['DEFAULT']['download_path'],
        config.getboolean('DEFAULT', 'encrypt', fallback=True))
    results = curses.wrapper(main.run)

    for target, key in results:
        print(f'URL: {target}')
        print(f'Key: {key}')
        print()
    _review = input('give a review:')
