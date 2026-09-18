# AI Sources and Licenses

## CatVTON

Project:
CatVTON — Concatenation Is All You Need for Virtual Try-On with Diffusion Models

Official GitHub:
https://github.com/Zheng-Chong/CatVTON

Model:
https://huggingface.co/zhengchong/CatVTON

Paper:
https://arxiv.org/abs/2407.15886

License:
Creative Commons BY-NC-SA 4.0

CatVTON states that its code, checkpoints, and demo are provided under CC BY-NC-SA 4.0.
The project is therefore used here for non-commercial portfolio/educational work,
with attribution to the original authors.

## Stable Diffusion Inpainting

Model:
https://huggingface.co/booksforcharlie/stable-diffusion-inpainting

License:
CreativeML OpenRAIL-M

CatVTON uses Stable Diffusion v1.5 inpainting as its base model.

## Automatic Mask Generation

CatVTON's application uses:

- DensePose
- SCHP

These components are used for automatic human/clothing mask generation.

Their respective original licenses and attribution requirements must be
preserved when distributing their code or weights.

## Our Contribution

The project does not train CatVTON from scratch.

Our AI contribution consists of:

- Selecting CatVTON for the virtual try-on task.
- Defining an upper-body clothing scope.
- Building image validation.
- Integrating automatic person-mask validation.
- Creating a reusable VirtualTryOn inference module.
- Selecting and testing an inference configuration for the available GPU.
- Comparing 768x1024 and 384x512 configurations.
- Performing a five-case qualitative evaluation.
- Recording inference-time and quality results.
- Defining the AI interface for integration with the application layer.