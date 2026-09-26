# WARDROBE SELECTIONS 👕

## Generative AI Virtual Try-On

A Generative AI Virtual Try-On system that allows a user to upload a person image and an upper-body garment image, then generates a new image showing the person wearing the selected garment.

The project uses the pretrained **CatVTON** model and integrates it into an end-to-end Gradio application with input validation, preprocessing, automatic person-mask generation, inference, history, and result visualization.

---

## Demo

The application provides:

* Person image upload
* Garment image upload
* Virtual Try-On generation
* Processing status
* Generated result
* Original/result comparison
* Result history

> Demo video: `ADD-DEMO-LINK-HERE`

---

## Architecture

```text
Person Image
     +
Garment Image
     ↓
Gradio Portal
     ↓
Input Validation
     ↓
Preprocessing
     ↓
AutoMasker
(DensePose + SCHP)
     ↓
Person / Clothing Mask
     ↓
CatVTON
     ↓
Generated Try-On Image
     ↓
Gradio Result / History
```

### Software Structure

```text
Virtual-Try-On/
│
├── src/
│   ├── app/
│   ├── input/
│   ├── person/
│   ├── garment/
│   ├── fitting/
│   ├── preprocessing/
│   ├── generation/
│   ├── postprocessing/
│   └── pipeline/
│
├── AI_PACKAGE/
│   └── CatVTON/
│
├── tests/
│
├── requirements.txt
├── run.bat
└── README.md
```

---

## AI Model

### CatVTON

The project uses the pretrained CatVTON diffusion-based Virtual Try-On model.

Official repository:

https://github.com/Zheng-Chong/CatVTON

Model checkpoint:

https://huggingface.co/zhengchong/CatVTON

CatVTON uses a Stable Diffusion v1.5 inpainting-based pipeline and a concatenation-based architecture for person and garment representations.

The current project uses:

* Attention checkpoint: `mix`
* Clothing scope: `upper`
* Resolution: `384 × 512`
* Inference steps: `50`
* Guidance scale: `2.5`
* Seed: `555`
* Precision: `FP16`
* Attention: Efficient SDPA

---

## Supported Clothing

Current scope:

**Upper-body garments**

Examples:

* T-Shirts
* Shirts
* Jackets
* Manteaux

The current model interface uses:

```text
cloth_type = "upper"
```

---

## Input Validation

Before generation, the AI component checks:

* File existence
* Supported image format
* Image readability
* Minimum image dimensions
* Maximum image dimensions
* Whether a usable person mask can be generated

Supported formats:

```text
JPG
JPEG
PNG
WEBP
```

Current application-level image limits:

```text
Minimum: 256 × 256
Maximum: 4096 × 4096
```

---

## Running the Application

### Requirements

The tested environment is:

```text
Windows 11 Pro
Python 3.9.13
PyTorch 2.4.0 + CUDA 12.1
Torchvision 0.19.0
NVIDIA GTX 1060 6GB
```

### Start the application

The easiest method on Windows is:

```text
Double-click run.bat
```

The launcher:

1. Activates the Python environment
2. Configures the local environment
3. Starts the Gradio application
4. Waits until the portal is ready
5. Opens the browser automatically

The application is available locally at:

```text
http://127.0.0.1:7860
```

### Manual start

From the project root:

```bat
python -m src.app.gradio_app
```

---

## AI Interface

The application communicates with the AI component through:

```python
generated_image, elapsed_time = tryon_pipeline.run(
    person_image=person_image,
    garment_image=garment_image,
    cloth_type="upper",
)
```

The AI component returns:

* `generated_image`: generated PIL image
* `elapsed_time`: inference time in seconds

---

## Evaluation

Five different person–garment pairs were tested using the same configuration.

### Functional Result

```text
Successful cases: 5 / 5
Success rate on tested cases: 100%
```

This is a functional success rate for the five tested inputs and is not a model accuracy metric.

### Inference Time

```text
Fastest: 2040.74 seconds
Slowest: 3907.25 seconds
Average: 3169.80 seconds
Average: approximately 52.83 minutes
```

Hardware:

```text
NVIDIA GTX 1060 6GB
```

### Qualitative Evaluation

| Criterion                   |  Average |
| --------------------------- | -------: |
| Naturalness                 |  3.8 / 5 |
| Garment Preservation        |  3.4 / 5 |
| Garment-Body Fit            |  4.8 / 5 |
| Identity Preservation       |  5.0 / 5 |
| Artifacts                   |  3.2 / 5 |
| Overall Qualitative Average | 4.04 / 5 |

The strongest observed result was identity preservation.

The main observed limitations were garment-detail preservation, visible artifacts, and long inference time on the available hardware.

---

## Resolution Experiment

Two configurations were tested using the same test pair and keeping the main inference settings fixed.

| Resolution |      Time | Observation                                   |
| ---------- | --------: | --------------------------------------------- |
| 768 × 1024 | 2019.27 s | Acceptable, but visual mistakes were observed |
| 384 × 512  | 2040.94 s | Visually better result in the tested pair     |

The `384 × 512` configuration was selected as the current baseline based on the observed visual result.

The experiment did **not** demonstrate that the lower resolution is always faster.

---

## Engineering Decisions

The main engineering decisions were:

### 1. Pretrained model instead of training from scratch

The project requirement allowed pretrained/open-source models, and training a large diffusion VTO model from scratch was outside the practical compute budget.

### 2. Upper-body scope

The first version focuses on upper-body garments to keep the problem controlled and allow meaningful validation and evaluation.

### 3. FP16 + Efficient SDPA

These settings were selected after testing the pipeline on the available GPU and dealing with VRAM constraints.

### 4. Reusable AI module

The CatVTON inference logic is isolated behind a reusable `VirtualTryOn` interface rather than being embedded directly inside the UI.

### 5. Two-level validation

File/image validation is performed before model processing, and person-mask validation is performed through AutoMasker before generation.

### 6. Controlled evaluation

A fixed seed and fixed main inference settings were used to make experimental comparisons reproducible.

---

## Limitations

* Current support is limited to upper-body garments.
* Inference is very slow on the GTX 1060 6GB.
* Some garment details may not be preserved perfectly.
* Some visual artifacts can occur.
* The evaluation set contains only five test cases.
* Garment semantic compatibility is not currently handled by a separate garment classifier.
* The current store/catalog section is not connected to a production garment database.

---

## Project Contribution

CatVTON is a pretrained model and was not trained from scratch for this project.

The project development work focused on:

* Model selection
* Scope definition
* Environment and dependency compatibility
* Input validation
* Preprocessing
* Automatic mask generation and validation
* AI inference wrapper
* Inference configuration
* Resolution experiments
* Qualitative evaluation
* Runtime measurement
* Error handling
* Gradio integration
* End-to-end testing
* Technical documentation

---

## Testing

The repository includes an application-facing AI pipeline smoke test:

```text
tests/test_tryon_pipeline.py
```

The test verifies the interface between the application pipeline and the AI module without running the expensive diffusion inference.

---

## Documentation

Additional AI documentation:

```text
AI_PACKAGE/CatVTON/AI_README.md
AI_PACKAGE/CatVTON/AI_INTERFACE.md
AI_PACKAGE/CatVTON/AI_EVALUATION.md
AI_PACKAGE/CatVTON/AI_SOURCES_LICENSES.md
AI_PACKAGE/CatVTON/AI_TEAM_HANDOFF.md
```

---

## License

CatVTON is distributed under the **CC BY-NC-SA 4.0** license according to its official repository.

The project also uses other open-source/pretrained components whose licenses must be considered separately.

See:

```text
AI_PACKAGE/CatVTON/AI_SOURCES_LICENSES.md
```

for the recorded source and license information.

---

## References

* CatVTON: https://github.com/Zheng-Chong/CatVTON
* CatVTON Model: https://huggingface.co/zhengchong/CatVTON
* Stable Diffusion Inpainting: https://huggingface.co/booksforcharlie/stable-diffusion-inpainting
* Gradio: https://www.gradio.app/
