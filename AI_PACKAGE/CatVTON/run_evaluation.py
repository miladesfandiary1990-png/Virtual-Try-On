import csv
import os

from vton_module import VirtualTryOn


BASE_DIR = r"C:\CatVTON\evaluation"
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
CSV_PATH = os.path.join(BASE_DIR, "evaluation_results.csv")


CASES = [
    (1, "person_01.jpg", "garment_01.jpg"),
    (2, "person_02.jpg", "garment_02.jpg"),
    (3, "person_03.jpg", "garment_03.jpg"),
    (4, "person_04.jpg", "garment_04.jpg"),
    (5, "person_05.jpg", "garment_05.jpg"),
]


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    vton = VirtualTryOn(
        width=384,
        height=512,
        num_inference_steps=50,
        guidance_scale=2.5,
        seed=555,
    )

    results = []

    for case_id, person_name, garment_name in CASES:
        person_path = os.path.join(BASE_DIR, person_name)
        garment_path = os.path.join(BASE_DIR, garment_name)

        output_path = os.path.join(
            OUTPUT_DIR,
            f"case_{case_id:02d}.png",
        )

        print()
        print("=" * 60)
        print(f"CASE {case_id}")
        print(f"Person:  {person_name}")
        print(f"Garment: {garment_name}")
        print("=" * 60)

        try:
            result_image, elapsed_time = vton.generate(
                person_path=person_path,
                garment_path=garment_path,
                cloth_type="upper",
            )

            result_image.save(output_path)

            print("SUCCESS")
            print(f"Time: {elapsed_time:.2f} seconds")
            print(f"Output: {output_path}")

            results.append({
                "case": case_id,
                "status": "SUCCESS",
                "inference_seconds": round(elapsed_time, 2),
                "output": output_path,
                "error": "",
            })

        except Exception as e:
            print("FAILED")
            print(f"Error: {e}")

            results.append({
                "case": case_id,
                "status": "FAILED",
                "inference_seconds": "",
                "output": "",
                "error": str(e),
            })

    with open(
        CSV_PATH,
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "case",
                "status",
                "inference_seconds",
                "output",
                "error",
            ],
        )

        writer.writeheader()
        writer.writerows(results)

    print()
    print("=" * 60)
    print("EVALUATION COMPLETE")
    print(f"Results CSV: {CSV_PATH}")
    print("=" * 60)


if __name__ == "__main__":
    main()