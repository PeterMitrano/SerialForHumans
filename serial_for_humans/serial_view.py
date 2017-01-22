import queue
from time import sleep

from asciimatics.exceptions import StopApplication, NextScene
from asciimatics.widgets import Layout, Divider, TextBox, Button

from .model import SettingsModel
from .utils import MyFrame, InputText


class SerialView(MyFrame):
    def __init__(self, screen, model, serial_thread, serial_out_queue):
        super(SerialView, self).__init__(screen, model)

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
        self.message_history = ""
        output_layout.add_widget(self.output_box)
        output_layout.add_widget(Divider())

        menu_layout = Layout([1, 1, 1, 1])
        self.add_layout(menu_layout)
        menu_layout.add_widget(Button("Clear", self._clear_output), 0)
        menu_layout.add_widget(Button("Settings", self._settings), 1)
        menu_layout.add_widget(Button("Help", self._help), 2)
        menu_layout.add_widget(Button("Quit", self._quit), 3)

        self.fix()

        self.serial_out_queue = serial_out_queue
        serial_thread._target = self.serial_worker
        serial_thread.start()

    def _writer(self, message):
        if self._model.data['send_cr']:
            message += '\r'
        if self._model.data['send_nl']:
            message += '\n'
        self.serial_out_queue.put(message)

    def serial_worker(self, serial, serial_output_queue):

        try:
            f = None
            while True:

                while not serial_output_queue.empty():
                    msg = serial_output_queue.get().encode()
                    serial.write(msg)

                if serial.in_waiting > 0:
                    waiting_data = serial.read(serial.in_waiting)
                    try:
                        waiting_data = str(waiting_data, encoding='utf-8')
                    except UnicodeDecodeError:
                        continue
                    self._put_output(waiting_data)

                    if self._model.data['log_to_file']:
                        if f is None:
                            f = open("serial.log", 'w')

                        f.write(waiting_data)
                        f.flush()
                    elif f:
                        f.close()

                    self.screen.force_update()

                sleep(0.005)  # reduce CPU usage
        except OSError:
            return

    def _clear_output(self):
        self._model.serial_output = [""]
        self.output_box.value = self._model.serial_output
        self.output_box.reset()

    def _put_output(self, message):
        if len(self.output_box.value) == 0:
            self._model.serial_output = [""]

        for idx, char in enumerate(message):

            self.message_history += char
            if char in SettingsModel.ctrl_chars.keys():
                if self._model.data['show_control_chars']:
                    self._model.serial_output[-1] += SettingsModel.ctrl_chars[char]
            else:
                self._model.serial_output[-1] += char

            split_str = self._model.data['splitting_string']
            latest_split_str_size_data = self.message_history[-len(split_str):]
            if latest_split_str_size_data == split_str:
                # actually create new line
                self._model.serial_output += [""]

        self.output_box.value = self._model.serial_output
        self.output_box.reset()

    @staticmethod
    def _quit():
        raise StopApplication("User pressed quit")

    @staticmethod
    def _settings():
        raise NextScene(name="Settings")

    @staticmethod
    def _help():
        raise NextScene(name="Help")