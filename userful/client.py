import logging
import os

import requests

USERFUL_HOST = os.environ.get('USERFUL_HOST', None)
USERFUL_USER = os.environ.get('USERFUL_USER', None)
USERFUL_PASS = os.environ.get('USERFUL_PASS', None)
USERFUL_PORT = os.environ.get('USERFUL_PORT', '9000')

logger = logging.getLogger(__name__)


class UserfulClient:

    # FIXME - Make a generic send_request method
    def __init__(
        self, host=USERFUL_HOST, user=USERFUL_USER, password=USERFUL_PASS,
        port=USERFUL_PORT
    ):
        '''
        :param host: Hostname or IP address of userful installation
        :param user: Username for Userful Authentication
        :param password: Password for Userful Authentication
        :param port: Port of Userful API (defaults to 9000)
        '''
        self.api_url = 'http://{0}:9000/api'.format(host)
        self.user = user
        self.password = password
        # FIXME - move this to a property instead of in init
        self.get_auth_cookie()

    def get_auth_cookie(self):
        '''
        Technically using a session should allow the auth cookie to work by
        default but for some reason it is not working. Thus we store the cookie
        as a property of the client, and pass it for each request
        '''
        res = requests.post(
            '{0}/session'.format(self.api_url),
            json={"user": self.user, 'password': self.password}
        )
        res.raise_for_status()
        self.cookie = {'JSESSIONID': res.json()['session']['value']}

    def get_sources(self, sourceName=None):
        '''
        Retrieve a list of sources. If `sourceName` is provided, only the
        source with that name will be returned
        '''
        params = {}
        if sourceName is not None:
            params = {'sourceName': sourceName}

        return requests.get(
            '{0}/sources'.format(self.api_url), params=params
        )

    def play_videolist_by_zone(
        self, video_list, zone, **kwargs
    ):
        '''
        :param video_list: `list` of `str` where each string is a full path
        to a file on the userful host machine
        :param zone: String of zone name
        :param queue: `bool` - If True, playlist will not begin until current
        media playback completes. Defaults to False
        :param repeat: `bool` - Whether to repeat the playlist, defaults to
        False
        :slideshowInterval: Really dont know what this does... defaults to 10
        '''
        kwargs['videolist'] = video_list
        res = requests.put(
            '{0}/zones/byname/{1}/playVideoList'.format(self.api_url, zone),
            json=kwargs,
            cookies=self.cookie
        )
        return res

    def switch_source_by_zone(self, zone, playlist_name):
        '''
        Switch the default source of a zone

        :param zone: `str` of zone name
        :param source: `str` of source name
        '''
        return requests.put(
            '{0}/zones/byname/{1}/switch'.format(self.api_url, zone),
            cookies=self.cookie,
            params={'destinationSourceName': playlist_name}
        )

    def play_by_zone(self, zone):
        '''
        Triggers a zone to start playing its assigned source

        :param zone: `str` of name of zone
        '''
        return requests.put(
            '{0}/zones/byname/{1}/play'.format(self.api_url, zone),
            cookies=self.cookie
        )