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

import curses

helptext = """azmirror

press up/down/pgup/pgdown to move cursor
press space to select file
press enter to enter folder, backspace to get out
press r to refresh
press c to upload
press e to toggle encryption
    encrypted files can only be decrypted with a special tool,
    the decryption key is provided at program exit
press q to quit

Copyright (C) 2019  Dinh Ngoc Tu

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""


class Help:
    def __init__(self, y0, x0, y1, x1):
        self.y0, self.x0 = y0, x0
        self.y1, self.x1 = y1, x1
        self.h = y1 - y0 + 1
        self.w = x1 - x0 + 1
        self.win = curses.newwin(self.h, self.w, self.y0, self.x0)

    def println(self, str=''):
        self.win.addnstr(self.row, 1, str, self.w - 2)  # border
        self.row = self.row + 1

    def render(self):
        self.win.border()
        self.row = 1
        for line in helptext.splitlines():
            self.println(line)

    def refresh(self):
        self.win.refresh()
