import sys
from pathlib import Path

from PIL import Image


REPO_ROOT = Path(__file__).resolve().parents[1]

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.pipeline import tryon_pipeline


class FakeVirtualTryOn:
    def generate(self, person_path, garment_path, cloth_type="upper"):
        assert Path(person_path).exists()
        assert Path(garment_path).exists()
        assert cloth_type == "upper"

        person = Image.open(person_path).convert("RGB")
        garment = Image.open(garment_path).convert("RGB")

        assert person.size == (100, 100)
        assert garment.size == (80, 80)

        return person, 1.23


def test_tryon_pipeline_wrapper():
    person = Image.new("RGB", (100, 100))
    garment = Image.new("RGB", (80, 80))

    tryon_pipeline._get_vton = lambda: FakeVirtualTryOn()

    result, elapsed_time = tryon_pipeline.run(
        person_image=person,
        garment_image=garment,
    )

    assert isinstance(result, Image.Image)
    assert result.size == (100, 100)
    assert elapsed_time == 1.23


if __name__ == "__main__":
    test_tryon_pipeline_wrapper()
    print("Try-on pipeline wrapper test: PASS")