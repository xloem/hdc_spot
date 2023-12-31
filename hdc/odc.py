import requests

class Client:
    def __init__(self, host='192.168.0.10', port=5000, ssl=False):
        self.url = f'{ssl and "https" or "http"}://{host}:{port}/'
        self.session = requests.Session()
        getjson = self._AttrRequests(self, 'GET', 'json')
        self._getjson = getjson

    def init(self):
        return self._getjson('init')
    def info(self):
        return self._getjson('info')
    def ping(self):
        return self._getjson('ping')
    def locktime(self):
        return self._getjson('locktime')
    def time(self):
        return self._getjson('time')
    def cron(self, config = []):
        return self._postjson('cron', config=config)
    def log(self):
        return self._getjson('log')['log']
    def log_delete(self):
        return self._deljson('log')
    def cmd(self, cmd):
        return self._postjson('cmd', cmd=cmd)
    def cmd_sync(self, cmd = ''):
        return self._postjson('cmd/sync', cmd=cmd)

    def _getjson(self, path):
        return self.session.get(self.url+path).json()
    def _postjson(self, path, **json):
        return self.session.post(self.url+path,json=json).json()
    def _deljson(self, path):
        return self.session.delete(self.url+path).json()
