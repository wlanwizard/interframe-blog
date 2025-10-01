---
title: "Wireshark 802.11 Retry Filters"
date: 2021-10-31T15:40:15.973000+00:00
draft: false
description: "802.11 frame retries are one of the most important metrics to judge the quality of WLAN communications. Excessive attempts at transmitting 802.11 data frames will result in delay and reduced throughput. For real-time traffic retries should be under 5..."
slug: wireshark-80211-retry-filters
---

802.11 frame retries are one of the most important metrics to judge the quality of WLAN communications. Excessive attempts at transmitting 802.11 data frames will result in delay and reduced throughput. For real-time traffic retries should be under 5% while 15% or less is considered typical for a WLAN serving data applications.

Retries can be caused by interference, hidden nodes, unequal power on up-link/down-links as examples. Since this varies from client to client, by location, and even in link direction, it's often critical during troubleshooting to narrow down the particular data stream you're concerned about to isolate the issue. This is where using Wireshark and display filters come in handy.

It's important to note that 802.11 retries are invisible from layer 3. Pings may look ok but at the same time the layer 2 frame transmissions may be failing. To see layer 2 you need to capture frames for protocol analysis with a WLAN adapter in monitor mode in macOS/Linux or with tools such as the Ekahau Sidekick or WLANPi. Windows captures are limited but may work with certain card/driver combos. (See [Eddie Forero's blog](https://badfi.com/blog/2019/9/3/ep-002-pcapn-w-eddie-wireless-packet-capture-on-the-windows) for more detail)

In this post, I'll assume you have the frames captured. The first step is to select the source and destination of the data frames. First select the source transmitter which can be filtered with: **wlan.ta == (mac)**, then select the L2 receiver of the data filtered as **wlan.da==(mac)** (typically a router/SVI interface on the wired LAN). Note these MAC addresses.

![](https://interframe.space/wp-content/uploads/2021/04/simple-flow-ta-da-macs.png)

Next, in Wireshark open Statistics > IO Graphs. We'll combine the transmitter, receiver and look at just data frames which is **wlan.fc.type == 2**. Combined with the AND operator "&&" the result will be:

![](https://interframe.space/wp-content/uploads/2021/04/io_data_frames.png)

This allows you to view the frames/second overtime and confirm this is the data stream you need. Are there more or fewer frames than expected? If you're capturing a voice conversation for example rates should be fairly steady, while web surfing will show spikes. Once you're convinced this is the stream you need to examine, add on a retry line on top by adding **wlan.fc.retry == 1**:

![](https://interframe.space/wp-content/uploads/2021/04/io_data_plus_retry_frames.png)

Here we can see overall the number of retries looks low compared to the total number of data frames transmitted. But what is the actual retry percentage? A simple way to calculate is to select copy from the IO screen and paste the values in Excel:

![](https://interframe.space/wp-content/uploads/2021/04/excel_calc_2.png)

With a couple SUM functions and taking the retries over total data frames we see we have 4% retries on this particular steam of frames - just under our 5% threshold for voice/real-time protocols.

While there are tools that will present this with less effort (even Wireshark has a WLAN Traffic analysis feature with retries but doesn't seem to work well) I've found it's useful especially when starting out to work with the data at a low level. This helps in understanding how the application protocol operates and to see patterns that can be lost when data is summarized or otherwise manipulated.
