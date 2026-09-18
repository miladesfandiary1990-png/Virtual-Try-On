# AI Team Handoff

## 1. AI Component

The AI component is implemented in:

```text
vton_module.py
```

The main class is:

```python
VirtualTryOn
```

The application layer should interact with this class rather than directly calling CatVTON internals.

---

## 2. Initialization

Create the model once when the application starts:

```python
from vton_module import VirtualTryOn

vton = VirtualTryOn(
    width=384,
    height=512,
    num_inference_steps=50,
    guidance_scale=2.5,
    seed=555,
)
```

Do not create a new `VirtualTryOn` object for every request.

Model initialization loads the required pretrained models and should therefore be treated as an expensive startup operation.

---

## 3. Generation Call

Use:

```python
result_image, elapsed_time = vton.generate(
    person_path=person_path,
    garment_path=garment_path,
    cloth_type="upper",
)
```

### Inputs

`person_path`

Path to the uploaded person image.

`garment_path`

Path to the uploaded garment image.

`cloth_type`

Currently:

```text
upper
```

Only upper-body clothing is supported.

---

## 4. Successful Output

The method returns:

```python
result_image
```

A PIL Image containing the generated try-on result.

and:

```python
elapsed_time
```

Inference time in seconds.

The application layer can use `elapsed_time` to display processing duration or record performance statistics.

---

## 5. Errors

The AI module raises exceptions when an input cannot be processed.

The application layer should catch exceptions around the generation call:

```python
try:
    result_image, elapsed_time = vton.generate(
        person_path=person_path,
        garment_path=garment_path,
        cloth_type="upper",
    )

except ValueError as e:
    # Show a user-friendly input/AI validation message

except Exception as e:
    # Show a general generation error
```

Do not expose raw Python tracebacks to normal users.

---

## 6. Validation Performed by AI

The AI module checks:

* File existence
* Image format
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

Size limits:

```text
Minimum: 256 × 256
Maximum: 4096 × 4096
```

---

## 7. Recommended User-Facing Error Messages

The application should translate technical errors into simple messages.

Examples:

```text
Please upload a person image.
```

```text
Please upload a garment image.
```

```text
This image format is not supported. Please use JPG, PNG, or WEBP.
```

```text
This image could not be read. Please upload another image.
```

```text
The image is too small. Please upload a higher-resolution image.
```

```text
No suitable person could be detected in this image.
Please upload a clearer full-body or upper-body person image.
```

```text
The garment could not be processed. Please try another garment image.
```

```text
Virtual try-on generation failed. Please try another image pair.
```

---

## 8. UI Requirements Relevant to AI

The application should provide:

1. Person image upload
2. Garment image upload/selection
3. Generate button
4. Processing status
5. Generated result
6. Original vs generated comparison
7. User-friendly error messages

During generation, the application should clearly indicate that processing is in progress because the tested local hardware can require several minutes.

---

## 9. Performance

Test hardware:

```text
NVIDIA GTX 1060 6 GB
Intel Core i3-4130
16 GB RAM
Windows 11 Pro
```

Current baseline:

```text
Resolution: 384 × 512
Steps: 50
Guidance: 2.5
Precision: FP16
```

Five-case evaluation:

```text
Successful cases: 5 / 5

Fastest:
2040.74 seconds

Slowest:
3907.25 seconds

Average:
3169.80 seconds
≈ 52.83 minutes
```

These times are specific to the tested hardware and should not be presented as general CatVTON performance.

---

## 10. Resource Warning

The application should initialize the AI model only once.

Creating the model repeatedly can cause unnecessary memory usage and very long startup times.

The application should also prevent multiple simultaneous generation requests if the available GPU cannot safely handle them.

---

## 11. AI Limitations

Current supported clothing scope:

```text
Upper-body garments only
```

Known limitations:

* Garment details are not always perfectly preserved.
* Some visual artifacts may appear.
* Results depend on input-image quality and pose.
* Inference is very slow on the tested GTX 1060.
* The current model configuration has been validated for upper-body try-on.
* Performance will vary substantially with different hardware.

---

## 12. AI Files

The application team only needs to integrate with:

```text
vton_module.py
```

Supporting documentation:

```text
AI_INTERFACE.md
AI_EVALUATION.md
AI_SOURCES_LICENSES.md
AI_README.md
AI_TEAM_HANDOFF.md
```

The evaluation scripts are not required by the application runtime:

```text
test_validation.py
test_vton_module.py
run_evaluation.py
```

---

## 13. Do Not Modify

The application layer should not directly modify:

```text
CatVTONPipeline
AutoMasker
DensePose
SCHP
CatVTON checkpoints
```

Changes to the AI configuration should be coordinated with the AI component owner because they can affect output quality, memory usage, compatibility, and evaluation results.

---

## 14. Final Integration Contract

```text
Application
    ↓
person_path
garment_path
cloth_type="upper"
    ↓
VirtualTryOn.generate()
    ↓
(result_image, elapsed_time)
    ↓
Application
    ↓
Display result + processing time
```

Error path:

```text
Application
    ↓
VirtualTryOn.generate()
    ↓
ValueError / processing exception
    ↓
Application catches error
    ↓
User-friendly message
```

The application layer owns the user experience.

The AI component owns image validation, preprocessing, mask generation, model inference, generated output, and AI-specific errors.
