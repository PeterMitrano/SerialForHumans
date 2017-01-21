from asciimatics.exceptions import NextScene
from asciimatics.widgets import Layout, Button

from utils import MyFrame
from model import SettingsModel


class SettingsView(MyFrame):
    def __init__(self, screen, model):
        super(SettingsView, self).__init__(screen, model)

        layout = Layout([1, 1, 1, 1])
        self.add_layout(layout)
        layout.add_widget(Button("Close", self._close), 0)
        layout.add_widget(Button("Save", self._save), 1)
        self.fix()

    def _save(self):
        raise NextScene(name="Serial")

    @staticmethod
    def _close():
        raise NextScene(name="Serial")
