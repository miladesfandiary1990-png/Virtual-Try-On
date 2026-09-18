import sys
import tempfile
from pathlib import Path

from PIL import Image


# ---------------------------------------------------------
# Locate the existing CatVTON AI package
# ---------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parents[2]
CATVTON_DIR = REPO_ROOT / "AI_PACKAGE" / "CatVTON"

if str(CATVTON_DIR) not in sys.path:
    sys.path.insert(0, str(CATVTON_DIR))


from vton_module import VirtualTryOn


# ---------------------------------------------------------
# Model configuration
# ---------------------------------------------------------

_vton = None


def _get_vton():
    global _vton

    if _vton is None:
        print("Loading Virtual Try-On AI model...")

        _vton = VirtualTryOn(
            width=384,
            height=512,
            num_inference_steps=50,
            guidance_scale=2.5,
            seed=555,
        )

    return _vton


# ---------------------------------------------------------
# Public AI interface
# ---------------------------------------------------------

def run(person_image, garment_image, cloth_type="upper"):
    """
    Run Virtual Try-On.

    Inputs:
        person_image: PIL.Image
        garment_image: PIL.Image
        cloth_type: currently "upper"

    Returns:
        generated_image, elapsed_time
    """

    if not isinstance(person_image, Image.Image):
        raise ValueError(
            "Person image must be a PIL image."
        )

    if not isinstance(garment_image, Image.Image):
        raise ValueError(
            "Garment image must be a PIL image."
        )

    person_temp = None
    garment_temp = None

    try:
        # CatVTON's current reusable module accepts file paths.
        # The application provides PIL images, so temporarily
        # save them as PNG files for the AI module.

        with tempfile.NamedTemporaryFile(
            suffix=".png",
            delete=False,
        ) as person_file:
            person_temp = person_file.name

        with tempfile.NamedTemporaryFile(
            suffix=".png",
            delete=False,
        ) as garment_file:
            garment_temp = garment_file.name

        person_image.convert("RGB").save(
            person_temp,
            format="PNG",
        )

        garment_image.convert("RGB").save(
            garment_temp,
            format="PNG",
        )

        vton = _get_vton()

        result_image, elapsed_time = vton.generate(
            person_path=person_temp,
            garment_path=garment_temp,
            cloth_type=cloth_type,
        )

        return result_image, elapsed_time

    finally:
        if person_temp:
            Path(person_temp).unlink(
                missing_ok=True
            )

        if garment_temp:
            Path(garment_temp).unlink(
                missing_ok=True
            )