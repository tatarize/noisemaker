import numpy as np

_MAX_ITERATIONS = 7

_SCALE_FACTOR = 2
_blur_kernel = ((1, 1, 1),
                (1, 1, 1),
                (1, 1, 1))  # Matrix for the blur.
_blur_edge = 2  # extra pixels are needed for the blur (3 - 1).


def noise(x, y, width, height):
    """
    returns a block of Olsen Noise within the given parameters.

    :param x: requested X location.
    :param y: requested Y location.
    :param width: width of noise block
    :param height: height of noise block
    :return:
    """
    r_width = required_dim(width)
    r_height = required_dim(height)
    pixels = np.zeros((r_width, r_height), dtype='uint8')
    _olsen_noise(pixels, x, y)
    return pixels[:width, :height]


def required_dim(dim):
    return dim + _blur_edge + _SCALE_FACTOR


def _olsen_noise(pixels, x=0, y=0, width=None, height=None, iteration=_MAX_ITERATIONS):
    if width is None:
        width = pixels.shape[0]
    if height is None:
        height = pixels.shape[1]
    if iteration == 0:
        # Base case.
        speckle(pixels, x, y, width, height, iteration)
        return
    x_remainder = x & 1  # Adjust the x_remainder so we know how much more into the pixel are.
    y_remainder = y & 1

    _olsen_noise(pixels,
                 ((x + x_remainder) // _SCALE_FACTOR) - x_remainder,
                 ((y + y_remainder) // _SCALE_FACTOR) - y_remainder,
                 ((width + x_remainder) // _SCALE_FACTOR) + _blur_edge,
                 ((height + y_remainder) // _SCALE_FACTOR) + _blur_edge, iteration - 1) # Recursive scope call.

    scale_shift(pixels, width, height, _SCALE_FACTOR, x_remainder, y_remainder)
    apply_blur(pixels, width - _blur_edge, height - _blur_edge)
    speckle(pixels, x, y, width, height, iteration)


def _scale_shift_np(pixels, width, height, factor, shift_x, shift_y):
    """
    Does not work.
    """
    r = pixels[shift_x:width + shift_x, shift_y:height + shift_y]
    kron = np.kron(r, np.ones((factor, factor)))
    pixels[:width * 2, :height * 2] = kron[
                                      :min(width * 2, pixels.shape[0]),
                                      :min(height * 2, pixels.shape[1])]


def scale_shift(pixels, width, height, factor, shift_x, shift_y):
    for y in range(height-1, -1, -1):
        for x in range(width-1, -1, -1):
            pixels[x, y] = pixels[(x+shift_x) // factor, (y+shift_y) // factor]


def speckle(pixels, x_within_field, y_within_field, width, height, iteration):
    for y in range(height):
        for x in range(width):
            pixels[x,y] += (hash_random(x + x_within_field, y + y_within_field, iteration) & (1 << (7 - iteration)))


def apply_noise(pixels, x, y, width, height, iteration):
    """
    add on to this pixel the hash function with the set reduction.
    The amount of randomness here somewhat arbitary. Just have it give self-normalized results 0-255.
    It simply must scale down with the larger number of iterations.

    :param pixels:
    :param x:
    :param y:
    :param width:
    :param height:
    :param iteration:
    :return:
    """
    for index, m in np.ndenumerate(pixels[:width, :height]):
        pixels[index] += hash_random(index[0] + x, index[1] + y, iteration) & (
                    1 << (7 - iteration))


def convolve2(pixels, width, height, matrix=_blur_kernel, offset=0, x=0, y=0):
    """
     Memory Free In-Place Convolution.

     It is modified to not actually do all the color blending work. The values
     passed to it are between 0-255 So it does a proper average.

    :param pixels:  pixels to be modified (pass by reference).
    :param offset:  offset within the pixel array to call zero.
    :param x: the start x value.
    :param y: the start y value.
    :param width: the width of blocks to be used for the convolution.
    :param height: the height of the convolution area.
    :param matrix: matrix of the convolution.
    :return:
    """
    # index is where we are in the pixels. All equal 0 for our use. Y=0, X=0, offset = 0.
    for y in range(height):  # iterate the y values. adding stride to index each time.
        for x in range(width):
            pixels[x, y] = convolve_p(pixels, (x, y), matrix)


def apply_blur(pixels, width, height, matrix=_blur_kernel, offset=0, x=0, y=0):
    for index, m in np.ndenumerate(pixels[:width, :height]):
        pixels[index] = convolve_p(pixels, index, matrix)


def crimp(color):
    """
    crimps the values between 255 and 0. Required for some other convolutions like emboss where they go out of register.
    :param color: color to crimp.
    :return:
    """
    if color > 255:
        return 255
    if color < 0:
        return 0
    return int(color)


def convolve_p(pixels, index, matrix):
    """
    Performs the convolution on that pixel by the given matrix. Note all values within the matrix are down and to the
    right from the current pixel. None are up or to the left. This is by design.
    :param pixels:
    :param index:
    :param matrix:
    :return:
    """
    parts = 0
    sum = 0
    for j in range(len(matrix)):  # iterates the matrix
        for k in range(len(matrix[j])):  # iterates the matrix[] within.
            factor = matrix[j][k]  # gets the multiple from that matrix.
            parts += factor  # keeps a running total for the parts.
            sum += factor * pixels[index[0] + j, index[1] + k]
    if parts == 0:
        return crimp(sum)
    return crimp(sum // parts)


def hash_random(*elements):
    """
    XOR hash the hashed values of each element, in elements
    :param elements: elements to be hashed and xor'ed together.
    :return:
    """
    hash_value = 0
    i = 0
    while i < len(elements):
        hash_value ^= elements[i]
        hash_value = hash(hash_value)
        i += 1
    return hash_value


def hash(v):
    value = v
    original = value
    q = value & 3
    if q == 3:
        value += original
        value ^= value << 32
        value ^= original << 36
        value += value >> 22
    elif q == 2:
        value += original
        value ^= value << 22
        value += value >> 34
    elif q == 1:
        value += original
        value ^= value << 20
        value += value >> 2
    value ^= value << 6
    value += value >> 10
    value ^= value << 8
    value += value >> 34
    value ^= value << 50
    value += value >> 12
    return value


