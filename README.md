# NoiseMaker

Olsen Noise algorithm for infinite scoped deterministic fractal noise. The noise is deterministic so it's perfectly for tiling and returning to the same postion and having the same regenerated noise. The algorithm is infinite and scoped so only enough values as needed are generated.

# Installing

`pip install noisemaker`

Dependencies:
`numpy`

# Example

```python
from PIL import Image
from noisemaker import noise
Image.fromarray(noise((250, 100), (0, 0), transpose=True)).save("noise0.png")
Image.fromarray(noise((250, 100), (0, 100), transpose=True)).save("noise1.png")
Image.fromarray(noise((250, 100), (0, 200), transpose=True)).save("noise2.png")
```

The `noise()` algorithm requires only the first shape parameter. The `transpose` flag is to covert it into an image ready format.

```python
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
```

# Tiling

* ![noise0](https://user-images.githubusercontent.com/3302478/101229669-34737000-3656-11eb-9820-2e18fae18918.png)
* ![noise1](https://user-images.githubusercontent.com/3302478/101229676-4523e600-3656-11eb-8ce1-74062438f93b.png)
* ![noise2](https://user-images.githubusercontent.com/3302478/101229681-48b76d00-3656-11eb-8641-8cb1cdd680ee.png)

Note these are three different images. Simply adjacent in the requested space, so they stack.

# Box Kernel (Default)

```python
from noisemaker import noise
from PIL import Image
Image.fromarray(noise(500, 500, iteration=5)).save("noise-5.png")
```

![noise-5](https://user-images.githubusercontent.com/3302478/101246313-5c4eec00-36c7-11eb-9d4f-49e4d080ddca.png)


# Gaussian Kernel

There is also a gaussian kernel availible, which is about a third the blur factor of the default box blur:

```python
from noisemaker import noise, GAUSSIAN
from PIL import Image
Image.fromarray(noise((500, 500), iteration=5, kernel=GAUSSIAN)).save("noise-5g.png")
```
![noise-5g](https://user-images.githubusercontent.com/3302478/101246608-47735800-36c9-11eb-8d56-0ac4b4432dbd.png)


# Contributing

The testing is pretty robust and impossible to pass without the algorithm working.

There are a number of speed advancements that could be made to the algorithm. If faster and still passing the tests any PRs will generally be accepted.

Other noise algorithms can be included or other interesting kernels.
