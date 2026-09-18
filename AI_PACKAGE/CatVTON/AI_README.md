# CatVTON Virtual Try-On — AI Component

## Overview

This project implements the AI component of a Virtual Try-On system.

The system takes:

* A person image
* An upper-body garment image

and generates an image of the person wearing the selected garment.

The project uses the pretrained CatVTON diffusion-based virtual try-on model rather than training a model from scratch. CatVTON is designed for virtual try-on and uses Stable Diffusion v1.5 inpainting together with DensePose and SCHP for automatic mask generation.

## AI Scope

Current supported clothing category:

**Upper-body garments**

Examples:

* T-shirt
* Shirt
* Jacket
* Manteau

The current implementation uses:

```text
cloth_type = "upper"
```

## AI Pipeline

```text
Person Image
      +
Garment Image
      ↓
Input Validation
      ↓
Image Preprocessing
      ↓
Automatic Person Mask Generation
(DensePose + SCHP)
      ↓
Mask Validation
      ↓
CatVTON Inference
      ↓
Generated Try-On Image
      +
Inference Time
```

## Input Validation

Before model inference, the AI module checks:

* File existence
* Supported image format
* Image readability
* Minimum image size
* Maximum image size

Supported formats:

```text
JPG
JPEG
PNG
WEBP
```

Current image limits:

```text
Minimum: 256 × 256
Maximum: 4096 × 4096
```

The person image is additionally checked through CatVTON's automatic mask generation process. If a usable person mask cannot be generated, the request is rejected with an explicit error.

## Model

Model:

**CatVTON**

Attention checkpoint:

```text
mix
```

Inference resolution:

```text
384 × 512
```

Inference steps:

```text
50
```

Guidance scale:

```text
2.5
```

Seed:

```text
555
```

Precision:

```text
FP16
```

Attention implementation:

```text
PyTorch Efficient SDPA
```

## Python Interface

The reusable AI interface is:

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
```

### Outputs

`result_image`

A PIL image containing the generated virtual try-on result.

`elapsed_time`

Inference time in seconds.

## Hardware Used for Evaluation

The main local evaluation was performed on:

```text
OS: Windows 11 Pro
CPU: Intel Core i3-4130
RAM: 16 GB DDR3
GPU: NVIDIA GTX 1060 6 GB
Python: 3.9.13
PyTorch: 2.4.0 + CUDA 12.1
Torchvision: 0.19.0
```

## Resolution Experiment

Two configurations were tested using the same person image, garment image, seed, guidance scale, and 50 inference steps.

| Resolution | Inference Time | Observed Result                                           |
| ---------- | -------------: | --------------------------------------------------------- |
| 768 × 1024 |      2019.27 s | Acceptable, but previous visual mistakes were observed    |
| 384 × 512  |      2040.94 s | Better visual result; previous mistakes were not observed |

The 384 × 512 configuration was selected as the current practical baseline for the local environment.

The lower resolution was not selected because it was faster; the measured runtime was approximately the same in this comparison. The decision was based on the observed visual result.

## Five-Case Evaluation

Five different person–garment pairs were evaluated using the 384 × 512 configuration.

Generation success:

```text
5 / 5
100% for the tested cases
```

Inference time:

```text
Fastest: 2040.74 seconds
Slowest: 3907.25 seconds
Average: 3169.80 seconds
Average: approximately 52.83 minutes
```

### Qualitative Evaluation

Each generated image was scored from 1 to 5.

| Criterion                   | Average Score |
| --------------------------- | ------------: |
| Naturalness                 |       3.8 / 5 |
| Garment preservation        |       3.4 / 5 |
| Garment-body fit            |       4.8 / 5 |
| Identity preservation       |       5.0 / 5 |
| Artifacts                   |       3.2 / 5 |
| Overall qualitative average |      4.04 / 5 |

The strongest observed characteristic was identity preservation.

The main limitations were garment-detail preservation and visible artifacts.

## Known Limitations

* Only upper-body garments are currently supported.
* Local inference is very slow on the GTX 1060 6GB.
* Generation time varies significantly between inputs.
* Garment detail is not always preserved perfectly.
* Visual artifacts can remain in some outputs.
* Results depend on the quality and suitability of the input images.
* The measured runtime should only be considered representative of the tested hardware and configuration.

## Project Contribution

The pretrained CatVTON model itself was not developed from scratch.

The AI work in this project includes:

* Selecting CatVTON for the virtual try-on task
* Defining the supported upper-body garment scope
* Building input validation
* Integrating automatic person-mask validation
* Creating a reusable `VirtualTryOn` inference module
* Selecting an inference configuration for the available hardware
* Comparing two inference resolutions
* Conducting a five-case qualitative evaluation
* Measuring inference time
* Documenting AI inputs, outputs, dependencies, limitations, and integration requirements

## Files

Important AI files:

```text
vton_module.py
test_validation.py
test_vton_module.py
run_evaluation.py
AI_INTERFACE.md
AI_EVALUATION.md
AI_SOURCES_LICENSES.md
requirements-working.txt
```

Evaluation outputs:

```text
evaluation/
├── outputs/
│   ├── case_01.png
│   ├── case_02.png
│   ├── case_03.png
│   ├── case_04.png
│   └── case_05.png
└── evaluation_results.csv
```

## Reproducibility

The AI environment was tested with:

```text
Python 3.9.13
PyTorch 2.4.0
Torchvision 0.19.0
NumPy 1.26.4
Diffusers 0.29.2
Accelerate 0.34.2
Transformers 4.46.3
PEFT 0.17.1
```

The exact working dependency versions are recorded in:

```text
requirements-working.txt
```

PyTorch and Torchvision should be installed using the CUDA-compatible configuration appropriate for the target machine.

## License and Attribution

CatVTON's official repository states that its code, checkpoints, and demo are released under the Creative Commons BY-NC-SA 4.0 license.

This project therefore treats CatVTON as a reused pretrained component and preserves attribution and the applicable non-commercial/share-alike requirements.

The project also relies on other pretrained/open-source components, including Stable Diffusion inpainting, DensePose, and SCHP. Their individual licenses and attribution requirements must be preserved separately.

See:

```text
AI_SOURCES_LICENSES.md
```

for the project's recorded source and license information.

## AI Status

```text
Input validation          PASS
Person-mask validation    PASS
CatVTON inference         PASS
Reusable AI module        PASS
Resolution experiment    COMPLETE
Five-case evaluation      COMPLETE
AI integration contract   COMPLETE
```
