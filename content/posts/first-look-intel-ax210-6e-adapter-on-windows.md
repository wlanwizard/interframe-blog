---
title: "First Look: Intel AX210 6E Adapter on Windows"
date: 2021-10-31T15:40:15.906000+00:00
draft: false
description: "The future of WiFi in 6Ghz is here! Sortof. Since the FCC announced the 6Ghz band was opening up for Wi-Fi in April 2020 many of us have been eagerly awaiting the new hardware to try out this new 1200Mhz of spectrum. While ASUS and Samsung have annou..."
slug: first-look-intel-ax210-6e-adapter-on-windows
---

![](https://interframe.space/wp-content/uploads/2020/12/future-now-icon.png)

The future of WiFi in 6Ghz is here! Sortof. Since the FCC announced the 6Ghz band was opening up for Wi-Fi in April 2020 many of us have been eagerly awaiting the new hardware to try out this new 1200Mhz of spectrum. While ASUS and Samsung have announced some early consumer-focused gear, the undercover launch of Intel's AX210 802.11ax 6E adapter marks the start of enterprise Wi-Fi in the new band.

Without 6E access points, there is no real way to use the adapter in 6Ghz but when [Linux drivers](https://www.intel.com/content/www/us/en/support/articles/000005511/network-and-i-o/wireless.html) are eventually available from Intel it may be possible to get a 2nd card to put into hostap mode (software AP). In meantime, here are the basics learned from a Windows install on a Dell laptop. Note: As of December 2020 the AX210 can be found at newegg and eBay _- it ships from China._

The details:

-   WLAN Adapter: Intel AX210
-   Driver: 22.10.0.7
-   OS: Win10 64-bit build 1909
-   M.2 PCIe E slot (SSD type slot will not work)

\*\*\*WARNING _Please check laws and regulations in your area regarding radio frequency use before proceeding. Operating a Wi-Fi radio without a tested and approved antenna may violate policy_ in your regulatory domain.\*\*\*

Power down your laptop, remove the back cover, and look for the existing Wi-Fi card. Unscrew the hold-down bracket and carefully pry off the antenna leads and remove the card.

![](https://interframe.space/wp-content/uploads/2020/12/pry-out-old2-1024x547.png)

Be carefully with the antenna leads,

![](https://interframe.space/wp-content/uploads/2020/12/ax210-installed.png)

Reverse the process for installing the AX210. Note: this slot must be PCIe, if you have a free M.2 E keyed slot for SSD drives it's not the same and won't work even if the slot type is identical. Connect the antenna leads - this won't be perfect since existing antennas were not designed for 6Ghz but should work for lab testing.

Next, boot up, download, and install drivers from [Intel](https://downloadcenter.intel.com/download/30057?v=t). It will appear as Intel(R) Wi-Fi 6E AX210 160MHz:

![](https://interframe.space/wp-content/uploads/2020/12/adpater-icon-cropped.png)

Now that it's installed let's see what we can find out about the card. Looking under Advanced driver properties we see a couple of 6E related options. The adapter can be limited to 20Mhz operation and the preferred band can be set. Not sure of the benefit of restricting channel width on a typical laptop client but it may be related to [power savings.](https://cse.buffalo.edu/faculty/dimitrio/publications/infocom15.pdf)

![](https://interframe.space/wp-content/uploads/2020/12/driver-channel-width-crop.png)

Auto is default.

![](https://interframe.space/wp-content/uploads/2020/12/driver-prefered-band-crop.png)

Band preference

Then it was time to run it through the WLANPi Profiler. This is a simulated association attempt used to pull capabilities from a client device. The report found that max transmit power was limited to 14dBm power even while max power was selected in the driver settings. This seems low. This is similar to many smartphones, laptop cards often operate at higher levels. Also to note is that no beam-forming is currently supported.

![](https://interframe.space/wp-content/uploads/2020/12/profiler2-.11r-not-reported-bl-1024x243.png)

WLANPI profiler feature from WLAN Pi 1.9.1 \[WLPC edition\]

And finally here's the output from Window's netsh wlan capabilities command, no surprise that monitor mode is not supported on an Intel card with a Windows driver:

WDI Version (Windows) : 0.1.1.8  
WDI Version (IHV) : 0.1.1.9  
Firmware Version : C3.C  
Station : Supported  
Soft AP : Not supported  
Network monitor mode : Not supported  
Wi-Fi Direct Device : Supported  
Wi-Fi Direct GO : Supported  
Wi-Fi Direct Client : Supported  
Protected Management Frames : Supported  
DOT11k neighbor report : Supported  
ANQP Service Information Discovery : Supported  
Action Frame : Supported  
Diversity Antenna : Supported  
IBSS : Not Supported  
Promiscuous Mode : Not Supported  
P2P Device Discovery : Supported  
P2P Service Name Discovery : Supported  
P2P Service Info Discovery : Not Supported  
P2P Background Discovery : Supported  
P2P GO on 5 GHz : Supported  
ASP 2.0 Service Name Discovery : Not Supported  
ASP 2.0 Service Information Discovery : Not Supported  
IP Docking Capable : Not Supported  
FIPS : Supported  
Instant Connect : Supported  
Dx Standby NLO : Supported  
Extended Channel Switch Announcement : Supported  
Function Level Reset : Supported  
Platform Level Reset : Supported  
Bus Level Reset : Not Supported  
MAC Randomization : Supported  
Fast Transition : Supported  
MU-MIMO : Supported  
Miracast Sink : Supported  
BSS Transition (802.11v) : Supported  
IHV Extensibility Module Configured : Supported  
SAE Authentication : Supported  
FTM as Initiator : Not Supported  
MBO Support : Supported  
Number of Tx Spatial Streams : 2  
Number of Rx Spatial Streams : 2  
Number of Concurrent Channels Supported : 0  
P2P GO ports count : 1  
P2P Clients Port Count : 1  
P2P Max Mobile AP Clients : 10  
Max ANQP Service Advertisements Supported : 0  
Co-existence Support : Wi-Fi performance is maintained

Admittedly, just getting a 6E adapter installed doesn't tell us much but it's an important first step in the journey to learn 6E. Look for future posts on AX210 operation under Linux, 6E frame captures, and exploring new concepts like out-of-band discovery.
