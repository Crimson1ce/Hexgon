# Hexgon
Tool to transform an image from square to hexagonal lattice.

## Theory

This tool uses the method described in [A Framework for Hexagonal Image Processing: 
Using Hexagonal Pixel-Perfect Approximations in Subpixel Resolution](https://ieeexplore.ieee.org/document/9409677). 

One small correction to the paper was included: formula (37) (and, by extension, formulas (48) and (49))
shows an incorrect value for the upper bound of delta x for the given case(s). This follows from the use
of an incorrect value of q when deriving the upper bound ($\dfrac{1}{\sqrt{3}}$ instead of $\dfrac{1}{2\sqrt{3}}$).

## How to use
Run 
```
python main.py
```

Currently, the image path is hardcoded in main.py, but I hope to change in near future.
Additionally, the required marker size might change depending on the image resolution and
aspect ratio. In the future I will try to implement an automatic marker size detection, 
but for now the marker size needs to be manually changed for every image.