import numpy as np

_MAX_ITERATIONS = 7

_SCALE_FACTOR = 2
BOX = np.ones((3, 3))  # Matrix for the box blur.
GAUSSIAN = np.array([[1, 2, 1],
                     [2, 4, 2],
                     [1, 2, 1]])
_blur_edge = 2  # extra pixels are needed for the blur (3 - 1).


def noise(shape, position=None, **kwargs):
    """
    Returns a block of noise within the specific parameters.

    :param shape: shape of the noise block
    :param position: requested position within the noise.
    :param kwargs:  'iteration'='0-7' number of iterations for the requested noise value.
                    'kernel'=GAUSSIAN, BOX use gaussian or box matrix.
                    'transpose'='True' transpose result.
    :return:
    """
    if position is None:
        position = [0] * len(shape)
    if len(position) != 2:
        raise NotImplementedError
    if len(shape) != 2:
        raise NotImplementedError
    if len(position) != len(shape):
        raise ValueError("Offset and shape values do not match")
    shape = np.array(shape)
    position = np.array(position)

    x, y = position
    r_shape = _required_dim(shape)
    pixels = np.zeros(r_shape, dtype='uint8')
    iteration = _MAX_ITERATIONS
    try:
        iteration = kwargs['iteration']
    except KeyError:
        pass
    kernel = BOX
    if 'kernel' in kwargs:
        kernel = kwargs['kernel']
    if kernel.shape != (3, 3):
        raise NotImplementedError
    width, height = shape
    _olsen_noise(pixels, x, y, width, height, iteration=iteration, kernel=kernel)
    if 'transpose' in kwargs:
        return np.transpose(pixels[:width, :height])
    else:
        return pixels[:width, :height]


def _required_dim(dim):
    """
    Required Dim specifies the amount of extra edge pixels required to process the noise.
    The largest amount is the dim, plus both edge blur bytes, plus the extra scaling factor, and the shift of 1.

    :param dim:
    :return:
    """
    return dim + _blur_edge + _SCALE_FACTOR + 1


def _olsen_noise(pixels, x, y, width, height, iteration=_MAX_ITERATIONS, kernel=BOX):
    """
    Olsen Noise generation algorithm.

    :param pixels: Pixel working space.
    :param x: x location to use for the chunk
    :param y: y location to use for the chunk
    :param width: width of the chunk
    :param height: height of the chunk
    :param iteration: iterations to apply to the noise.
    :return:
    """
    if iteration == 0:
        # Base case.
        _apply_noise(pixels, x, y, width, height, iteration)
        return
    x_remainder = x & 1  # Adjust the x_remainder so we know how much more into the pixel are.
    y_remainder = y & 1

    _olsen_noise(pixels,
                 ((x + x_remainder) // _SCALE_FACTOR) - x_remainder,
                 ((y + y_remainder) // _SCALE_FACTOR) - y_remainder,
                 ((width + x_remainder) // _SCALE_FACTOR) + _blur_edge,
                 ((height + y_remainder) // _SCALE_FACTOR) + _blur_edge, iteration - 1)  # Recursive scope call.

    _scale_shift(pixels, width + _blur_edge, height + _blur_edge, _SCALE_FACTOR, x_remainder, y_remainder)
    _apply_kernel(pixels, width, height, kernel=kernel)
    _apply_noise(pixels, x, y, width, height, iteration)


def _scale_shift(pixels, width, height, factor, shift_x, shift_y):
    """
    Scale_shift pixels located in width and height of the array by the factor given and shifted by shift_x, and shift_y

    This process may be sped up applying np.kron or other accelerations later.

    :param pixels:
    :param width:
    :param height:
    :param factor:
    :param shift_x:
    :param shift_y:
    :return:
    """
    for y in range(height - 1, -1, -1):
        for x in range(width - 1, -1, -1):
            pixels[x, y] = pixels[(x + shift_x) // factor, (y + shift_y) // factor]


def _apply_noise(pixels, x_within_field, y_within_field, width, height, iteration):
    for i, m in np.ndenumerate(pixels[:width, :height]):
        pixels[i] += (_hash_random(i[0] + x_within_field, i[1] + y_within_field, iteration) & (1 << (7 - iteration)))


def _hash_random(*elements):
    """
    XOR hash the hashed values of each element, in elements
    :param elements: elements to be hashed and xor'ed together.
    :return:
    """
    hash_value = 0
    i = 0
    while i < len(elements):
        hash_value ^= elements[i]
        hash_value = _hash(hash_value)
        i += 1
    return hash_value


def _hash(v):
    value = int(v)
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


def _crimp(color):
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


def _apply_kernel(pixels, width, height, kernel=BOX):
    """
    Applies a convolution with the results pixel in the upper left-hand corner.
    :param pixels:
    :param width:
    :param height:
    :param kernel:
    :return:
    """
    for index, m in np.ndenumerate(pixels[:width, :height]):
        pixels[index] = _convolve(pixels, index, kernel)


def _convolve(pixels, index, matrix):
    """
    Performs the convolution on that pixel by the given matrix. Note all values within the matrix are down and to the
    right from the current pixel. None are up or to the left. This is by design.
    :param pixels:
    :param index:
    :param matrix:
    :return:
    """
    parts = 0
    total = 0
    for mi, m in np.ndenumerate(matrix):
        parts += m  # keeps a running total for the parts.
        total += m * pixels[index[0] + mi[0], index[1] + mi[1]]
    if parts == 0:
        return _crimp(total)
    return _crimp(total // parts)
