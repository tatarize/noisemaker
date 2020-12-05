# NoiseMaker

Olsen Noise algorithm for infinite scoped deterministic fractal noise. The noise is deterministic so it's perfectly for tiling and returning to the same postion and having the same regenerated noise. The algorithm is infinite and scoped so only enough values as needed are generated.

```python
from PIL import Image
from noisemaker import noise
Image.fromarray(noise((250, 100), (0, 0), transpose=True)).save("noise0.png")
Image.fromarray(noise((250, 100), (0, 100), transpose=True)).save("noise1.png")
Image.fromarray(noise((250, 100), (0, 200), transpose=True)).save("noise2.png")
```

The `noise()` algorithm requires only the first shape parameter. The `transpose` flag is to covert it into an image ready format.

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
