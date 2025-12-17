# Hexgon
Tool to transform an image from square to hexagonal lattice.

## Theory
This tool uses the method described in [A Framework for Hexagonal Image Processing: Using Hexagonal Pixel-Perfect Approximations in Subpixel Resolution](https://ieeexplore.ieee.org/document/9409677). 

One small correction to the paper was included: formula (37) (and, by extension, formulas (48) and (49)) shows an incorrect value for the upper bound of delta x for the given case(s). This follows from the use of an incorrect value of q when deriving the upper bound ($\dfrac{1}{\sqrt{3}}$ instead of $\dfrac{1}{2\sqrt{3}}$).

## How to use
Run 
```
python main.py FILEPATH
```

FILEPATH should be the path to an image file.

## Requirements
- Numpy
- Pillow
- Matplotlib

## Notes
- Currently, the conversion to hexagonal image only works with grayscale images. A method for converting an RGB image to grayscale is provided. In the future, I will add support for RGB images.
- The calculation for the marker (hexagonal pixel) size has been implemented but not thoroughly tested, and it may not work for some image resolutions or aspect ratios.

## Issues
- Zooming in with the "Zoom to rectangle" tool changes the marker size with respect to the maximum change factor between the old and new height/width. Using the scroll wheel to zoom in, on the other hand, keeps marker size consistent, since the aspect ratio of the plot remains the same.
