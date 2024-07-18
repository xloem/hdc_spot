class Client:
    def __init__(self, client):
        self._ = client
    def __call__(self):
    def start(self):
        return self._._getjson('start')
    def finish(self):
        return self._._getjson('finish')
