# OlsenNoise
Algorithm for Infinite Deterministic Fractal Noise Generation

```python
import OlsenNoise
n = OlsenNoise.noise(0,0,512,512)
from PIL import Image
Image.fromarray(n).save("noise.png")
```

![noise](https://user-images.githubusercontent.com/3302478/101179616-542b7980-35ff-11eb-886e-cbb53c6499fc.png)
![noise3](https://user-images.githubusercontent.com/3302478/101180193-1c710180-3600-11eb-8a7a-c3738e3bf29c.png)

Note, 2nd image created with:

```python
Image.fromarray(OlsenNoise.noise(512, 0, 512, 512)).save("noise3.png")
```
