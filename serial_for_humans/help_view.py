from asciimatics.exceptions import NextScene
from asciimatics.widgets import Layout, Button, Divider, TextBox

from utils import MyFrame


class HelpView(MyFrame):

    data = {
        'Help': [
            "use Tab to navigate between buttons You may also use the mouse to click if you are a plebeian.",
            "Ctrl-C will also quit the application at any time.",
        ]
    }

    def __init__(self, screen, model):
        super(HelpView, self).__init__(screen, model, data=HelpView.data)

        self._model = model
        self.screen = screen

        divider_layout_1 = Layout([1])
        self.add_layout(divider_layout_1)
        divider_layout_1.add_widget(Divider())

        input_layout = Layout([1, 5, 1])
        self.add_layout(input_layout)
        self.help_box = TextBox(10, name='Help')
        self.help_box.disabled = True
        input_layout.add_widget(self.help_box, 1)
        input_layout.update_widgets()

        divider_layout_2 = Layout([1])
        self.add_layout(divider_layout_2)
        divider_layout_2.add_widget(Divider())

        menu_layout = Layout([1, 1, 1, 1])
        self.add_layout(menu_layout)
        menu_layout.add_widget(Button("Close", self._close), 2)

        self.fix()

    @staticmethod
    def _close():
        raise NextScene(name='Serial')
