import collections
import curses
import curses.ascii
import pathlib
import os
import sys
import typing

NAME_MAX = 256
STATUS_HEIGHT = 1
SCROLL_OFFSET = 1


def run(stdscr):
    if not stdscr:
        # for completion only
        stdscr = curses.newwin()
        raise ValueError

    curses.curs_set(False)
    # dir
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    # selected (file only)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    stdscr.keypad(True)
    stdscr.refresh()

    h, w = curses.LINES, curses.COLS

    def list_dir(path: pathlib.Path):
        dirs = []
        files = []
        num = len(dirs) + len(files)

        for item in path.iterdir():
            if item.is_dir():
                dirs.append(item)
            else:
                files.append(item)

        return dirs, files

    def draw_path(
            dirs: typing.List[pathlib.Path], files: typing.List[pathlib.Path]):
        num = len(dirs) + len(files)
        pad = curses.newpad(num, NAME_MAX)
        pos = 0
        for d in dirs:
            pad.addnstr(pos, 0, d.name, NAME_MAX)
            pad.chgat(pos, 0, item_attr(d, False, False))
            draw_item(d, pad, pos)
            pos += 1
        for f in files:
            pad.addnstr(pos, 0, f.name, NAME_MAX)
            pad.chgat(pos, 0, item_attr(f, False, False))
            pos += 1
        return pad

    def item_at(x):
        if x < len(dirs):
            return dirs[x]
        elif x - len(dirs) < len(files):
            return files[x - len(dirs)]
        else:
            return None

    def selected_at(x):
        if x < len(dirs):
            return False
        elif x - len(dirs) < len(files):
            return selected[x - len(dirs)]
        else:
            return False

    def idx_dir(x):
        return x

    def idx_file(x):
        return x - len(dirs)

    def item_attr(item, cursor, selected):
        attr = 0
        attr = attr | (curses.A_STANDOUT if cursor else 0)
        if item.is_dir():
            return curses.color_pair(1) | attr
        else:
            if selected:
                return curses.color_pair(2) | attr
            else:
                return curses.color_pair(0) | attr

    def draw_item(item, pad, cur, cursor=False):
        pad.chgat(cur, 0, item_attr(item, cursor, selected_at(cur)))

    pathstack = [pathlib.Path('/mnt/d')]
    while True:
        stdscr.clear()
        stdscr.refresh()

        pwd = pathstack[-1]
        dirs, files = list_dir(pwd)
        nd, nf = len(dirs), len(files)
        n = nd + nf

        pad = draw_path(dirs, files)
        cur = 0
        pad_top = 0

        selected = [False] * nf

        while True:
            pad_bottom = pad_top + h - 1 - STATUS_HEIGHT
            draw_item(item_at(cur), pad, cur, cursor=True)
            pad.refresh(pad_top, 0, 0, 0, pad_bottom - pad_top, w - 1)
            cmd = stdscr.getch()

            if cmd == curses.ascii.ESC or cmd == ord('q'):
                return
            elif cmd == curses.KEY_DOWN:
                draw_item(item_at(cur), pad, cur)
                cur += 1
                if cur >= n:
                    cur = n - 1
                if cur > pad_bottom - SCROLL_OFFSET and cur < n - 1:
                    pad_top += 1
            elif cmd == curses.KEY_UP:
                draw_item(item_at(cur), pad, cur)
                cur -= 1
                if cur < 0:
                    cur = 0
                if cur < pad_top + SCROLL_OFFSET and cur > 0:
                    pad_top -= 1
            elif cmd == ord(' '):
                if item_at(cur).is_file():
                    selected[idx_file(cur)] = not selected[idx_file(cur)]
            elif cmd == ord('\n'):
                pathstack.append(item_at(cur))
                break
            elif cmd == curses.KEY_BACKSPACE and len(pathstack) > 1:
                pathstack.pop()
                break
            elif cmd == ord('c'):
                result = []
                for i, f in enumerate(files):
                    if selected[i]:
                        result.append(f)
                return result


if __name__ == "__main__":
    print(curses.wrapper(run))
