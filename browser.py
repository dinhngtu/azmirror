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
import pathlib
import typing


class Browser:
    PAIR_FILE = 0
    PAIR_DIR = 1
    PAIR_FILE_SELECTED = 2
    PAIR_EMPTY = 3
    SCROLL_OFFSET = 1

    def __init__(self, path: pathlib.Path, y0, x0, y1, x1):
        curses.init_pair(
            Browser.PAIR_DIR, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(
            Browser.PAIR_FILE_SELECTED,
            curses.COLOR_YELLOW,
            curses.COLOR_BLACK)
        curses.init_pair(
            Browser.PAIR_EMPTY, curses.COLOR_RED, curses.COLOR_WHITE)
        self.pathstack = [path]
        self.y0, self.x0 = y0, x0
        self.y1, self.x1 = y1, x1
        self.h = y1 - y0 + 1
        self.w = x1 - x0 + 1

    def render(self):
        pwd = self.pathstack[-1]
        self.items = sorted(
            list(pwd.iterdir()),
            key=lambda item: item.stat().st_mtime,
            reverse=True)
        self.selected = [False] * len(self.items)

        self.cur = 0
        self.pad_top = self.y0
        self.draw_path()

    def cur_selected(self):
        if self.cur < len(self.items):
            return self.selected[self.cur]
        else:
            raise ValueError

    def cur_item(self):
        if self.cur < len(self.items):
            return self.items[self.cur]
        else:
            raise ValueError

    @staticmethod
    def item_attr(item, cursor, selected):
        attr = curses.A_STANDOUT if cursor else 0
        if item.is_dir():
            return curses.color_pair(Browser.PAIR_DIR) | attr
        else:
            if selected:
                return curses.color_pair(Browser.PAIR_FILE_SELECTED) | attr
            else:
                return curses.color_pair(Browser.PAIR_FILE) | attr

    def draw_item(self, item, pos, cursor=False):
        self.pad.chgat(
            pos, 0, self.item_attr(item, cursor, self.selected[self.cur]))

    def draw_path(self):
        self.pad = curses.newpad(max(len(self.items), self.h), self.w)
        pos = 0
        for item in self.items:
            self.pad.addnstr(pos, 0, item.name, self.w)
            self.pad.chgat(pos, 0, Browser.item_attr(item, False, False))
            pos += 1

    def refresh(self):
        if self.cur < len(self.items):
            self.draw_item(self.cur_item(), self.cur, cursor=True)
        else:
            self.pad.addnstr(
                0, 0, 'Empty', self.w, curses.color_pair(Browser.PAIR_EMPTY))
        self.pad.refresh(self.pad_top, 0, self.y0, self.x0, self.y1, self.x1)

    def do_select(self):
        if self.cur < len(self.items) and self.cur_item().is_file():
            self.selected[self.cur] = not self.selected[self.cur]

    def do_down(self, amount=1):
        if not len(self.items):
            return
        for _i in range(amount):
            pad_bottom = self.pad_top + self.h - 1
            self.draw_item(self.cur_item(), self.cur)
            self.cur += 1
            if self.cur >= len(self.items):
                self.cur = len(self.items) - 1
            if self.cur > pad_bottom - Browser.SCROLL_OFFSET and self.cur < len(
                    self.items) - 1:
                self.pad_top += 1

    def do_up(self, amount=1):
        if not len(self.items):
            return
        for _i in range(amount):
            self.draw_item(self.cur_item(), self.cur)
            self.cur -= 1
            if self.cur < 0:
                self.cur = 0
            if self.cur < self.pad_top + Browser.SCROLL_OFFSET and self.cur > 0:
                self.pad_top -= 1

    def push(self):
        if self.cur < len(self.items) and self.cur_item().is_dir():
            self.pathstack.append(self.cur_item())

    def pop(self):
        if len(self.pathstack) > 1:
            self.pathstack.pop()

    def get_selected(self) -> typing.List[pathlib.Path]:
        ret = []
        for s, f in zip(self.selected, self.items):
            if s:
                ret.append(f)
        return ret
