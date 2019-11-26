import curses


class Help:
    def __init__(self, y0, x0, y1, x1):
        self.y0, self.x0 = y0, x0
        self.y1, self.x1 = y1, x1
        self.h = y1 - y0 + 1
        self.w = x1 - x0 + 1
        self.win = curses.newwin(self.h, self.w, self.y0, self.x0)

    def println(self, y, str):
        self.win.addnstr(y, 1, str, self.w - 2)  # border

    def render(self):
        self.win.border()
        self.println(1, 'how to use azmirror')
        self.println(2, 'press up/down/pgup/pgdown to move cursor')
        self.println(3, 'press space to select file')
        self.println(4, 'press c to upload')
        self.println(5, 'press q to quit')

    def refresh(self):
        self.win.refresh()
