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

    def render(self):
        self.win.hline(0, 0, curses.ACS_HLINE, self.w)
        self.win.addnstr(1, 0, 'Ready.', self.w)

    def refresh(self):
        self.win.refresh()
