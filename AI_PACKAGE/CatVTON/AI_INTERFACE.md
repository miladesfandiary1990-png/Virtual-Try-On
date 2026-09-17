# Virtual Try-On AI Interface

## Purpose

This module generates a virtual try-on image by applying an upper-body garment
to a person image using CatVTON.

## Supported Scope

Clothing category:
- Upper-body garments

Expected examples:
- T-shirt
- Shirt
- Jacket
- Manteau

Clothing type passed to the model:

`upper`

---

## Inputs

### Person image

Accepted formats:
- JPG
- JPEG
- PNG
- WEBP

Image constraints:
- Minimum: 256 x 256
- Maximum: 4096 x 4096

The image should contain a visible person suitable for upper-body virtual try-on.

### Garment image

Accepted formats:
- JPG
- JPEG
- PNG
- WEBP

Image constraints:
- Minimum: 256 x 256
- Maximum: 4096 x 4096

The garment should be an upper-body garment.

---

## Python Interface

```python
from vton_module import VirtualTryOn

vton = VirtualTryOn(
    width=384,
    height=512,
    num_inference_steps=50,
    guidance_scale=2.5,
    seed=555,
)

result_image, elapsed_time = vton.generate(
    person_path=person_path,
    garment_path=garment_path,
    cloth_type="upper",
)