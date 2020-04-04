#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 12:56:26 2020

@author: isaaclera
"""

import libtorrent as lt
import time
import sys

ses = lt.session({'listen_interfaces': '0.0.0.0:6881'})

info = lt.torrent_info(sys.argv[1])
h = ses.add_torrent({'ti': info, 'save_path': '/media/HardDrive/'})
s = h.status()
#print('starting', )

while (not s.is_seeding):
    s = h.status()
    
    filelog = open('logs/estado.log', 'a+')
    filelog.write('\r%s %.2f%% complete (down: %.1f kB/s up: %.1f kB/s peers: %d) %s\n' % (
        s.name,s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000,
        s.num_peers, s.state))

    alerts = ses.pop_alerts()
    for a in alerts:
        if a.category() & lt.alert.category_t.error_notification:
            filelog.write("%s\t%s"%(s.name,a))

    filelog.close()
#    sys.stdout.flush()
    time.sleep(60)

filelog = open('logs/completados.log', 'a+')
filelog.write("Download: %s\n "%h.status().name)
filelog.close()

