---
title: "Convert Floorplans from PDF to PNG with Poppler"
date: 2021-10-31T15:40:15.856000+00:00
draft: false
description: "The Ekahau Advanced course demonstrates many benefits of using raster-based/png maps in Ekahau over CAD/vector. It decreases application load times, makes cropping and image manipulation possible, and lets you swap out images at a later time if floor..."
slug: convert-floorplans-from-pdf-to-png-with-poppler
---

The Ekahau Advanced course demonstrates many benefits of using raster-based/png maps in Ekahau over CAD/vector. It decreases application load times, makes cropping and image manipulation possible, and lets you swap out images at a later time if floor plans change ([here is a post on Ekahau map swap](https://interframe.space/ekahau-map-swap-trick/)). I've found it's often faster to manually draw walls on a PNG image than it is to wait for Ekahau to process DWF files during import. You also have control over how walls are drawn. If you can get high-resolution png's, you can still zoom in with enough detail for surveys and analysis.

The key is getting images in png format. If you're starting with DWG you can [export from DWG-TrueView](https://firemywires.tumblr.com/post/64783477803/converting-dwg-files-to-use-for-wireless-site). However, often PDF versions are provided so we need a high quality and batch friendly way to export to PNG. A great solution I've found is the pdftopppm tool within the open-source Poppler package available for Linux/WSL/macOS (Homebrew).

First, use Linux or [Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/install-win10) in Windows to install Poppler utilities. If using a Debian based distro such as Ubuntu, you'd run apt-get to install the Poppler tools we need:

```
sudo apt-get install poppler-utils
```

Now we can export each page of a PDF document into a PNG. Note: if your PDF was created with low-res images then you can't make it high-res. This works best if the PDF has high-res or vector images embedded.

```
pdftoppm -png customer_floorplan.pdf floorplan_export
```

To control the DPI of the resulting image play with the -r (resolution) options. I've found 600 DPI is a good compromise of zoomable detail and file size:

```
pdftoppm -r 600 -png customer_floorplan.pdf floorplan_export_600
```

I typically crop images after export in a tool such as Paint.Net for Windows, however, Popper will also crop during export which could save a lot of time on building plans with repeating floors. Converting to greyscale may also help with readability so your AP's stand out better. Here are all the options:

```
Usage: pdftoppm [options] [PDF-file [PPM-file-prefix]]
  -f <int>                 : first page to print
  -l <int>                 : last page to print
  -o                       : print only odd pages
  -e                       : print only even pages
  -singlefile              : write only the first page and do not add digits
  -r <fp>                  : resolution, in DPI (default is 150)
  -rx <fp>                 : X resolution, in DPI (default is 150)
  -ry <fp>                 : Y resolution, in DPI (default is 150)
  -scale-to <int>          : scales each page to fit within scale-to*scale-to pixel box
  -scale-to-x <int>        : scales each page horizontally to fit in scale-to-x pixels
  -scale-to-y <int>        : scales each page vertically to fit in scale-to-y pixels
  -x <int>                 : x-coordinate of the crop area top left corner
  -y <int>                 : y-coordinate of the crop area top left corner
  -W <int>                 : width of crop area in pixels (default is 0)
  -H <int>                 : height of crop area in pixels (default is 0)
  -sz <int>                : size of crop square in pixels (sets W and H)
  -cropbox                 : use the crop box rather than media box
  -mono                    : generate a monochrome PBM file
  -gray                    : generate a grayscale PGM file
  -png                     : generate a PNG file
  -jpeg                    : generate a JPEG file
  -jpegopt <string>        : jpeg options, with format <opt1>=<val1>[,<optN>=<valN>]*
  -tiff                    : generate a TIFF file
  -tiffcompression <string>: set TIFF compression: none, packbits, jpeg, lzw, deflate
  -freetype <string>       : enable FreeType font rasterizer: yes, no
  -thinlinemode <string>   : set thin line mode: none, solid, shape. Default: none
  -aa <string>             : enable font anti-aliasing: yes, no
  -aaVector <string>       : enable vector anti-aliasing: yes, no
  -opw <string>            : owner password (for encrypted files)
  -upw <string>            : user password (for encrypted files)
  -q                       : don't print any messages or errors
  -v                       : print copyright and version info
  -h                       : print usage information
  -help                    : print usage information
  --help                   : print usage information
  -?                       : print usage information
```

References:

-   https://poppler.freedesktop.org/
-   https://www.linuxuprising.com/2019/03/how-to-convert-pdf-to-image-png-jpeg.html
-   for macOS: https://formulae.brew.sh/formula/poppler
-   https://docs.microsoft.com/en-us/windows/wsl/install-win10
