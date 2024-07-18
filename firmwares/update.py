#!/usr/bin/env python3
import json, os, urllib.request
import datalad.support.annexrepo, google_play_scraper, tqdm

devicekeys = {
    'hdc': 'minFirmwareURL',
    'hdc-s': 'minFirmwareURLHdcS',
}
try:
    VERS=[google_play_scraper.app('com.hivemapper.companion')['version'], 'testing']
except urllib.error.URLError as e:
    import ssl
    if isinstance(e.reason, ssl.SSLCertVerificationError):
        import certifi
        os.environ['SSL_CERT_FILE'] = certifi.where()
        VERS=[google_play_scraper.app('com.hivemapper.companion')['version'], 'testing']

repo = datalad.support.annexrepo.AnnexRepo('..')
jsons = {
    f'{platform}-{VER}':
        json.load(urllib.request.urlopen(urllib.request.Request(
            f'https://hivemapper.com:8443/defaultflags?platform={platform}&app_version={VER}',
            headers={'User-Agent':'hdc_spot'},
        )))['flags']
    for platform in ['Android','iOS']
    for VER in VERS
}
urls = set([json[urlkey] for json in jsons.values() for urlkey in devicekeys.values()])
for url in urls:
    print('Considering', url)
    _, fn = url.rsplit('/',1)
    repo.add_url_to_file(os.path.abspath(fn), url, unlink_existing=True)
    added = set()
    for platform, json in jsons.items():
        platform, VER = platform.rsplit('-',1)
        for device, urlkey in devicekeys.items():
            if json[urlkey] == url:
                sn = f'{VER}-min-{platform}-{device}'
                print('applies to', sn, f'({fn})')
                if os.path.lexists(sn):
                    os.unlink(sn)
                os.symlink(fn, sn)
                added.add(os.path.abspath(sn))
    repo.add(list(added), git=True)
repo.sync()
