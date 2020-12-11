"""
A platform which give you info about the newest video on a channel.

For more details about this component, please refer to the documentation at
https://github.com/custom-components/youtube
"""

import html
import json
import logging
import async_timeout
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.aiohttp_client import async_create_clientsession
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.helpers.entity import Entity

CONF_CHANNEL_ID = 'channel_id'
CONF_API_KEY = 'api_key'

ICON = 'mdi:youtube'

BASE_URL = 'https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=1&order=date&channelId={}&key={}'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_CHANNEL_ID): cv.string,
    vol.Required(CONF_API_KEY): cv.string,
})

_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(
        hass, config, async_add_entities, discovery_info=None):  # pylint: disable=unused-argument
    """Setup sensor platform."""
    channel_id = config['channel_id']
    api_key = config['api_key']
    session = async_create_clientsession(hass)
    try:
        url = BASE_URL.format(channel_id, api_key)
        async with async_timeout.timeout(10, loop=hass.loop):
            response = await session.get(url)
            info = await response.text()
        data = json.loads(info)
        name = data['items'][0]['snippet']['channelTitle']
    except Exception:  # pylint: disable=broad-except

        name = None

    if name is not None:
        async_add_entities([YoutubeSensor(channel_id, api_key, name, session)], True)

class YoutubeSensor(Entity):
    """YouTube Sensor class"""
    def __init__(self, channel_id, api_key, name, session):
        self._state = None
        self.session = session
        self._image = None
        self.live = False
        self._name = name
        self.channel_id = channel_id
        self.api_key = api_key
        self.url = None
        self.published = None

    async def async_update(self):
        """Update sensor."""
        _LOGGER.debug('%s - Running update', self._name)
        try:
            url = BASE_URL.format(self.channel_id, self.api_key)
            async with async_timeout.timeout(10, loop=self.hass.loop):
                response = await self.session.get(url)
                info = await response.text()
            data = json.loads(info)
            title = data['items'][0]['snippet']['title']
            url = 'https://www.youtube.com/watch?v=' + data['items'][0]['id']['videoId']
            try:
                async with async_timeout.timeout(10, loop=self.hass.loop):
                    response = await self.session.get(url + '&type=video&eventType=live')
                    live_info = await response.text()
                    live_data = json.loads(live_info)
                live_data = data['items'][0]['snippet']['liveBroadcastContent']
                if live_data == 'live':
                    self.live = True
                else:
                    _LOGGER.debug('%s - Skipping live check', self._name)
            except Exception as error:  # pylint: disable=broad-except
                _LOGGER.debug('%s - Skipping live check', self._name)
            self.url = url
            self.published = data['items'][0]['snippet']['publishTime']
            thumbnail_url = data['items'][0]['snippet']['thumbnails']['high']['url']
            self._state = title
            self._image = thumbnail_url
        except Exception as error:  # pylint: disable=broad-except
            _LOGGER.debug('%s - Could not update - %s', self._name, error)

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
    def icon(self):
        """Icon."""
        return ICON

    @property
    def device_state_attributes(self):
        """Attributes."""
        return {'url': self.url,
                'published': self.published,
                'live': self.live}
