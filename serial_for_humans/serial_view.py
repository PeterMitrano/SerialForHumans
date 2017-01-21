import queue
from time import sleep

import serial
from asciimatics.exceptions import StopApplication, NextScene
from asciimatics.widgets import Layout, Divider, TextBox, Button

from model import SettingsModel
from utils import MyFrame, InputText


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

    @staticmethod
    def _settings():
        raise NextScene(name="Settings")

    @staticmethod
    def _help():
        raise NextScene(name="Help")