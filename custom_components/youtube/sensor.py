"""
A platform which give you info about the newest video on a channel.

For more details about this component, please refer to the documentation at
https://github.com/custom-components/youtube
"""

import logging
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.aiohttp_client import async_create_clientsession
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.helpers.entity import Entity
from dateutil.parser import parse
import re
import html

CONF_CHANNEL_ID = 'channel_id'
ICON = 'mdi:youtube'
CHANNEL_URL = "https://www.youtube.com/{}"
RSS_URL = 'https://www.youtube.com/feeds/videos.xml?channel_id={}'
CHANNEL_LIVE_URL = 'https://www.youtube.com/channel/{}'
COOKIES = {"SOCS": "CAESEwgDEgk0ODE3Nzk3MjQaAmVuIAEaBgiA_LyaBg"}

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_CHANNEL_ID): cv.string,
})

_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(
        hass, config, async_add_entities, discovery_info=None):  # pylint: disable=unused-argument
    """Setup sensor platform."""
    channel_id = config['channel_id']
    _LOGGER.debug(f'Setting up {channel_id}')
    session = async_create_clientsession(hass)
    if channel_id.startswith('@'):
        channel_id = await get_channel_id(session, channel_id)
    try:
        url = RSS_URL.format(channel_id)
        response = await session.get(url)
        info = await response.text()
        name = info.split('<title>')[1].split('</')[0]
    except Exception as error:  # pylint: disable=broad-except
        _LOGGER.error(f'Unable to set up {channel_id} - {error}')
        name = None

    if name is not None:
        sensor = YoutubeSensor(channel_id, name, session)
        async_add_entities([sensor], True)


async def get_channel_id(session, user_name):
    channel_id = None
    url = CHANNEL_URL.format(user_name)
    _LOGGER.debug("Trying %s", url)
    try:
        response = await session.get(url, cookies=COOKIES)
        html = await response.text()
        regex = r"<link rel=\"alternate\" type=\"application/rss\+xml\" title=\"RSS\" href=\"(.*?)\">"
        found = re.findall(regex, html, re.MULTILINE)
        if found:
            strings = found[0].split("=")
            channel_id = strings[1]
    except Exception as error:  # pylint: disable=broad-except
        _LOGGER.debug(f'{user_name} - get_channel_id(): Error {error}')

    _LOGGER.debug("Channel id for name %s: %s", user_name, channel_id)
    return channel_id


class YoutubeSensor(Entity):
    """YouTube Sensor class"""

    def __init__(self, channel_id, name, session):
        self._state = None
        self.session = session
        self._image = None
        self.stars = 0
        self.views = 0
        self.stream = False
        self.live = False
        self._name = name
        self.channel_id = channel_id
        self.url = None
        self.content_id = None
        self.published = None
        self.channel_live = False
        self.channel_image = None
        self.expiry = parse('01 Jan 1900 00:00:00 UTC')
        self.stream_start = None

    async def async_update(self):
        """Update sensor."""
        _LOGGER.debug(f'{self._name} - Running update')
        try:
            url = RSS_URL.format(self.channel_id)
            response = await self.session.get(url)
            info = await response.text()
            exp = parse(response.headers['Expires'])
            if exp < self.expiry:
                return
            self.expiry = exp
            title = info.split('<title>')[2].split('</')[0]
            url = info.split('<link rel="alternate" href="')[2].split('"/>')[0]
            if self.live or url != self.url:
                self.stream, self.live, self.stream_start = await self.is_live(url)
            else:
                _LOGGER.debug(f'{self._name} - Skipping live check')
            self.url = url
            self.content_id = url.split('?v=')[1]
            self.published = info.split('<published>')[2].split('</')[0]
            thumbnail_url = info.split(
                '<media:thumbnail url="')[1].split('"')[0]
            self._state = html.unescape(title)
            self._image = thumbnail_url
            self.stars = info.split('<media:starRating count="')[1].split('"')[0]
            self.views = info.split('<media:statistics views="')[1].split('"')[0]

            self.channel_live, self.channel_image = await self.is_channel_live()
        except Exception as error:  # pylint: disable=broad-except
            _LOGGER.debug(f'{self._name} - Could not update - {error}')

    @property
    def name(self):
        """Name."""
        return self._name

    @property
    def entity_picture(self):
        """Picture."""
        return self._image

    @property
    def state(self):
        """State."""
        return self._state

    @property
    def unique_id(self):
        """Return unique ID for this sensor."""
        return self.channel_id

    @property
    def icon(self):
        """Icon."""
        return ICON

    @property
    def extra_state_attributes(self):
        """Attributes."""
        return {'url': self.url,
                'content_id': self.content_id,
                'published': self.published,
                'stars': self.stars,
                'views': self.views,
                'stream': self.stream,
                'stream_start': self.stream_start,
                'live': self.live,
                'channel_is_live': self.channel_live,
                'channel_image': self.channel_image}

    async def is_live(self, url):
        """Return bool if video is stream and bool if video is live"""
        live = False
        stream = False
        start = None
        try:
            response = await self.session.get(url)
            html = await response.text()
            if 'isLiveBroadcast' in html:
                stream = True
                start = parse(html.split('startDate" content="')[1].split('"')[0])
                if 'endDate' not in html:
                    live = True
                    _LOGGER.debug(f'{self._name} - Latest Video is live')
        except Exception as error:  # pylint: disable=broad-except
            _LOGGER.debug(f'{self._name} - is_live(): Error {error}')
        return stream, live, start

    async def is_channel_live(self):
        """Return bool if channel is live"""
        live = False
        channel_image = None
        url = CHANNEL_LIVE_URL.format(self.channel_id)
        try:
            _LOGGER.debug("GET %s: %s", self._name, url)
            response = await self.session.get(url, cookies=COOKIES)
            html = await response.text()
            if '{"iconType":"LIVE"}' in html:
                live = True
                _LOGGER.debug(f'{self._name} - Channel is live')
            regex = r"\"width\":48,\"height\":48},{\"url\":\"(.*?)\",\"width\":88,\"height\":88},{\"url\":"
            found = re.findall(regex, html, re.MULTILINE)
            if found:
                channel_image = found[0]
                channel_image = channel_image.replace("=s88-c-k-c0x00ffffff-no-rj", "")
        except Exception as error:  # pylint: disable=broad-except
            _LOGGER.debug(f'{self._name} - is_channel_live(): Error {error}')
        return live, channel_image
