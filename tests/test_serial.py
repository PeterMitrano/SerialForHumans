import unittest
from serial_for_humans.main import App


class MockSerial:

    def __init__(self, port, baudrate):
        self.in_waiting = 0

    def read(self, num_bytes):
        pass

    def write(self, bytes):
        pass

    def close(self):
        pass


class TestSerial(unittest.TestCase):

    def test_launch(self):
        app = App()
        port = 'fake_port'
        baudrate = '-1'
        app.run(MockSerial, port, baudrate)
        self.fail()

if __name__ == '__main__':
    unittest.main()