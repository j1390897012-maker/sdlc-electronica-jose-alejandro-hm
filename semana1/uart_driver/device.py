

class UartDevice:

    def __init__(self, config, parser):
        self.config = config
        self.parser = parser

    def receive(self, message):
        return self.parser.parse(message)