#!/usr/bin/python3.5

import queue
import sys
import threading

from asciimatics.exceptions import ResizeScreenError
from asciimatics.scene import Scene
from asciimatics.screen import Screen

from model import SettingsModel
from help_view import HelpView
from serial_view import SerialView
from settings_view import SettingsView


def demo(screen, scene, model, serial_thread, serial_out_queue):
    scenes = [
        Scene([SerialView(screen, model, serial_thread, serial_out_queue)], -1, name="Serial"),
        Scene([SettingsView(screen, model)], -1, name="Settings"),
        Scene([HelpView(screen, model)], -1, name="Help"),
    ]

    screen.play(scenes, stop_on_resize=True, start_scene=scene)


class App:

    def __init__(self):
        self.model = SettingsModel()

    def run(self, port, baudrate):
        # don't assign target yet!

        last_scene = None
        serial_out_q = queue.Queue()
        while True:
            try:
                serial_thread = threading.Thread(target=None, args=(port, baudrate, serial_out_q), daemon=True)
                Screen.wrapper(demo, catch_interrupt=False,
                               arguments=[last_scene, self.model, serial_thread, serial_out_q])
                sys.exit(0)
            except KeyboardInterrupt:
                break
            except ResizeScreenError as e:
                last_scene = e.scene

if __name__ == "__main__":
    if '--debug' in sys.argv:
        import time; time.sleep(10)

    if len(sys.argv) < 3:
        print("Usage: python main.py port_path baudrate")
        print()
        print("EX: python main.py /dev/ttyUSB0 9600")
    else:
        g_port = sys.argv[1]
        g_baudrate = int(sys.argv[2])

        app = App()
        app.run(g_port, g_baudrate)
