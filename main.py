import curses
import curses.ascii
import pathlib
import time
import urllib

from browser import Browser
from help import Help
from status import Status
from upload import create_uploader


class Main:
    def __init__(self, root, upload_path, download_path, encrypt):
        self.root = pathlib.Path(root)
        self.upload_url = urllib.parse.urlparse(upload_path)
        self.download_url = urllib.parse.urlparse(download_path)
        self.encrypt = encrypt

    def make_target(self, base, fn):
        return urllib.parse.urlunparse(
            (base[0], base[1], base[2] + '/' + fn, '', base[4], ''))

    def run(self, stdscr):
        if not stdscr:
            # for completion only
            stdscr = curses.newwin()
            raise ValueError

        curses.curs_set(False)

        stdscr.keypad(True)
        stdscr.clear()
        stdscr.refresh()

        h, w = stdscr.getmaxyx()

        browser = Browser(self.root, 0, 0, h - 1 - Status.STATUS_HEIGHT, w - 1)
        status = Status(h - Status.STATUS_HEIGHT, 0, h - 1, w - 1)
        results = []
        while True:
            browser.render()
            browser.refresh()

            status.render()
            status.refresh()

            while True:
                cmd = stdscr.getch()

                if cmd == curses.ascii.ESC or cmd == ord('q'):
                    return results
                elif cmd == curses.KEY_DOWN:
                    browser.do_down()
                    browser.refresh()
                elif cmd == curses.KEY_UP:
                    browser.do_up()
                    browser.refresh()
                elif cmd == curses.KEY_NPAGE:
                    browser.do_down(h - 1 - Status.STATUS_HEIGHT)
                    browser.refresh()
                elif cmd == curses.KEY_PPAGE:
                    browser.do_up(h - 1 - Status.STATUS_HEIGHT)
                    browser.refresh()
                elif cmd == ord(' '):
                    browser.do_select()
                    browser.refresh()
                elif cmd == ord('\n'):
                    browser.push()
                    break
                elif cmd == curses.KEY_BACKSPACE:
                    browser.pop()
                    break
                elif cmd == ord('c'):
                    files_upload = browser.get_selected()
                    if len(files_upload) > 0:
                        if self.encrypt:
                            fn = time.strftime('%Y-%m-%d_%H.%M.%S.bin')
                        else:
                            fn = time.strftime('%Y-%m-%d_%H.%M.%S.zip')

                        status.render(f'Uploading {fn}, be patient...')
                        status.refresh()

                        target = self.make_target(self.upload_url, fn)
                        download_target = self.make_target(self.download_url, fn)
                        with create_uploader(target, encrypt=self.encrypt) as ku:
                            uploader, key = ku
                            for f in files_upload:
                                uploader.write(f, f.name)

                        results.append((download_target, key))

                        status.render(f'Done uploading {fn}.')
                        status.refresh()
                    else:
                        status.render('Choose something to upload first!')
                        status.refresh()
                elif cmd == ord('h'):
                    help = Help(0, 0, h - 1, w - 1)
                    help.render()
                    help.refresh()
                    stdscr.getch()
                    break
