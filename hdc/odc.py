import requests

class Client:
    def __init__(self, url='http://192.168.0.10:5000/', session=None):
        self.url =url
        self.session = session or requests.Session()
        self.ota = self._OTA(self)
        self.upload =  self._Upload(self)
    def init(self):
        return self._get('init')
    def info(self):
        return self._get('info')
    def ping(self):
        return self._get('ping')
    def locktime(self):
        return self._get('locktime')
    def time(self):
        return self._get('time')
    def cron(self, config = []):
        return self._post('cron', config=config)
    def log(self):
        return self._get('log')['log']
    def log_delete(self):
        return self._del('log')
    def cmd(self, cmd):
        return self._post('cmd', cmd=cmd)
    def cmd_sync(self, cmd = ''):
        return self._post('cmd/sync', cmd=cmd)

    def _get(self, path, **params):
        return self.session.get(self.url+path, params=params).json()
    def _post(self, path, **json):
        return self.session.post(self.url+path,json=json).json()
    def _upload(self, path, **files):
        return self.session.post(self.url+path,json=json).json()
    def _del(self, path):
        return self.session.delete(self.url+path).json()

    class _OTA(Client):
        def __init__(self, client):
            super().__init__(client.url, client.session)
        def __call__(self, filename):
            return self._get('ota', filename=filename)
        def start(self):
            return self._get('ota/start')
        def finish(self):
            return self._get('ota/finish')
    
    class _Upload:
        def __init__(self, client):
            super().__init__(client.url, client.session)
        def __init__(self, client):
            self._ = client
        def __call__(self, filename):
            with os.open(filename) as file:
                return self._upload('upload', filename=file)
