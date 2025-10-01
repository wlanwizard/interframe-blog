---
title: "Ekahau Map Swap Trick"
date: 2021-10-31T15:40:16.061000+00:00
draft: false
description: "Its common during the WLAN design cycle for floor plans to change especially if new construction is involved. If you're using a tool such as Ekahau Pro its possible to use the map swap feature but unless the new map has the same dimensions Ekahau wil..."
slug: ekahau-map-swap-trick
---

Its common during the WLAN design cycle for floor plans to change especially if new construction is involved. If you're using a tool such as Ekahau Pro its possible to use the map swap feature but unless the new map has the same dimensions Ekahau will reject it. Walls and alignment points need to line up. This can get tricky if maps come from different sources. Note: map swap only works with raster (png, jpg) map, it won't work if the original map was CAD.

The method below will allow you to keep your walls, attenuation areas and AP placement while just swapping out the underlying map. The goal is to reflect the floor changes while preserving alignment with the map elements that are staying. These steps will use Ekahau Pro 10.1.3.308 and Paint.Net on Windows. Other image programs such as Photoshop and Gimp can be used. The process is:

1.  Open original image used to create map
2.  Create a 50% opacity layer on top of the original
3.  Paste in new map in this new layer
4.  Line up and expand image to exactly fit over the original
5.  Remove original layer and increase new lay opacity to 100%
6.  Export image and use Swap Map feature in Ekahau

To demonstrate, we'll start our fictional project with a public domain floor plan using a high quality PNG:

![](https://interframe.space/wp-content/uploads/2020/05/map1.png)

Soon you have your walls added, AP's placed and signal:

![](https://interframe.space/wp-content/uploads/2020/05/maps1-with-walls.png)

Walls drawn

![](https://interframe.space/wp-content/uploads/2020/05/maps1-wall-and-ap-sig-2.png)

Add AP's (coverage design)

Let's say at this point the customer informs you that offices in the middle are being eliminated. You are sent a new floor plan with the updates. Assuming you cropped the original it will now be very difficult to crop the new map to the exact same dimensions while having the walls placed in the same x,y coordinates as the original.

The solution is to leverage your old map then layer the new image on top then eliminate the old image.

First import your original image into Paint.Net:

![](https://interframe.space/wp-content/uploads/2020/05/pn_1-1024x785.png)

![](https://interframe.space/wp-content/uploads/2020/05/pn-add-layer-1024x721.png)

Create a new layer

![](https://interframe.space/wp-content/uploads/2020/05/layer-50-opacity.png)

Change opacity to 50%

![](https://interframe.space/wp-content/uploads/2020/05/new-map-on-top-layer-1024x641.png)

Paste updated map into new layer. Line up the new floor plan on top of the original by first aligning one corner then dragging the opposite corner (to keep the original proportions) until they match.

![](https://interframe.space/wp-content/uploads/2020/05/pn-line-up-layers.png)

Drag until new image outside dimensions cover original

![](https://interframe.space/wp-content/uploads/2020/05/pn-merged-complete.png)

Increase opacity on new top layer to reveal new image now aligned to the old

![](https://interframe.space/wp-content/uploads/2020/05/ek-swap-menu.png)

Swap map in Ekahau

![](https://interframe.space/wp-content/uploads/2020/05/ek-final.png)

New map with update interior walls. Walls line up to the original.
