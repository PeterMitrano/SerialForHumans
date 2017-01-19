import glob
from time import sleep
from curses import wrapper
import curses
import serial

def main(stdscr):
    # setup
    curses.noecho()
    curses.cbreak()
    curses.start_color()
    stdscr.keypad(True)

    # setup serial
    port = '/dev/ttyUSB0'
    baudrate = 115200

    with_serial = False

    if with_serial:
        ser = serial.Serial(port, baudrate)

    title_win = curses.newwin(3, curses.COLS - 1, 0, 0)
    input_win = curses.newwin(1, curses.COLS - 1, 3, 1)

    title = "Serial for HUMANS! Press q to quit."
    center_x = int((curses.COLS - 1) / 2 - len(title) / 2)
    title_win.addstr(1, center_x, title)
    title_win.refresh()

    input_win.addstr('input: ')

    msg = ''
    while True:
        key = input_win.getch()
        maxy, maxx = input_win.getmaxyx()
        y, x = input_win.getyx()

        if key == ord('q'):
            break
        elif key == curses.KEY_ENTER:
            # send over serial
            if with_serial:
                ser.write(msg)
            msg = ''
            input_win.clear()
            input_win.refresh()
        elif key == 127:

            input_win.delch(y, x - 1)
            input_win.refresh()
        elif 31 < key < 127:
            # stop at end of window
            if x == maxx - 1:
                continue

            c = chr(key)
            input_win.addstr(c)
            input_win.refresh()

            msg += c



    # teardown
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()


if __name__ == '__main__':
    wrapper(main)
