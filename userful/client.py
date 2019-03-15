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

    def get_sources(self, name=None):
        '''
        Retrieve a list of sources. If `name` is provided, only the
        source with that name will be returned
        '''
        params = {}
        if name is not None:
            params = {'sourceName': name}

        return requests.get(
            '{0}/sources'.format(self.api_url), params=params,
            cookies=self.cookie
        )

    def create_source(self, name, source_type, params):
        '''
        Creates a new source.

        :param name: `str` of new source name
        :param source_type: Type of source, such as "Signage Player"
        :param params: `dict` of params required to create source. Please
        consult the official docs on this, as there are too many to document
        here. http://dev.userful.com/rest/#sources_post

        The ID of the new source can be found in the result JSON in the
        'sourceId' key at the top level.
        '''
        payload = {
            'sourceName': name,
            'sourceType': source_type,
        }
        payload['params'] = params

        return requests.post(
            '{0}/sources'.format(self.api_url),
            json=payload,
            cookies=self.cookie
        )

    def update_source(self, source_id, payload):
        '''
        Update an existing source.

        :param source_id: `str` of source of ID to update
        :param payload: `dict` of full payload. Because this call is not
        idempotent, you are expected to have already used `get_sources` to
        get the details of your source, replacing the properties that you
        wish to.

        The ID of the new source can be found in the result JSON in the
        'sourceId' key at the top level.
        '''
        return requests.put(
            '{0}/sources/{1}'.format(self.api_url, source_id),
            json=payload,
            cookies=self.cookie
        )

    def play_videolist_by_name(
        self, video_list, display_type, display_name, **kwargs
    ):
        '''
        :param video_list: `list` of `str` where each string is a full path
        to a file on the userful host machine
        :param display_type: String of display types. Can be "zones",
        or "mirrorgroups".
        :param display_name: String of the name of the associated display
        to play the video list. EG "control display"
        :param queue: `bool` - If True, playlist will not begin until current
        media playback completes. Defaults to False
        :param repeat: `bool` - Whether to repeat the playlist, defaults to
        False
        :slideshowInterval: Really dont know what this does... defaults to 10
        '''
        valid_display_types = ['zones', 'mirrorgroups']
        if display_type not in valid_display_types:
            raise ValueError(
                'Invalid display_type {0}, must be one of {1}'.format(
                    display_type, valid_display_types
                )
            )

        kwargs['videolist'] = video_list
        res = requests.put(
            '{0}/{1}/byname/{2}/playVideoList'.format(
                self.api_url, display_type, display_name
            ),
            json=kwargs,
            cookies=self.cookie
        )
        return res

    def play_videolist_by_id(
        self, video_list, display_type, display_id, **kwargs
    ):
        '''
        :param video_list: `list` of `str` where each string is a full path
        to a file on the userful host machine
        :param display_type: String of display types. Can be "display", "zones",
        or "mirrorgroups".
        :param display_id: String of the id of the display, mirrorgroup, or zone
        to play the video list. EG "control display"
        :param queue: `bool` - If True, playlist will not begin until current
        media playback completes. Defaults to False
        :param repeat: `bool` - Whether to repeat the playlist, defaults to
        False
        :slideshowInterval: Really dont know what this does... defaults to 10
        '''
        valid_display_types = ['displays', 'zones', 'mirrorgroups']
        if display_type not in valid_display_types:
            raise ValueError(
                'Invalid display_type {0}, must be one of {1}'.format(
                    display_type, valid_display_types
                )
            )
        valid_display_types = ['zones', 'mirrorgroups']
        if display_type not in valid_display_types:
            raise ValueError(
                'Invalid display_type {0}, must be one of {1}'.format(
                    display_type, valid_display_types
                )
            )
        kwargs['videolist'] = video_list
        res = requests.put(
            '{0}/{1}/{2}/playVideoList'.format(
                self.api_url, display_type, display_id
            ),
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
