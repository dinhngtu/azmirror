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
