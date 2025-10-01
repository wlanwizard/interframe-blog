---
title: "WPA3 SAE Anti-Clog Frame Exchanges"
date: 2021-10-31T15:40:15.843000+00:00
draft: false
description: "The WPA3 SAE authentication mechanism (a variant of Dragonfly) is the replacement for WPA2-PSK. It offers improved encryption, perfect forward secrecy, and is resistant to offline attacks. However, online attacks can be attempted and while cracking t..."
slug: wpa3-sae-anti-clog-frame-exchanges
---

The WPA3 SAE authentication mechanism (a variant of Dragonfly) is the replacement for WPA2-PSK. It offers improved encryption, perfect forward secrecy, and is resistant to offline attacks. However, online attacks can be attempted and while cracking the encryption does not seem possible, making the AP calculate the new encryption keys could cause high CPU utilization resulting in DoS. The standard has deployed anti-clogging tokens to counteract this. This is best explained by Hemant Chaskar on this excellent [blog](https://securityscoops.com/2019/04/10/wpa3-security-weaknesses-discovered/):

"_Anti-clogging tokens is a primitive wireless DoS prevention technique in WPA3-Personal. According to it, AP sends tokens to new requesting clients when the AP is overwhelmed with connection requests, because each request triggers PWE computation on the AP. The client has to re-send its connection request including the token that it received from the AP for the request to be accepted. This is done in hope of isolating clients that flood connection requests by spoofing MAC addresses._

Bypassing anti-clogging defenses is trivial since a WLAN adapter in monitor mode + injection can pretend to be all the spoofed clients and reply to the tokens to keep the SAE sessions going. Let's see how it works in action on a Cisco 9115AXI-B Embedded Wireless Controller (EWC) and [Dragondrain](https://github.com/vanhoefm/dragondrain-and-time) to flood spoofed Commit exchanges.

The entire SAE exchange consisted of Commit, Confirm, 802.11 Association 2-way exchanges followed by the classic 4-way EAPOL handshake. Anti-clogging and its DoS condition occurs in the first Commit frame exchange so the other steps are omitted for clarity. Below is the normal SAE Commit exchange of 2 frames:

![](https://interframe.space/wp-content/uploads/2020/08/normal-commit-success.png)

![](https://interframe.space/wp-content/uploads/2020/08/intial-client-to-ap-success.png)

The client (under the anti-clog threshold) sends a Commit 1 frame to the AP to start the SAE handshake

![](https://interframe.space/wp-content/uploads/2020/08/intial-ap-to-client-success.png)

AP responds with its own Commit frame

Once the anti-clog threshold (number of simultaneous of SAE ongoing sessions) is met however, additional clients experience Commit as a 4-frame exchange:

![](https://interframe.space/wp-content/uploads/2020/08/clogged-process.png)

4-frame anti-clog exchange

The AP sends a 64 digit alpha-numeric value for the token that is then replayed back from the client with no modification. Its only purpose is to validate a device is alive at that client MAC address. The PCAPS:

![](https://interframe.space/wp-content/uploads/2020/08/4-way-commit-1.png)

Same initial Commit frame from the client, it doesn't know anti-clogging is in effect yet

![](https://interframe.space/wp-content/uploads/2020/08/AP-to-client-reject-token.png)

AP responses with a Reject message and the anti-clog (AC) token

![](https://interframe.space/wp-content/uploads/2020/08/client-to-AP-respond-w-token.png)

Client tries Commit again, this time with the token

![](https://interframe.space/wp-content/uploads/2020/08/ap-success-AC-frame4_2.png)

The AP completes the Commit phase with a Success message

While this type of defense may be effective at detecting spoofed IP packets on the wire, on a shared medium like Wi-Fi it's simple for the adapter to listen and respond for each spoofed MAC address making anti-clog nearly worthless. Take away as a WLAN professional: avoid this dubious mechanism and don't set the AC threshold low enough for it to be triggered. The Cisco default of 1,500 simultaneous SAE sessions should probably be left alone.
