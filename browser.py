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
            Browser.PAIR_DIR,
            curses.COLOR_CYAN,
            curses.COLOR_BLACK)
        curses.init_pair(
            Browser.PAIR_FILE_SELECTED,
            curses.COLOR_YELLOW,
            curses.COLOR_BLACK)
        curses.init_pair(
            Browser.PAIR_EMPTY,
            curses.COLOR_RED,
            curses.COLOR_WHITE)
        self.pathstack = [path]
        self.y0, self.x0 = y0, x0
        self.y1, self.x1 = y1, x1
        self.h = y1 - y0 + 1
        self.w = x1 - x0 + 1

    def render(self):
        pwd = self.pathstack[-1]
        self.dirs, self.files = Browser.list_dir(pwd)
        self.selected = [False] * len(self.files)

        self.cur = 0
        self.pad_top = self.y0
        self.draw_path()

    def idx_dir(self):
        return self.cur

    def idx_file(self):
        return self.cur - len(self.dirs)

    def cur_selected(self):
        if self.cur < len(self.dirs):
            return False
        elif self.cur - len(self.dirs) < len(self.files):
            return self.selected[self.cur - len(self.dirs)]
        else:
            raise ValueError

    def cur_item(self):
        if self.cur < len(self.dirs):
            return self.dirs[self.cur]
        elif self.cur - len(self.dirs) < len(self.files):
            return self.files[self.cur - len(self.dirs)]
        else:
            raise ValueError

    @staticmethod
    def list_dir(path: pathlib.Path):
        dirs = []
        files = []

        for item in path.iterdir():
            if item.is_dir():
                dirs.append(item)
            else:
                files.append(item)

        return dirs, files

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
            pos, 0, self.item_attr(item, cursor, self.cur_selected()))

    def draw_path(self):
        num = len(self.dirs) + len(self.files)
        self.pad = curses.newpad(max(num, self.h), self.w)
        pos = 0
        for d in self.dirs:
            self.pad.addnstr(pos, 0, d.name, self.w)
            self.pad.chgat(pos, 0, Browser.item_attr(d, False, False))
            pos += 1
        for f in self.files:
            self.pad.addnstr(pos, 0, f.name, self.w)
            self.pad.chgat(pos, 0, Browser.item_attr(f, False, False))
            pos += 1

    def refresh(self):
        n = len(self.dirs) + len(self.files)
        if self.cur < n:
            self.draw_item(self.cur_item(), self.cur, cursor=True)
        else:
            self.pad.addnstr(
                0, 0, 'Empty', self.w, curses.color_pair(Browser.PAIR_EMPTY))
        self.pad.refresh(self.pad_top, 0, self.y0, self.x0, self.y1, self.x1)

    def do_select(self):
        n = len(self.dirs) + len(self.files)
        if self.cur < n and self.cur_item().is_file():
            self.selected[self.idx_file()] = not self.selected[self.idx_file()]

    def do_down(self, amount=1):
        n = len(self.dirs) + len(self.files)
        if not n:
            return
        for _i in range(amount):
            pad_bottom = self.pad_top + self.h - 1
            self.draw_item(self.cur_item(), self.cur)
            self.cur += 1
            if self.cur >= n:
                self.cur = n - 1
            if self.cur > pad_bottom - Browser.SCROLL_OFFSET and self.cur < n - 1:
                self.pad_top += 1

    def do_up(self, amount=1):
        n = len(self.dirs) + len(self.files)
        if not n:
            return
        for _i in range(amount):
            self.draw_item(self.cur_item(), self.cur)
            self.cur -= 1
            if self.cur < 0:
                self.cur = 0
            if self.cur < self.pad_top + Browser.SCROLL_OFFSET and self.cur > 0:
                self.pad_top -= 1

    def push(self):
        if self.cur_item().is_dir():
            self.pathstack.append(self.cur_item())

    def pop(self):
        if len(self.pathstack) > 1:
            self.pathstack.pop()

    def get_selected(self) -> typing.List[pathlib.Path]:
        ret = []
        for s, f in zip(self.selected, self.files):
            if s:
                ret.append(f)
        return ret
