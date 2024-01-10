from PIL import Image
from matplotlib import pyplot as plt
import hexgon as hx
import numpy  as np
import threading

# constants
PLOT_ORIGINAL = True
FILEPATH = "lena.png"
VERBOSE = True


def main():
  global PLOT_ORIGINAL, FILEPATH, VERBOSE


  IS_RGB = False
  # read the color image
  if VERBOSE: print(f"Reading file '{FILEPATH}'")
  try:
    img = np.asarray(Image.open(FILEPATH))
    IS_RGB = len(img.shape) > 2
  except FileNotFoundError:
      print(f"File '{FILEPATH}' not found.")
      exit()

  # convert to grayscale
  gimg = hx.to_grayscale(img) if IS_RGB else img


  # decided to calculate hex image in a separate thread in case the original 
  # image is displayed.
  result = [None]
  th = threading.Thread(target=convert_to_hexagonal, args=(gimg, result))
  th.start()

  # global boolean to determine if original image is plotted
  if PLOT_ORIGINAL == True:
    plot = plt.imshow(gimg)
    plot.set_cmap('gray')
    ax = plt.gca()
    ax.axis("off")
    ax.set_title("Original image")
    plt.show()

  if VERBOSE: print("Coverting to hexagonal lattice...")

  th.join()

  himg = result[0]

  # convert to a hexagonal image
  #himg = hx.to_hex(gimg)

  if VERBOSE: print("Done converting.")
  if VERBOSE: print("Displaying hexagonal image.")

  hx.display_hex_image(himg)


def convert_to_hexagonal(image, array: list):
  """
  Converts the given image to a hexagonal image and 
  stores the result in the first index of the given list
  """
  if len(array) < 1:
    array.append(None)
  array[0] = hx.to_hex(image)

  
if __name__ == "__main__":
    main()