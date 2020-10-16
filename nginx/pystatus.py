#!/usr/bin/env python3
import datetime
import os
import requests
import sys
import time
from jinja2 import Environment, FileSystemLoader
from requests.packages import urllib3
from signal import signal, SIGINT, SIGTERM


class SiteChecks(object):
    def __init__(self, title, desc, url):
        self.title = title
        self.desc = desc
        self.url = url
        self.up = False
        self.r = None

    def __repr__(self):
        return 'Check: %s' % self.title


class SiteStatus(object):
    index_file = '/data/html/index.html'

    def __init__(self):
        self.conf = self.get_conf()
        self.checks = self.get_checks()
        self.updated = datetime.datetime

    def __repr__(self):
        return 'SiteStatus: %s' % len(self.checks)

    def update_status(self):
        self.run_checks()
        self.render_template()

    def run_checks(self):
        for c in self.checks:
            print('Processing:', c.url)
            try:
                c.r = requests.head(c.url, verify=False, timeout=5)
            except Exception as error:
                print('Error:', error)
                c.up = False
                continue
            c.up = True if c.r.ok else False
        self.updated = datetime.datetime.now()

    def render_template(self):
        print('Rendering template... ', end='')
        file_loader = FileSystemLoader('source')
        env = Environment(loader=file_loader)
        template = env.get_template('index.jinja2')
        meta = {'updated': self.updated}
        data = {'checks': self.checks, 'conf': self.conf, 'meta': meta}
        output = template.render(data)
        with open(self.index_file, 'w+') as f:
            f.write(output)
        print('Done.')

    @staticmethod
    def get_conf():
        return {
            'title': os.getenv('SITE_TITLE'),
            'desc': os.getenv('SITE_DESCRIPTION'),
            'author': os.getenv('SITE_AUTHOR'),
            'url': os.getenv('SITE_HOME_URL'),
            'favicon': os.getenv('SITE_FAVICON'),
            'logo': os.getenv('SITE_LOGO'),
        }

    @staticmethod
    def get_checks():
        envs = []
        for key in os.environ:
            envs.append(key)
        envs.sort()
        status = []
        for key in envs:
            if key.startswith('STATUS_'):
                status.append(os.getenv(key))
        checks = []
        for line in status:
            checks.append(SiteChecks(
                title=line.split('|')[0],
                desc=line.split('|')[1],
                url=line.split('|')[2],
            ))
        return checks


def sig_handler(signal_received, frame):
    print('Signal %s detected, exiting gracefully...' % signal_received)
    os.kill(1, signal_received)
    sys.exit(0)


if __name__ == '__main__':
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    signal(SIGINT, sig_handler)
    signal(SIGTERM, sig_handler)
    ss = SiteStatus()
    print('Initializing with %s checks.' % len(ss.checks))
    while True:
        ss.update_status()
        time.sleep(60)