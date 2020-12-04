# OlsenNoise
Algorithm for Infinite Deterministic Fractal Noise Generation

```python
import OlsenNoise
n = OlsenNoise.noise(0,0,512,512)
from PIL import Image
Image.fromarray(n).save("noise.png")
```

![noise](https://user-images.githubusercontent.com/3302478/101179616-542b7980-35ff-11eb-886e-cbb53c6499fc.png)
