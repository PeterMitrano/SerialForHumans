import unittest
from serial_for_humans.main import App


class MockSerial:

    def __init__(self):
        self.in_waiting = 0

    def read(self, num_bytes):
        pass

    def write(self, bytes):
        pass


class TestSerial(unittest.TestCase):

    def test_launch(self):
        mock_serial = MockSerial()
        app = App()
        app.run(mock_serial)
        self.fail()

if __name__ == '__main__':
    unittest.main()