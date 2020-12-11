_A platform which give you info about the newest video on a channel._

![example](https://github.com/custom-components/sensor.youtube/raw/master/example.png)

## Example configuration.yaml

```yaml
sensor:
  platform: youtube
  channel_id: UCZ2Ku6wrhdYDHCaBzLaA3bw
  api_key: <YouTube Data API v3 key>
```

## Configuration variables
  
key | type | description  
:--- | :--- | :---  
**platform (Required)** | string | The platform name.
**channel_id (Required)** | string | The Channel ID of the Youtube channel.
**api_key (Required)** | string | YouTube Data API v3 key.