# CatVTON AI Evaluation

## Model

Model: CatVTON  
Checkpoint: `zhengchong/CatVTON`  
Attention checkpoint: `mix`  
Clothing scope: Upper-body garments  
Clothing type used in test: `upper`

## Inference Configuration

Inference steps: 50  
Guidance scale: 2.5  
Seed: 555  
Precision: FP16  
Attention implementation: PyTorch Efficient SDPA

## Hardware

OS: Windows 11 Pro  
CPU: Intel Core i3-4130  
RAM: 16 GB DDR3  
GPU: NVIDIA GTX 1060 6 GB

## Resolution Comparison

| Resolution | Inference Time | Visual Result |
|---|---:|---|
| 768x1024 | 2019.27 s (~33.65 min) | Acceptable, but previous mistakes observed |
| 384x512 | 2040.94 s (~34.02 min) | Better result; previous mistakes not observed |

## Resolution Decision

The 384x512 configuration is selected as the current practical baseline for the local GTX 1060 environment.

The decision is based on the observed visual quality of the tested outputs. 
Although the lower-resolution run was not faster in this experiment, it produced a better result for the tested person/garment pair.

## Current Test Images

Person:
`test_images/person.jpg`

Garment:
`test_images/garment.jpg`

768x1024 result:
`test_images/baseline_768x1024.png`

384x512 result:
`test_images/result_module_test_384x512.png`

## Quality Evaluation Criteria

Each generated result should be evaluated for:

1. Naturalness
2. Garment feature preservation
3. Garment-body fit
4. Identity preservation
5. Visual artifacts

## Current Test Result

Naturalness: Acceptable  
Garment feature preservation: Acceptable  
Garment-body fit: Acceptable  
Identity preservation: Acceptable  
Visual artifacts: Lower in the 384x512 result than in the 768x1024 result

## Current AI Component Status

Input validation: PASS  
Person-mask validation: PASS  
CatVTON generation: PASS  
Reusable `VirtualTryOn` module: PASS  
Resolution comparison: COMPLETE
