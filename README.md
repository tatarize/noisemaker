# OlsenNoise
Algorithm for Infinite Deterministic Fractal Noise Generation

```python
from PIL import Image
import OlsenNoise
Image.fromarray(OlsenNoise.noise(0, 0, 250, 100)).save("noise0.png")
Image.fromarray(OlsenNoise.noise(0, 100, 250, 100)).save("noise1.png")
Image.fromarray(OlsenNoise.noise(0, 200, 250, 100)).save("noise2.png")
```

* ![noise0](https://user-images.githubusercontent.com/3302478/101229669-34737000-3656-11eb-9820-2e18fae18918.png)
* ![noise1](https://user-images.githubusercontent.com/3302478/101229676-4523e600-3656-11eb-8ce1-74062438f93b.png)
* ![noise2](https://user-images.githubusercontent.com/3302478/101229681-48b76d00-3656-11eb-8641-8cb1cdd680ee.png)

Note these are three different images. Simply adjacent in the requested space.



```python
import OlsenNoise
from PIL import Image
Image.fromarray(OlsenNoise.noise(0, 0, 500, 500, iteration=5)).save("noise-5.png")
```

![noise-5](https://user-images.githubusercontent.com/3302478/101229929-751fb900-3657-11eb-9bd7-c84373bc79bd.png)

