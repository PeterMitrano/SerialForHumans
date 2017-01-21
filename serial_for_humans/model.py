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