import math
from matplotlib import pyplot as plt
from PIL import Image
import numpy as np



_sqrt3 = np.sqrt(3)
_inv_sqrt3 = np.divide(1, _sqrt3)
_half_sqrt3 = np.multiply(0.5, _sqrt3)
_marker_size = 0.68

# horizontal boundaries for horizontal displacement in ascending order
_bounds = [
    0,
   -0.5 + np.divide(  1, _sqrt3),
    0.5 - np.divide(0.5, _sqrt3),
    0.5 + np.divide(0.5, _sqrt3),
    0.5 + np.divide(  1, _sqrt3)
]




######################### start of adapted code 2 #########################

# source: https://stackoverflow.com/questions/48474699/marker-size-alpha-scaling-with-window-size-zoom-in-plot-scatter

##saving some values
xlim = dict()
ylim = dict()
lines = dict()
line_sizes = dict()

# Hardcoded for now, maybe can try to set them based on input image
fig_width, fig_height = 6, 6
fig, ax = None, None

def on_resize(event):
    global fig_factor

    assert fig is not None, "'fig' was not initialized"

    w = fig.get_figwidth()
    h = fig.get_figheight()

    fig_factor = max(w/fig_width,h/fig_height)

    lim_change(ax)


def lim_change(ax):
    lx = ax.get_xlim()
    ly = ax.get_ylim()

    factor = min(
        (xlim[ax][1]-xlim[ax][0])/(lx[1]-lx[0]),
        (ylim[ax][1]-ylim[ax][0])/(ly[1]-ly[0])
    )

    try:
        for line, size in zip(lines[ax],line_sizes[ax]):
            line.set_markersize(size*factor*fig_factor)
    except KeyError:
        pass


#########################  end of adapted code 1  #########################


######################### start of adapted code 2 #########################

# source https://stackoverflow.com/questions/11551049/matplotlib-plot-zooming-with-scroll-wheel

# save a reference to the zoom factory
zoomfac = None

def zoom_factory(ax,base_scale = 2.):
    def zoom_fun(event):
        # get the current x and y limits
        cur_xlim = ax.get_xlim()
        cur_ylim = ax.get_ylim()
        cur_xrange = (cur_xlim[1] - cur_xlim[0])*.5
        cur_yrange = (cur_ylim[1] - cur_ylim[0])*.5
        xdata = event.xdata # get event x location
        ydata = event.ydata # get event y location

        if xdata is None or ydata is None:
            return

        if event.button == 'up':
            # deal with zoom in
            scale_factor = 1/base_scale
        elif event.button == 'down':
            # deal with zoom out
            scale_factor = base_scale
        else:
            # deal with something that should never happen
            scale_factor = 1
            print(event.button)


        # fix issue with home button not working
        ax.figure.canvas.toolbar.push_current()

        # set new limits
        """
        ax.set_xlim([xdata - cur_xrange*scale_factor,
                     xdata + cur_xrange*scale_factor])
        ax.set_ylim([ydata - cur_yrange*scale_factor,
                     ydata + cur_yrange*scale_factor])
        """
        #"""

        ax.set_xlim([xdata - (xdata-cur_xlim[0]) * scale_factor,   # / scale_factor,
                     xdata + (cur_xlim[1]-xdata) * scale_factor])  # / scale_factor])
        ax.set_ylim([ydata - (ydata-cur_ylim[0]) * scale_factor,   # / scale_factor,
                     ydata + (cur_ylim[1]-ydata) * scale_factor])  # / scale_factor])
        #"""

        ax.figure.canvas.draw_idle() # force re-draw the next time the GUI refreshes
        # plt.draw() # force re-draw

    fig = ax.get_figure() # get the figure of interest
    # attach the call back
    fig.canvas.mpl_connect('scroll_event',zoom_fun)

    #return the function
    return zoom_fun

#########################  end of adapted code 2  #########################



def display_hex_image(heximg):
    """
    Displays a hexagonal-pixel based image heximg.
    """

    M, N = heximg.shape
    # one bucket for each possible intensity
    # each bucket will contain two lists: the corresponding x and y coordinates
    # of all the points with that intensity
    levels = [[list(), list()] for _ in range(256)]

    # add every pixel in the image

    # first horizontal position (for 1-based i and j)
    x_start = 0.5 + _inv_sqrt3

    for i in range(1, M + 1):      # rows in heximg
        x = x_start
        for j in range(1, N + 1):  # cols in heximg
            # the coords of each hexagonal pixel will be added to the corresponding intensity bucket
            # x
            levels[heximg[i-1, j-1]][0].append(x)
            # y
            levels[heximg[i-1, j-1]][1].append(-(i if j & 1 == 1 else i + 0.5)) # formulas (54) and (55)

            x += _half_sqrt3 # horizontal step between each hexagon


    global fig, ax

    fig = plt.figure(figsize=(6, 6), constrained_layout=False)
    gs  = fig.add_gridspec(1)
    ax = gs.subplots()

    # fig=plt.figure()
    # ax=fig.add_axes([0,0,1,1])

    ret_lines = list()


    global _marker_size
    # _marker_size = 0.68 = constant / 512 , if it changes to 1280, it becomes smaller
    # constant seems to be about 348.16
    _marker_size = 348.16 / max(M, N)
    for intensity, coords in enumerate(levels):
        x_coords, y_coords = coords

        # if intensity == 12: break

        # assign a hexadecimal string
        # to each pixel intensity
        # the hex string format is 0xHEXA,
        # where HEXA is 2 characters (up to 255)
        # so we multiply it by 3 to get an equally
        # distributed 6-digit hexadecimal value
        c = "#" + (hex(intensity)[2:].zfill(2) * 3)

        if len(x_coords) == len(y_coords) and len(x_coords) > 0:
            ret_lines.extend(ax.plot(x_coords, y_coords, marker='H', ms=_marker_size, mec=c, mfc=c, ls="")) # type: ignore
    lines[ax] = ret_lines
    xlim[ax] = ax.get_xlim()    # type: ignore
    ylim[ax] = ax.get_ylim()    # type: ignore
    line_sizes[ax] = [line.get_markersize() for line in lines[ax]]


    # resize markers when zooming in and out
    fig.canvas.mpl_connect('resize_event', on_resize)
    ax.callbacks.connect('xlim_changed', lim_change) # type: ignore
    ax.callbacks.connect('ylim_changed', lim_change) # type: ignore
    ax.axis("off")  # type: ignore

    # maintain aspect ratio when zooming in
    plt.gca().set_aspect('equal')

    # zoom in with scroll wheel
    global zoomfac
    scale = 2
    zoomfac = zoom_factory(ax, base_scale = scale)

    # plt.tight_layout()
    plt.show()


def to_grayscale(img):
    """
    Converts an image img from RGB to grayscale. img should be numpy array.
    """
    # first, broadcast multiply each pixel by the corresponding percentages of red, green, and blue
    # then, sum the value in each of the innermost array (axis -1 == axis 2), which will then be removed
    # finally, round the values to integers
    g_img = np.uint8(np.round(np.sum(img * np.array([0.299, 0.587, 0.114]), axis=-1)))

    return g_img


def _get_overlapping_area(displacement):
    """
    Returns the overlapping area of the hexagonal and square pixels of height 1,
    given the horizontal and vertical displacements
    """
    dx, dy = displacement
    A = 0

    # if greater than largest boundary, return 0
    if dx > _bounds[4]:
        return 0

    # Eight possible cases
    if dx > _bounds[3]:
        # case 1
        A = _sqrt3 * np.square(_inv_sqrt3 + 0.5 - dx)

    elif dx > _bounds[2]:
        # case 3
        A = np.multiply(0.25, _sqrt3) + 0.5 - dx

    elif dx > _bounds[1]:
        # case 5
        A = 0.5 + np.multiply(0.25, _sqrt3) - dx - np.multiply(_sqrt3, np.square(0.5 - np.multiply(0.5, _inv_sqrt3) - dx))

    elif dx > _bounds[0]:
        # case 7
        A = 1 - np.multiply(_sqrt3,
                    np.square(0.5 - np.multiply(0.5, _inv_sqrt3) - dx)
                  + np.square(0.5 - np.multiply(0.5, _inv_sqrt3) + dx)
                            )

    # cases 2, 4, 6, and 8 are half of cases 1, 3, 5, and 7, respectively
    if dy == 0.5:
            A = np.multiply(0.5, A)

    # if none of the conditions was satisfied, A remains 0
    return A


def to_hex(squimg):
    """
    Converts an image squimg from a rectangular to hexagonal lattice.
    The resulting image is returned in the form of a matrix (numpy
    multidimensional array). Every other column has one less pixel in
    it, so the last element from every odd column is 0 but should be
    ignored (first column is the 0th, so it will be even).

    At the moment, the function is only implemented for grayscale
    images.
    """

    if len(squimg.shape) != 2:
        return None

    global _sqrt3, _inv_sqrt3

    M, N = squimg.shape
    print(M, N)

    Mh, Nh = M, int(np.floor(2 * N * _inv_sqrt3))

    heximg = np.zeros((Mh, Nh), dtype="uint8")

    for i in range(1, Mh + 1):
        for j in range(1, Nh + 1):

            # calculate x_h and y_h using (54), y_h is integer
            # (54) x_h, y_h = 0.5 + ((3 * j - 1) / (2 * _sqrt3)), i
            # (55) x_h, y_h = 0.5 + ((3 * j - 1) / (2 * _sqrt3)), i + 0.5

            # x_h is identical in both cases, y_h is the only difference
            x_h = 0.5 + ((((3 * j) - 1) >> 1) * _inv_sqrt3)
            y_h = i # will add 0.5 later on if j is even

            delta_x_pk, delta_y_pk = 0, 0

            # coordinates of possibly overlapping pixels
            squixels = []

            # calculate the coordinates of every pixel that might have an overlap
            if j % 2 == 1: # it is faster to do the same check again # if y_h == i:

                # y_h is an integer in this case

                # at most three pixels overlap, use (56)
                p2 = (int(round(x_h)), y_h)
                p1 = (p2[0] - 1, p2[1])
                p3 = (p2[0] + 1, p2[1])

                # add to the list of overlaps
                squixels.append(p1)
                squixels.append(p2)
                squixels.append(p3)

            else:
                y_h = y_h + 0.5
                # at most six pixels overlap, use (58)
                p2 = (int(round(x_h)), int(y_h - 0.5))  # closes integer to x_h
                p1 = (p2[0] - 1, p2[1])
                p3 = (p2[0] + 1, p2[1])
                p4 = (p2[0] - 1, p2[1] + 1)
                p5 = (p2[0]    , p2[1] + 1)
                p6 = (p2[0] + 1, p2[1] + 1)

                # add to the list of overlaps
                squixels.append(p1)
                squixels.append(p2)
                squixels.append(p3)
                squixels.append(p4)
                squixels.append(p5)
                squixels.append(p6)

            # calculate delta_x_pk and delta_y_pk for all k using (57)
            delta_ps = [ (abs(x - x_h), abs(y - y_h)) for x, y in squixels]

            # calculate overlap of neighbors for hexagonal pixel (i,j) using (42) to (49)
            areas = [_get_overlapping_area(disp) for disp in delta_ps]

            # in squixels, each coordinate is (x, y) and composed of integers,
            # which correspond to (j, i) in the matrix
            def valid(sqix, M, N):
                return sqix[0] >= 0 and sqix[0] < N and sqix[1] >= 0 and sqix[1] < M

            # Calculate intensity of hexagonal pixel (i,j) using (3).
            # set the value of the pixel in the matrix heximg
            heximg[i-1][j-1] = np.round(sum(areas[k]
                                          * (squimg[squixels[k][1] - 1, squixels[k][0] - 1]
                                             if valid(squixels[k], M, N) else 0)  # do not take into account pixels that are out of range
                            for k in range(len(areas))))
        # end j
    # end i

    return heximg
