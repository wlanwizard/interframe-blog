---
title: "Meraki MR Cable Routing Disconnects"
date: 2021-10-31T15:40:15.897000+00:00
draft: false
description: "The MR-56 and other Meraki access points feature similar Ethernet cable path routing that curves within the AP housing and out through the mounting plate. I recently ran into a puzzling issue on a project installing MR-56's where the AP would be moun..."
slug: meraki-mr-cable-routing-disconnects
---

The MR-56 and other Meraki access points feature similar Ethernet cable path routing that curves within the AP housing and out through the mounting plate. I recently ran into a puzzling issue on a project installing MR-56's where the AP would be mounted, get POE then fail to bring up Ethernet link. The issue was repeating on multiple AP's.

The first suspect was the cabling, thinking the POE pins were connecting but not the Ethernet. The cabling contractor re-tested again from the jack to the patch panel finding no issues. I also tested the AP, switch port, and patch cables but all were good. The AP also worked directly connected to the switch. So what was going on?

Finally after carefully monitoring it was clear the MR-56 lost Ethernet just before it clicked into place on the mounting bracket. The final bit of force was bending the patch cable just enough to put torque on the NIC slightly bending it out of place causing Ethernet to drop but not POE.

This was caused by having a patch cord with an extra-long strain-relief boot along with the tight cable radius forced by the Meraki AP/mounting place design. In addition, the single gang box the bracket was attached to forced the cable to continue the 90-degree bend beyond the AP and bracket.

![](https://interframe.space/wp-content/uploads/2021/02/bent-cable-diagram-exp-reduce.jpg)

The patch cable style, Meraki cable routing, and the gang box forced this tight radius.

![](https://interframe.space/wp-content/uploads/2021/02/cable-force.jpg)

This bending caused the Ethernet link link to disconnect while POE remained on. Meraki MR-56.

The solution was to use a regular patch cable with a short boot to reduce the bend radius. Perhaps a better solution considering the long-term effects on the NIC is to use a 90-degree patch cable like shown below on this MR-52. I found these to be about around 4x more expensive than a standard patch cord ($4 vs $1) but might be worth it considering the time to troubleshoot especially if AP's are mounted in a difficult-to-reach area.

![](https://interframe.space/wp-content/uploads/2021/02/solution-MR52-reduced.jpg)

Eliminate the bend with a 90 degree connector.

While this issue may be attributed to the particular patch cable selected and the gang box forcing the tight radius, it's interesting to note Cisco's AP's offer a potentially more forgiving cable path by comparison.

![](https://interframe.space/wp-content/uploads/2021/02/3802-compare-reduce.jpg)

Cisco 3802i

![](https://interframe.space/wp-content/uploads/2021/02/9115-compare-reduce.jpg)

Cisco 9115AXI

The Aruba 515 path for example is also horizontal while an AP-315 NIC is perpendicular to the mounting surface.

In the big picture this may seem like a minor detail and not even worthy of a blog post but the hours I spent troubleshooting and the fact that I had to RMA one MR-56 with a bad NIC that may have been caused by the bending force, leads me to think this is an important pre-deployment consideration. The fact that POE was not affected made this even more tricky to troubleshoot.

I was lucky that my deployment was relatively small with on-site cable installers and a customer willing to work with me. This could have easily turned into a finger-pointing contest of blaming the structured cabling or the switch, which in this case all were working properly. On a large deployment with difficult to reach AP's this could have major cost implications to troubleshoot, replace patch cables, or worse case RMA multiple units. (Assuming they are even accepted by the RMA process and not considered abuse!)

To prevent this issue in the future, I've updated my standard pre-deployment report to include mounting/cable path instructions and diagrams. I'll also be adding a step in my pre-deployment checklist to include an AP mounting and cable path walk-thru with the installers. 90-degree patch cables will also be highly recommended.
