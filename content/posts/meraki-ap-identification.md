---
title: "Meraki AP Identification"
date: 2021-10-31T15:40:16.056000+00:00
draft: false
description: "By default, Meraki does not advertise the AP (MR) name in beacons. This can be confusing doing a survey in a tool such as Ekahau and trying to find an AP in the seemingly random BSSID's used by the AP radios. If you need to determine the BSSID to AP ..."
slug: meraki-ap-identification
---

By default, Meraki does not advertise the AP (MR) name in beacons. This can be confusing doing a survey in a tool such as Ekahau and trying to find an AP in the seemingly random BSSID's used by the AP radios. If you need to determine the BSSID to AP mapping after the fact, you can use the Meraki API to pull that information. My colleague has such a PowerShell script available [here](https://github.com/huntsman95/Meraki_APNameBSSID) to make the job easier.

However, an easier solution is to enable AP name broadcast in beacons which will put names directly into your surveys. This feature is not available in the UI by default, you'll need to open a Meraki support case to enable AP Name Broadcast. It's enabled per SSID so make sure to include which SSID to change in the case notes. (Note: it's a good idea to check this doesn't violate any security policies before implementing!) Once enabled you'll see this in Ekahau:

![](https://interframe.space/wp-content/uploads/2021/04/name-in-ekahau.png)

This is done by adding a new tag named **Cisco CCX1 CKIP + Device Name** to beacon frames:

![](https://interframe.space/wp-content/uploads/2021/04/pcap-w-ccx-device-name.png)

In this example it added 32 bytes to the frame:

![](https://interframe.space/wp-content/uploads/2021/04/tag-frame-size-1024x217.png)

A couple last notes on this feature: it does reset the SSID so expect a minor disruption and Meraki support must be contacted each time to enable/disable.

References

-   [https://www.nickjvturner.com/ap-name-broadcast-support](https://www.nickjvturner.com/ap-name-broadcast-suppor)
-   [https://github.com/huntsman95/Meraki\_APNameBSSID](https://github.com/huntsman95/Meraki_APNameBSSID)
-   [https://documentation.meraki.com/MR/WiFi\_Basics\_and\_Best\_Practices/Calculating\_Cisco\_Meraki\_BSSID\_MAC\_Addresses](https://documentation.meraki.com/MR/WiFi_Basics_and_Best_Practices/Calculating_Cisco_Meraki_BSSID_MAC_Addresses)
