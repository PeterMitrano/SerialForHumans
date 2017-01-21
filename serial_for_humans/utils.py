from asciimatics.event import KeyboardEvent
from asciimatics.widgets import Frame, TextBox, Text


class MyTextBox(TextBox):

        def __init__(self, height, label=None, name=None, as_string=False,
                     on_change=None):
            super(TextBox, self).__init__(height, label, name, as_string, on_change)
            self.disabled = True


class MyFrame(Frame):

    def __init__(self, screen, model, data=None):
        super(MyFrame, self).__init__(screen, screen.height, screen.width, hover_focus=True,
                                      has_border=False, reduce_cpu=False, data=data)
        self._model = model
        self.screen = screen

        # Set up color scheme
        self.palette['background'] = (0, 0, 0)
        self.palette['borders'] = (7, 0, 0)
        self.palette['title'] = (7, 0, 0)
        self.palette['label'] = (2, 0, 0)
        self.palette['disabled'] = (7, 0, 0)
        self.palette['edit_text'] = (7, 0, 0)
        self.palette['focus_edit_text'] = (7, 0, 0)
        self.palette['button'] = (2, 0, 0)
        self.palette['focus_button'] = (2, 1, 0)
        self.palette['control'] = (7, 0, 0)
        self.palette['focus_control'] = (7, 0, 0)
        self.palette['selected_focus_control'] = (7, 0, 0)
        self.palette['field'] = (7, 0, 0)
        self.palette['focus_field'] = (7, 0, 0)
        self.palette['selected_field'] = (0, 0, 7)
        self.palette['selected_focus_field'] = (0, 0, 7)


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