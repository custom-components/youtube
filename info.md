_A platform which give you info about the newest video on a channel._

**This uses web scraping!**

![example](https://github.com/custom-components/sensor.youtube/raw/master/example.png)

## Example configuration.yaml

```yaml
sensor:
  platform: youtube
  channel_id: UCZ2Ku6wrhdYDHCaBzLaA3bw
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
* published: The time and date the video was published
* stream: If the video was streamed live
* live: If the video is live now
