from asciimatics.exceptions import NextScene
from asciimatics.widgets import Layout, Button, ListBox, CheckBox, RadioButtons

from utils import MyFrame
from model import SettingsModel


class SettingsView(MyFrame):
    def __init__(self, screen, model):
        super(SettingsView, self).__init__(screen, model)

        self._temp_model = SettingsModel()
        self.settings_data = self._temp_model.get_as_data_dict()

        settings_layout = Layout([100], fill_frame=True)
        self.add_layout(settings_layout)
        # 'splitting_char'
        # 'show_control_chars'
        # 'send_nl'
        # 'send_cr'
        # 'log_to_file'

        settings_layout.add_widget(RadioButtons([("\\n", 0),
                                        ("\\r\\n", 1)],
                                       label="Split Line On:",
                                       name="splitting_char",
                                       on_change=self._on_change), 0)

        menu_layout = Layout([1, 1, 1, 1])
        self.add_layout(menu_layout)
        self._reset_button = Button("Reset", self._reset)
        menu_layout.add_widget(Button("Close", self._close), 0)
        menu_layout.add_widget(Button("Save", self._save), 1)
        menu_layout.add_widget(self._reset_button, 2)
        self.fix()

    def _on_change(self):
        changed = False
        self.save()
        for key, value in self.data.items():
            if key not in self.settings_data or self.settings_data[key] != value:
                changed = True
                break
        self._reset_button.disabled = not changed

    def _reset(self):
        self.reset()

    def reset(self):
        # Do standard reset to clear out form, then populate with new data.
        super(SettingsView, self).reset()
        self.data = self._model.get_as_data_dict()

    def _save(self):
        self.save()
        self._model.set_from_data_dict(self.data)
        raise NextScene(name="Serial")

    @staticmethod
    def _close():
        raise NextScene(name="Serial")
