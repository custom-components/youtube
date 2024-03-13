[![hacs_badge](https://img.shields.io/badge/HACS-Default-41BDF5.svg?style=for-the-badge)](https://github.com/hacs/integration)
# youtube

_A platform which give you info about the newest video on a channel._

**This uses web scraping, a better implementation will be to use the API.**

![example][exampleimg]

## __BREAKING CHANGE__

Video views and stars are now reported.  As a result any automations triggered by state will now be triggered when the number of views or stars changes.  To avoid this, add the url attribute to the trigger so that the automation is only triggered when the reported url changes ie:

``` yaml
trigger:
  - platform: state
    entity_id: sensor.franck_nijhof
    attribute: url
```

## Installation
### HACS
This repository supports installing through [HACS](https://hacs.xyz/).
### Manual
To get started put all the files from`/custom_components/youtube/` here:
`<config directory>/custom_components/youtube/`

## Example configuration.yaml

Using the old style channel id.

```yaml
sensor:
  platform: youtube
  channel_id: UCZ2Ku6wrhdYDHCaBzLaA3bw
```

Or using new style channel name (_Note: You need to enclose the channel name in quotes!_)

```yaml
sensor:
  platform: youtube
  channel_id: '@frenck'
```

## Configuration variables

key | type | description
:--- | :--- | :---
**platform (Required)** | string | The platform name.
**channel_id (Required)** | string | The Channel ID of the Youtube channel.

## State and Attributes

### State

* The name of the most recent video

### Attributes

* url: URL of the most recent video
* content_id: the content ID (useful for sending to certain media players)
* published: The time and date the video was published
* stars: The 'stars' recieved on youtube. (This is all reactions both 👍 and 👎 combined)
* views: the number of video views
* stream: If the video was streamed live
* stream_start: datetime of the start of a live stream
* live: If the video is live now
* channel_is_live: If any video on the channel is live
* channel_image: URL of the channel logo image

***

[exampleimg]: example.png
