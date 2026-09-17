import os
import time

import torch
from diffusers.image_processor import VaeImageProcessor
from huggingface_hub import snapshot_download
from PIL import Image
from torch.nn.attention import SDPBackend, sdpa_kernel

from model.cloth_masker import AutoMasker
from model.pipeline import CatVTONPipeline
from utils import init_weight_dtype, resize_and_crop, resize_and_padding


MIN_IMAGE_SIZE = 256
MAX_IMAGE_SIZE = 4096

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


def validate_image(path, image_type):
    """
    Validate an input image before expensive VTO processing.
    Returns a valid RGB PIL image.
    """

    if not os.path.isfile(path):
        raise ValueError(
            f"{image_type} image was not found: {path}"
        )

    extension = os.path.splitext(path)[1].lower()

    if extension not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            f"{image_type} image format is not supported. "
            f"Use: JPG, JPEG, PNG, or WEBP."
        )

    try:
        with Image.open(path) as image:
            image.verify()
    except Exception:
        raise ValueError(
            f"{image_type} image is corrupted or cannot be read."
        )

    try:
        image = Image.open(path).convert("RGB")
    except Exception:
        raise ValueError(
            f"{image_type} image could not be loaded."
        )

    width, height = image.size

    if width < MIN_IMAGE_SIZE or height < MIN_IMAGE_SIZE:
        raise ValueError(
            f"{image_type} image is too small. "
            f"Minimum size is {MIN_IMAGE_SIZE}x{MIN_IMAGE_SIZE}."
        )

    if width > MAX_IMAGE_SIZE or height > MAX_IMAGE_SIZE:
        raise ValueError(
            f"{image_type} image is too large. "
            f"Maximum size is {MAX_IMAGE_SIZE}x{MAX_IMAGE_SIZE}."
        )

    return image


class VirtualTryOn:
    def __init__(
        self,
        width=768,
        height=1024,
        num_inference_steps=50,
        guidance_scale=2.5,
        seed=555,
    ):
        self.width = width
        self.height = height
        self.num_inference_steps = num_inference_steps
        self.guidance_scale = guidance_scale
        self.seed = seed

        print("Loading CatVTON checkpoint...")

        self.repo_path = snapshot_download(
            repo_id="zhengchong/CatVTON"
        )

        print("Loading CatVTON pipeline...")

        self.pipeline = CatVTONPipeline(
            base_ckpt="booksforcharlie/stable-diffusion-inpainting",
            attn_ckpt=self.repo_path,
            attn_ckpt_version="mix",
            weight_dtype=init_weight_dtype("fp16"),
            use_tf32=False,
            device="cuda",
        )

        print("Loading AutoMasker...")

        self.automasker = AutoMasker(
            densepose_ckpt=os.path.join(
                self.repo_path, "DensePose"
            ),
            schp_ckpt=os.path.join(
                self.repo_path, "SCHP"
            ),
            device="cuda",
        )

        self.mask_processor = VaeImageProcessor(
            vae_scale_factor=8,
            do_normalize=False,
            do_binarize=True,
            do_convert_grayscale=True,
        )

        print("VirtualTryOn initialized successfully.")

    def generate(
        self,
        person_path,
        garment_path,
        cloth_type="upper",
    ):
        person_image = validate_image(
            person_path,
            "Person",
        )

        garment_image = validate_image(
            garment_path,
            "Garment",
        )

        person_image = resize_and_crop(
            person_image,
            (self.width, self.height),
        )

        cloth_image = resize_and_padding(
            garment_image,
            (self.width, self.height),
        )

        try:
            mask = self.automasker(
                person_image,
                cloth_type,
            )["mask"]
        except Exception as e:
            raise ValueError(
                "Could not detect a usable person in the person image."
            ) from e

        if mask is None or mask.getbbox() is None:
            raise ValueError(
                "Could not detect a usable person in the person image."
            )

        mask = self.mask_processor.blur(
            mask,
            blur_factor=9,
        )

        generator = torch.Generator(
            device="cuda"
        ).manual_seed(self.seed)

        torch.cuda.synchronize()
        start_time = time.time()

        with torch.inference_mode():
            with sdpa_kernel(
                SDPBackend.EFFICIENT_ATTENTION
            ):
                result_image = self.pipeline(
                    image=person_image,
                    condition_image=cloth_image,
                    mask=mask,
                    num_inference_steps=self.num_inference_steps,
                    guidance_scale=self.guidance_scale,
                    generator=generator,
                )[0]

        torch.cuda.synchronize()

        elapsed_time = time.time() - start_time

        return result_image, elapsed_time