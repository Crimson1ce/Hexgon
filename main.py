from PIL import Image
from matplotlib import pyplot as plt
import hexgon as hx
import numpy  as np
import threading


def convert_to_hexagonal(image, array: list):
  """
  Converts the given image to a hexagonal image and 
  stores the result in the first index of the given list
  """
  if len(array) < 1:
    array.append(None)
  array[0] = hx.to_hex(image)

  

def main():
  # read the color image
  print("Reading image...")
  img = np.asarray(Image.open('lena.png'))

  # gimg = np.asarray(Image.open('bear.jpg'))

  # convert to grayscale
  gimg = hx.to_grayscale(img)

  result = [None]
  th = threading.Thread(target=convert_to_hexagonal, args=(gimg, result))
  th.start()

  plot_original = False
  if plot_original == True:
    plot = plt.imshow(gimg)
    plot.set_cmap('gray')
    ax = plt.gca()
    ax.axis("off")
    ax.set_title("Original image")
    plt.show()

  print("Coverting to hexagonal lattice...")

  th.join()

  himg = result[0]

  # convert to a hexagonal image
  #himg = hx.to_hex(gimg)

  print("Done converting")

  hx.display_hex_image(himg)


if __name__ == "__main__":
    main()