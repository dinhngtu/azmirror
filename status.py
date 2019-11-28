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


class Status:
    STATUS_HEIGHT = 2

    def __init__(self, y0, x0, y1, x1):
        self.y0, self.x0 = y0, x0
        self.y1, self.x1 = y1, x1
        self.h = y1 - y0 + 1
        self.w = x1 - x0 + 1
        if self.h < Status.STATUS_HEIGHT:
            raise ValueError("status window too small")
        self.win = curses.newwin(
            Status.STATUS_HEIGHT, self.w, self.y0, self.x0)

    def render(self, text='Ready. Press "h" for help and copyright information.'):
        self.win.clear()
        self.win.hline(0, 0, curses.ACS_HLINE, self.w)
        self.win.addnstr(1, 0, text, self.w)

    def refresh(self):
        self.win.refresh()
