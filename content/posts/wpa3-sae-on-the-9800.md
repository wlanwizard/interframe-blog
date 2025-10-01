---
title: "WPA3 SAE on the 9800"
date: 2021-10-31T15:40:15.993000+00:00
draft: false
description: "This post will show how to configure and verify operation of WPA3 - Simultaneous Authentication of Equals (SAE) on a 9115 EWC 9800. WPA3-SAE is the replacement for WPA2-PSK that thwarts offline attacks.
Details of setup:

Cisco 9115 AP running 9800 E..."
slug: wpa3-sae-on-the-9800
---

This post will show how to configure and verify operation of WPA3 - Simultaneous Authentication of Equals (SAE) on a 9115 EWC 9800. WPA3-SAE is the replacement for WPA2-PSK that thwarts offline attacks.

Details of setup:

-   Cisco 9115 AP running 9800 Embedded Wireless Controller: 16.12.03
-   Windows 10 with Killer Wi-Fi 6 AX1650 (Intel AX-200) client, driver version 21.10.1.2

WLAN Configuration:

```
wlan interframe.wpa3 3 interframe.wpa3
 radio dot11a
 no security ft adaptive
 no security wpa wpa2
 security wpa psk set-key ascii 0 secret123
 no security wpa akm dot1x
 security wpa akm sae
 security wpa wpa3
 security pmf mandatory
 no shutdown
```

![](https://interframe.space/wp-content/uploads/2020/05/wlan-gui.png)

View from GUI

A reminder with the 9800 config model, always ensure the WLAN is associated to a Policy Tag that connects your WLAN Profile with a Policy Profile:

![](https://interframe.space/wp-content/uploads/2020/05/edit-policy-tag.png)

Let's take a look at our new WPA3 WLAN from Bettercap:

![](https://interframe.space/wp-content/uploads/2020/05/bettercap-show-wifi-1.png)

Bettercap (from the [wlanpi](https://www.wlanpi.com/))

Fail! So we have a problem, either Bettercap doesn't recognize WPA3 or we have a mis-configuration and we're really using WPA2. Let's confirm by looking in a beacon from a pcap:

![](https://interframe.space/wp-content/uploads/2020/05/beacon_border-1.png)

Here you can see under RSN Information the use of AES cipher suite and SAE/SHA265 for Authenticated Key Management. Frame Protection is also required. Let's see it in action. First connect via the built-in Windows 10 connection manager:

![](https://interframe.space/wp-content/uploads/2020/05/win10-connect.png)

![](https://interframe.space/wp-content/uploads/2020/05/probe-req-1.png)

Probe Request

![](https://interframe.space/wp-content/uploads/2020/05/probe-response-1.png)

Probe Response

![](https://interframe.space/wp-content/uploads/2020/05/seq-1-commit1.png)

SAE Commit - Client to AP

![](https://interframe.space/wp-content/uploads/2020/05/ap-to-client-seq1-commit-1.png)

SAE Commit - AP to Client

![](https://interframe.space/wp-content/uploads/2020/05/confirm1.png)

SAE Confirm - Client to AP

![](https://interframe.space/wp-content/uploads/2020/05/confirm2.png)

SAE Confirm - AP to Client

![](https://interframe.space/wp-content/uploads/2020/05/assoc-req.png)

Association Request

![](https://interframe.space/wp-content/uploads/2020/05/assoc-response.png)

Association Response

![](https://interframe.space/wp-content/uploads/2020/05/4-way.png)

And finally, the 4-way handshake

Another good way to analyze the connection process is with the 9800 trace logs accessed via the Troubleshooting menu, then Radioactive Trace:

![](https://interframe.space/wp-content/uploads/2020/05/radioactive.png)

Add the client MAC address:

![](https://interframe.space/wp-content/uploads/2020/05/radioactive-9800-1.png)

Add MAC then hit Start

![](https://interframe.space/wp-content/uploads/2020/05/radioactive-results-1.png)

Stop, select Generate then open the text file

Below is an abbreviated version of the trace log. It begins with association, the unique SAE Commit/Confirm frames are not represented in the logs.

```
MAC: 3800.2511.1111  Association received. BSSID 2c4f.5276.0bce
MAC: 3800.2511.1111  Received Dot11 association request
MAC: 3800.2511.1111  dot11 send association response
MAC: 3800.2511.1111  Association success. AID 1
MAC: 3800.2511.1111  DOT11 state transition: S_DOT11_INIT -> S_DOT11_ASSOCIATED
MAC: 3800.2511.1111  L2 Authentication initiated. method PSK
MAC: 3800.2511.1111  Client auth-interface state transition: S_AUTHIF_AWAIT_PSK_AUTH_START_RESP -> S_AUTHIF_PSK_AUTH_PENDING
Authentication Success. Resolved Policy bitmap:11 for client 3800.2511.1111 
MAC: 3800.2511.1111  Client auth-interface state transition: S_AUTHIF_ADD_MOBILE_ACK_WAIT_KM -> S_AUTHIF_PSK_AUTH_KEY_XCHNG_PENDING
MAC: 3800.2511.1111  EAP key M1 Sent successfully
MAC: 3800.2511.1111   M2 Status: EAP key M2 validation success
MAC: 3800.2511.1111  EAP key M3 Sent successfully
MAC: 3800.2511.1111  M4 Status: EAP key M4 validation is successful
MAC: 3800.2511.1111  EAP Key management successful. AKM:SAE Cipher:CCMP WPA2
MAC: 3800.2511.1111  Client key-mgmt state transition: S_PTKINITNEGOTIATING -> S_PTKINITDONE
Managed client RUN state notification: 3800.2511.1111
Client IP learn method update successful. Method: DHCP IP: 192.168.62.76
```

More info:

-   [Cisco Catalyst 9800 Series Wireless Controller Software Configuration Guide](https://www.cisco.com/c/en/us/td/docs/wireless/controller/9800/16-12/config-guide/b_wl_16_12_cg/wpa3.html)
-   [Meraki and WPA3](https://documentation.meraki.com/MR/WiFi_Basics_and_Best_Practices/WPA3_Encryption_and_Configuration_Guide)
-   [Dragonblood: An analysis of the WPA3-SAE handshake](https://blogs.arubanetworks.com/solutions/dragonblood-an-analysis-of-the-wpa3-sae-handshake/)
