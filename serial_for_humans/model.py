class SettingsModel(object):

    ctrl_chars = {'\n': '\\n',
                  '\r': '\\r',
                  '\t': '\\t',
                  }

    def __init__(self):
        self.serial_output = []
        self.data = {
            'splitting_string': '\r\n',
            'show_control_chars': True,
            'send_nl': True,
            'send_cr': True,
            'log_to_file': False,
        }

    def get_as_data_dict(self):
        return self.data

    def set_from_data_dict(self, data):
        self.data = data
