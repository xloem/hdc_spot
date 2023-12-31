#!/usr/bin/env python3
import os
import datalad.support.annexrepo, google_play_scraper, requests, tqdm

requests = requests.Session()

import ssl, urllib
try:
    VERS=[google_play_scraper.app('com.hivemapper.companion')['version'], 'testing']
except urllib.error.URLError as e:
    # please send this section to a therapist?
    if isinstance(e.reason, ssl.SSLCertVerificationError):
        print('Author of this software was victim of mind control and unsure how to handle this error:')
        print(e.reason)
        print('This may be an indication of somebody falsifying your network communications in a very dangerous way.')
        print('It could also simply be a bug. Have an expert verify by reviewing the dependency and using certificate transparency.')
            # we expressed a more rational thing and are impressive
            # review processes showed that we may have experienced [...]
            # [...] [development of strong cognitive behaviors roleplaying specific roles internally]
            # [via some influence like facebook channel]
            # [... [maybe? same old thing?]] [but that this leaves us with um the need to do tihngs that make sense,
            #  which only survives in small parts of mind. this is related to karl's personal why-so-slow.]
                # psychotic slowness could be from coping strategies for engaging misbehaving cognitive parts
                # many parts acting out strong stories, hard to orchestrate rational habits [with them].
        whatdoido = ssl._create_default_https_context
        ssl._create_default_https_context = ssl._create_unverified_context
        VERS=[google_play_scraper.app('com.hivemapper.companion')['version'], 'testing']
        ssl._create_default_https_context = whatdoido
    else:
        raise

devicekeys = {
    'hdc': 'minFirmwareURL',
    'hdc-s': 'minFirmwareURLHdcS',
}
repo = datalad.support.annexrepo.AnnexRepo('..')
jsons = {
    f'{platform}-{VER}':
        requests.get(f'https://hivemapper.com:8443/defaultflags?platform={platform}&app_version={VER}')
            .json()['flags']
    for platform in ['Android','iOS']
    for VER in VERS
}
urls = set([json[urlkey] for json in jsons.values() for urlkey in devicekeys.values()])
for url in urls:
    print('Considering', url)
    _, fn = url.rsplit('/',1)
    response = requests.get(url, stream=True)
    #with open(fn, 'wb') as f, tqdm.tqdm(total=int(response.headers['Content-Length']),desc=fn,unit='B',unit_scale=True,unit_divisor=1024) as pbar:
    #    for chunk in response.iter_content(chunk_size=1024*1024*4):
    #        f.write(chunk)
    #        pbar.update(len(chunk))
    #repo.add([fn])
    repo.add_url_to_file(os.path.abspath(fn), url, unlink_existing=True)
    added = set()
    for platform, json in jsons.items():
        platform, VER = platform.rsplit('-',1)
        for device, urlkey in devicekeys.items():
            if json[urlkey] == url:
                sn = f'{VER}-min-{platform}-{device}'
                print('applies to', sn, f'({fn})')
                if os.path.exists(sn):
                    os.unlink(sn)
                os.symlink(fn, sn)
                added.add(os.path.abspath(sn))
    repo.add(list(added), git=True)
repo.sync()
