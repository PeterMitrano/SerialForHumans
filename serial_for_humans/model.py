class SettingsModel(object):

    ctrl_chars = {'\n': '\\n',
                  '\r': '\\r',
                  '\t': '\\t',
                  }

    def __init__(self):
        self.data = {
            'splitting_char': '\n',
            'show_control_chars': False,
            'send_nl': True,
            'send_cr': False,
            'log_to_file': False,
        }

    def get_as_data_dict(self):
        return self.data

    def set_from_data_dict(self, data):
        self.data = data
