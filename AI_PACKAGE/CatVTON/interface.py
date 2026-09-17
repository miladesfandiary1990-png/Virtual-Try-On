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