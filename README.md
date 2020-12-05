# NoiseMaker

Currently using Olsen Noise algorithm for infinite scoped deterministic fractal noise.

```python
from PIL import Image
from noisemaker import noise
Image.fromarray(noise((250, 100), (0, 0), transpose=True)).save("noise0.png")
Image.fromarray(noise((250, 100), (0, 100), transpose=True)).save("noise1.png")
Image.fromarray(noise((250, 100), (0, 200), transpose=True)).save("noise2.png")
```

The `noise()` algorithm requires only the first shape parameter. The `transpose` flag is to covert it into an image ready format.

* ![noise0](https://user-images.githubusercontent.com/3302478/101229669-34737000-3656-11eb-9820-2e18fae18918.png)
* ![noise1](https://user-images.githubusercontent.com/3302478/101229676-4523e600-3656-11eb-8ce1-74062438f93b.png)
* ![noise2](https://user-images.githubusercontent.com/3302478/101229681-48b76d00-3656-11eb-8641-8cb1cdd680ee.png)

Note these are three different images. Simply adjacent in the requested space, so they stack.


```python
from noisemaker import noise
from PIL import Image
Image.fromarray(noise(500, 500, iteration=5)).save("noise-5.png")
```

![noise-5](https://user-images.githubusercontent.com/3302478/101246313-5c4eec00-36c7-11eb-9d4f-49e4d080ddca.png)


There is also a gaussian kernel availible:

```python
from noisemaker import noise, GAUSSIAN
from PIL import Image
Image.fromarray(noise(500, 500, iteration=5, kernel=GAUSSIAN)).save("noise-5g.png")
```

![noise-5g](https://user-images.githubusercontent.com/3302478/101246329-738dd980-36c7-11eb-8419-89d7b9379207.png)
