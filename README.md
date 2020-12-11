# youtube

[![BuyMeCoffee][buymecoffeebedge]][buymecoffee]

_A platform which give you info about the newest video on a channel._

![example][exampleimg]

## Installation

To get started put all the files from`/custom_components/youtube/` here:
`<config directory>/custom_components/youtube/`

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

***

[exampleimg]: example.png
[buymecoffee]: https://www.buymeacoffee.com/ludeeus
[buymecoffeebedge]: https://camo.githubusercontent.com/cd005dca0ef55d7725912ec03a936d3a7c8de5b5/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f6275792532306d6525323061253230636f666665652d646f6e6174652d79656c6c6f772e737667
