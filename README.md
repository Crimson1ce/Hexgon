# Hexgon
Tool to transform an image from square to hexagonal lattice.

This tool uses the method described in [A Framework for Hexagonal Image Processing: 
Using Hexagonal Pixel-Perfect Approximations in Subpixel Resolution](https://ieeexplore.ieee.org/document/9409677).

## How to use
Run 
```
python main.py
```

Currently, the image path is hardcoded in main.py, but I hope to change in near future.
Additionally, the required marker size might change depending on the image resolution and
aspect ratio. In the future I will try to implement an automatic marker size detection, 
but for now the marker size needs to be manually changed for every image.