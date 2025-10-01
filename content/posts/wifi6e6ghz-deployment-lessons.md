---
title: "WIFi6E/6Ghz Deployment Lessons"
date: 2023-02-23T20:36:02.859000+00:00
draft: false
description: "This post will list some of the lessons learned from a Meraki 9166 deployment (FW: 29.4.1) of a 6Ghz WLAN and using Ekahau Survey + iPad + Sidekick2 (FW: 1.0.82) to gather data and Ekahau AI Pro 11.1.3 for analysis. Keep in mind these are observation..."
tags:
  - 56c01f0bf7a8a564cd3cf436
  - 63f7ce325e428f179acd9e8c
slug: wifi6e6ghz-deployment-lessons
cover: "/static/images/hashnode/wifi6e6ghz-deployment-lessons/7ee45bf5-d668-4c62-bad5-361f6f3e4db5.png"
---

This post will list some of the lessons learned from a Meraki 9166 deployment (FW: 29.4.1) of a 6Ghz WLAN and using Ekahau Survey + iPad + Sidekick2 (FW: 1.0.82) to gather data and Ekahau AI Pro 11.1.3 for analysis. Keep in mind these are observations in Feb 2023 and many lessons may be moot or reversed as firmware/code matures.

### How does Meraki out-of-band discovery operate?

Reduced Neighboor Reports (RNR's) are the mandatory out-of-band discovery method if other 2.4 or 5Ghz SSID's exist on an AP. These are extra fields in beacon frames that direct clients on how to find 6Ghz SSID's and BSSID's while listening on 2.4 and 5Ghz. However, with a multiple BSSID/SSID configuration it wasn't clear if all SSID's or which SSID(s) would include RNR on a given AP. Below is my configuration with WPA2 and an Open SSID in the first 2 SSID "slots" of the Merkai SSID config. These have RNR's and the 3rd which is my dual 5 and 6Ghz WPA3 SSID does not. This leads me to think if the first 2 were disabled, the 3rd 6Ghz SSID would become un-discoverable for devices that rely on RNR's only.

![](images/posts/wifi6e6ghz-deployment-lessons/7ee45bf5-d668-4c62-bad5-361f6f3e4db5.png)

### How does Merkai Auto-Channel Work in 6Ghz?

Not really. Meraki auto-channel functionality put nearly all 6Ghz radios on channel 161 with a couple on 157. Not only is this poor channel planning but 161 isn't a Prefered Scanning Channel (PSC) so if in-band discovery was required clients would not find the SSID. Recommendation: manual channel planning and use PSC channels as primaries in a 40-80Mhz design. This is recommended by [David Coleman at WLPC Prague 2022](https://www.youtube.com/watch?v=HbpD4BRdNvI).

![](/images/posts/wifi6e6ghz-deployment-lessons/c942e4c1-f923-444f-865f-ece20cf8d01d.png)

### How well does Ekahau detect 6Ghz WLAN's?

Ekahau Sidekick 2 with 1.0.82 with Ekahau Survey (ie ipad version) can scan all 6Ghz channels. However, Ekahau AI Pro version 11.1.3 only doew PSC:

![](/images/posts/wifi6e6ghz-deployment-lessons/9b241f57-a52a-449e-a948-0f1075307936.png)

### How does the SK2 capture in 6Ghz?

Sidekick 2 with 1.0.82 firmware does not capture traffic.

![](/images/posts/wifi6e6ghz-deployment-lessons/12b65f3a-89f9-4a5b-bc3e-861ae1e6421c.png)

### Best way to confirm 6Ghz is working without a 6Ghz client?

If you are lacking a 6Ghz device to validate the next best method may be to use a Merkai wireless interface packet capture. With a wireless capture, you can see 6Ghz beacons and confirm RNR's are included for out-of-band discovery

![](/images/posts/wifi6e6ghz-deployment-lessons/c3ebb086-1d40-4000-bead-80beae53e9d2.png)

6Ghz beacons can also be observed:

![](/images/posts/wifi6e6ghz-deployment-lessons/18ca808b-5b6e-41c7-bc05-47d7cc147ab8.png)

### How to configure Meraki for a 6Ghz SSID?

Create WPA3 SSID, then add a WIFi6E AP to the network to enable 6Ghz settings, define in RF Profile which SSID's you want to operate in 6Ghz.

### Ekahau doesn't see your 6Ghz under My Networks.

Be careful with filtering, 6Ghz WLAN's do not seem to be bundled together under All My Networks when you are connected to a 5Ghz WLAN while surveying.

### Understand 6Ghz Power Spectrum Density

6Ghz data frames will be sent at a high power compared to beacons. Meaning in surveys 6Ghz networks will appears to have much lower RSSI then 5Ghz networks at the same power level. This was discussed at WPLC 2022 Prague [here](https://www.youtube.com/watch?v=HbpD4BRdNvI).

### Sidekick 1 vs Sidekick 2.

Sidekick 2 appears to 3 to 11db less sensitive than the SK1 per Jerry Olla. My first deployment seems to confirm this. This seems to be due to 1 less spatial stream and antenna design. Keep this in mind with offsets, you may be offsetting too much with "View as Mobile."

### What should be your 6Ghz SSID Strategy?

It's not an easy decision considering early client compatibility, discovery methods and the need for WPA3 in 6Ghz. Here is guidance from [Cisco TAC](https://blogs.cisco.com/networking/wlan-ssid-security-migration-into-6ghz-networks?utm_source=pocket_saves), [Extreme](https://www.extremenetworks.com/extreme-networks-blog/wireless-security-in-a-6-ghz-wi-fi-6e-world/?utm_source=pocket_saves) and [Aruba](https://blogs.arubanetworks.com/corporate/8-questions-to-ask-before-you-deploy-wi-fi-6e/). However, one thing to point out is that Meraki does not support a WPA2+WPA3 Enterprise Transition mode the way Mist does. This forces a separate WPA Enterprise SSID unless you know for sure all devices support WPA3.
