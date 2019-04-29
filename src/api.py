import datetime
import hashlib
import json
import os
import urllib
from itertools import chain
import time

import grequests
import requests


class BaseApiEndpoint:
    API_ENDPOINT = os.environ.get('API_URL', 'https://gateway.marvel.com')
    PREFIX = 'v1/public'
    URL = ''

    def __init__(self, private_api_key, public_api_key):
        self.private_api_key = private_api_key
        self.public_api_key = public_api_key

    def _generate_auth_params(self):
        """
        Handle marvel api auth logic to generate:
        ts: timestampe
        apikey: public api key
        hash: hash(ts + public key + private key)
        """
        ts = int(time.time())
        m = hashlib.md5()
        m.update(
            str(
                str(ts) +
                self.private_api_key +
                self.public_api_key
            ).encode())
        hash = m.hexdigest()
        return {
            'ts': ts,
            'apikey': self.public_api_key,
            'hash': hash
        }

    def _get_url(self, *args, **kwargs):
        url_kwargs = self._generate_auth_params()
        url_kwargs.update(kwargs)
        url_param = '?' + urllib.parse.urlencode(url_kwargs, doseq=True)
        return ('/'.join([
            self.API_ENDPOINT,
            self.PREFIX,
            self.URL] +
            list(args)) +
            url_param)

    def _headers(self):
        return {
            'content-type': 'application/json',
            'accept': 'application/json',
        }

    def _get(self, url):
        print(f'GET: {url}')
        resp = requests.get(url, headers=self._headers())
        return self._validate_resp(resp)

    def _post(self, url, data=None):
        resp = requests.post(url, data=data, headers=self._headers())
        return self._validate_resp(resp)

    def _validate_resp(self, resp):
        assert resp.status_code == 200, f'Invalid response url:{resp.url} content: {resp.content}'
        return resp.json()

    def async_reseponses(self, reqs):
        resps = grequests.map(reqs)
        return [self._validate_resp(r) for r in resps]

    def get_batch(self, uids):
        reqs = []
        for uid in uids:
            url = self._get_url(uid)
            print(f'async GET: {url}')
            reqs.append(grequests.get(url, headers=self._headers()))
        return [resp['data'] for resp in self.async_reseponses(reqs)]

    def get(self, uid, **kwargs):
        url = self._get_url(uid, **kwargs)
        return self._get(url)['data']

    def find(self, *args, **kwargs):
        if 'limit' not in kwargs:
            kwargs['limit'] = 10
        url = self._get_url(*args, **kwargs)
        return self._get(url)['data']['results']


class Comic(BaseApiEndpoint):
    URL = 'comics'


class Character(BaseApiEndpoint):
    URL = 'characters'


class Creator(BaseApiEndpoint):
    URL = 'creators'


class Event(BaseApiEndpoint):
    URL = 'events'


class Series(BaseApiEndpoint):
    URL = 'series'


class Stories(BaseApiEndpoint):
    URL = 'stories'


class Api:
    def __init__(self):
        self._auth()
        keys = [self.private_key, self.pub_key]
        self.comic = Comic(*keys)
        self.character = Character(*keys)
        self.creator = Creator(*keys)
        self.event = Event(*keys)
        self.series = Series(*keys)
        self.story = Stories(*keys)

    def _auth(self):
        self.pub_key = os.environ['PUBLIC_KEY']
        self.private_key = os.environ['PRIVATE_KEY']
