# Logos and icons

Use the SVG files. `sling-logo-white.svg` (white wordmark, cyan #0ADBDE dot) is the primary logo, for dark grounds. `sling-logo-charcoal.svg` (charcoal #1D1D1D wordmark, cyan dot) is for light grounds. `sling-logo-mono-white.svg` and `sling-logo-mono-charcoal.svg` are single-colour versions for one-colour reproduction. The colours are baked into each file, and none of them use currentColor.

The wordmark is rebuilt from Poppins Bold outlines ("sl", dotless "i", "ng"), with the dot as a true circle centred on the "i" stem. It matches the deck artwork to within a pixel. The two PNGs are the original 981 x 497 px raster extracts from the deck, kept for reference only.

Keep clear space of one dot diameter on every side, and keep the logo at least 72 px wide on screen.

Files in `logos/`: the four SVGs are the masters. The `legacy-*.png` files are the raster extracts from the deck, kept for reference only.

`favicon.svg` is the cyan dot on a charcoal rounded square. Generate the 32 px PNG, apple-touch-icon (180 px) and Open Graph images from it and the logo SVGs.
