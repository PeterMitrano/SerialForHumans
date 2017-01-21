#!/usr/bin/python3.5

from asciimatics.widgets import Frame, Layout, Divider, Text, TextBox, Button
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError, NextScene, StopApplication
from asciimatics.event import KeyboardEvent
import sys
import serial
import threading
from time import sleep
import queue


class SettingsModel(object):

    ctrl_chars = {'\n': '\\n',
                  '\r': '\\r',
                  '\t': '\\t',
                  }

    def __init__(self):
        self.splitting_char = '\n'
        self.show_control_chars = False
        self.send_nl = True
        self.send_cr = False
        self.log_to_file = False


class SettingsView(Frame):
    def __init__(self, screen, model):
        super(SettingsView, self).__init__(screen,
                                           screen.height * 2 // 3,
                                           screen.width * 2 // 3,
                                           hover_focus=True,
                                           title="Settings")
        # Save off the model that accesses the contacts database.
        self._model = model

        layout = Layout([1, 1, 1, 1])
        self.add_layout(layout)
        layout.add_widget(Button("Quit", self._quit), 3)
        self.fix()

    @staticmethod
    def _quit():
        raise NextScene(name="Main")


class InputText(Text):

    KEY_ENTER = 10

    def __init__(self, writer, label=None, name=None, on_change=None):
        super(InputText, self).__init__(label, name, on_change)
        self.writer = writer

    def process_event(self, event):
        if isinstance(event, KeyboardEvent):
            if event.key_code == InputText.KEY_ENTER:
                message_to_write = self.value
                self.value = ""
                self.reset()
                self.writer(message_to_write)
            else:
                return super().process_event(event)
        else:
            return super().process_event(event)


class ContactView(Frame):
    def __init__(self, screen, model, serial_thread, serial_out_queue):
        super(ContactView, self).__init__(screen,
                                          screen.height,
                                          screen.width,
                                          hover_focus=True,
                                          title="Serial For Humans",
                                          reduce_cpu=False)
        # Save off the model that accesses the contacts database.
        self._model = model
        self.screen = screen

        h, w = self.screen.dimensions
        self.output_rows = h - 5
        input_layout = Layout([1])
        self.add_layout(input_layout)
        input_layout.add_widget(InputText(self._writer, "Input:  ", "input"))
        input_layout.add_widget(Divider())

        output_layout = Layout([1])
        self.add_layout(output_layout)
        self.output_box = TextBox(self.output_rows, "Output: ", "output")
        self.output_box.disabled = True
        output_layout.add_widget(self.output_box)

        menu_layout = Layout([1, 1, 1, 1])
        self.add_layout(menu_layout)
        menu_layout.add_widget(Button("Clear", self._clear_output), 0)
        menu_layout.add_widget(Button("Settings", self._settings), 1)
        menu_layout.add_widget(Button("Quit", self._quit), 3)

        self.palette['disabled'] = (7, 0, 0)
        self.palette['edit_text'] = (7, 0, 0)
        self.palette['focus_edit_text'] = (7, 0, 0)

        self.fix()

        self.serial_out_queue = serial_out_queue
        serial_thread._target = self.serial_worker
        serial_thread.start()

    def _writer(self, message):
        if self._model.send_cr:
            message += '\r'
        if self._model.send_nl:
            message += '\n'
        self.serial_out_queue.put(message)

    def serial_worker(self, port, baudrate, serial_output_queue : queue.Queue):
        ser = serial.Serial(port, baudrate, timeout=0)

        if self._model.log_to_file:
            f = open("serial.log", 'w')
        while True:

            while not serial_output_queue.empty():
                msg = serial_output_queue.get().encode()
                ser.write(msg)

            if ser.in_waiting > 0:
                waiting_data = ser.read(ser.in_waiting)
                waiting_data = str(waiting_data, encoding='utf-8')
                self._put_output(waiting_data)

                if self._model.log_to_file:
                    f.write(waiting_data)
                    f.flush()

                self.screen.force_update()

            sleep(0)  # yield to thread scheduler

    @staticmethod
    def _settings():
        raise NextScene(name="Settings")

    def _clear_output(self):
        self.output_box.value = None

    def _put_output(self, message):
        if len(self.output_box.value) == 0:
            self.output_box.value = [""]

        for char in message:
            if char in SettingsModel.ctrl_chars.keys():
                if self._model.show_control_chars:
                    self.output_box.value[-1] += SettingsModel.ctrl_chars[char]
                if char == self._model.splitting_char:
                    # actually create new line in output box
                    self.output_box.value += [""]
            else:
                self.output_box.value[-1] += char
        self.output_box.reset()

    @staticmethod
    def _quit():
        raise StopApplication("User pressed quit")


def demo(screen, scene, model, serial_thread, serial_out_queue):
    scenes = [
        Scene([ContactView(screen, model, serial_thread, serial_out_queue)], -1, name="Main"),
        Scene([SettingsView(screen, model)], -1, name="Settings"),
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
    if len(sys.argv) != 3:
        print("Usage: python main.py port_path baudrate")
        print()
        print("EX: python main.py /dev/ttyUSB0 9600")
    else:
        g_port = sys.argv[1]
        g_baudrate = int(sys.argv[2])

        app = App()
        app.run(g_port, g_baudrate)
