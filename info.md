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
