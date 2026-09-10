import gradio as gr

from src.input.input_manager import InputManager


# =========================================================
# CORE
# =========================================================

input_manager = InputManager()


# =========================================================
# GARMENT PANEL
# =========================================================

def show_garment_upload():
    return (
        gr.update(visible=True),
        gr.update(visible=False),
        "📤 بخش آپلود لباس فعال شد."
    )


def show_garment_store():
    return (
        gr.update(visible=False),
        gr.update(visible=True),
        "🛍️ فروشگاه لباس فعال شد."
    )


# =========================================================
# GENERATE
# =========================================================

def generate(person_image, garment_image, history):

    person_valid, person_message = (
        input_manager.validate_person_image(person_image)
    )

    if not person_valid:
        return (
            person_message,
            history,
            0,
            None,
            "",
            "0 / 0"
        )

    garment_valid, garment_message = (
        input_manager.validate_garment_image(garment_image)
    )

    if not garment_valid:
        return (
            garment_message,
            history,
            0,
            None,
            "",
            "0 / 0"
        )

    if history is None:
        history = []

    # -----------------------------------------------------
    # ORIGINAL = INITIAL PERSON IMAGE
    # -----------------------------------------------------

    if len(history) == 0:
        history = [
            {
                "image": person_image,
                "label": "Original"
            }
        ]

    # -----------------------------------------------------
    # AI PIPELINE
    # -----------------------------------------------------
    #
    # بعداً:
    #
    # generated_image = tryon_pipeline.run(
    #     person_image=person_image,
    #     garment_image=garment_image
    # )
    #
    # -----------------------------------------------------

    generated_image = None

    # -----------------------------------------------------
    # AI NOT CONNECTED
    # -----------------------------------------------------

    if generated_image is None:

        return (
            "✅ تصاویر ورودی معتبر هستند.\n\n"
            "🧠 موتور Virtual Try-On هنوز متصل نشده است.\n"
            "History آماده دریافت Result مدل است.",
            history,
            0,
            history[0]["image"],
            history[0]["label"],
            f"1 / {len(history)}"
        )

    # -----------------------------------------------------
    # RESULT NUMBER
    # -----------------------------------------------------

    result_number = len(
        [
            item
            for item in history
            if item["label"].startswith("Result")
        ]
    ) + 1

    new_result = {
        "image": generated_image,
        "label": f"Result {result_number}"
    }

    # جدیدترین نتیجه همیشه اول
    history.insert(0, new_result)

    return (
        f"✅ {new_result['label']} با موفقیت تولید شد.",
        history,
        0,
        generated_image,
        new_result["label"],
        f"1 / {len(history)}"
    )


# =========================================================
# PREVIOUS
# =========================================================

def previous_result(history, current_index):

    if not history:
        return (
            0,
            None,
            "",
            "0 / 0"
        )

    if current_index > 0:
        current_index -= 1

    item = history[current_index]

    return (
        current_index,
        item["image"],
        item["label"],
        f"{current_index + 1} / {len(history)}"
    )


# =========================================================
# NEXT
# =========================================================

def next_result(history, current_index):

    if not history:
        return (
            0,
            None,
            "",
            "0 / 0"
        )

    last_index = len(history) - 1

    if current_index < last_index:
        current_index += 1

    item = history[current_index]

    return (
        current_index,
        item["image"],
        item["label"],
        f"{current_index + 1} / {len(history)}"
    )


# =========================================================
# CSS
# =========================================================

custom_css = """

/* =====================================================
   VAZIRMATN
   ===================================================== */

@import url(
    'https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700;800&display=swap'
);


/* =====================================================
   GLOBAL
   ===================================================== */

html,
body,
.gradio-container {

    font-family:
        'Vazirmatn',
        sans-serif !important;

    overflow-x: hidden !important;
}


/* =====================================================
   ALL GRADIO ELEMENTS
   ===================================================== */

.gradio-container,
.gradio-container * {

    font-family:
        'Vazirmatn',
        sans-serif !important;
}


/* =====================================================
   RTL
   ===================================================== */

.gradio-container {

    direction: rtl !important;

    max-width: 1200px !important;

    margin: 0 auto !important;
}


/* =====================================================
   MAIN HEADER
   ===================================================== */

.main-title,
.main-title * {

    font-family:
        'Vazirmatn',
        sans-serif !important;

    direction: rtl !important;

    text-align: center !important;

    font-size: 34px !important;

    font-weight: 800 !important;

    line-height: 1.6 !important;

    margin-top: 20px !important;

    margin-bottom: 4px !important;
}


/* =====================================================
   MAIN SUBTITLE
   ===================================================== */

.main-subtitle,
.main-subtitle * {

    font-family:
        'Vazirmatn',
        sans-serif !important;

    direction: rtl !important;

    text-align: center !important;

    font-size: 16px !important;

    font-weight: 400 !important;

    opacity: 0.75 !important;

    margin-top: 0 !important;

    margin-bottom: 28px !important;
}


/* =====================================================
   SECTION TITLES
   ===================================================== */

.section-title,
.section-title * {

    font-family:
        'Vazirmatn',
        sans-serif !important;

    direction: rtl !important;

    text-align: right !important;

    font-size: 20px !important;

    font-weight: 700 !important;

    line-height: 1.8 !important;

    margin-top: 24px !important;

    margin-bottom: 8px !important;
}


/* =====================================================
   SUBTITLES
   ===================================================== */

.subtitle,
.subtitle * {

    font-family:
        'Vazirmatn',
        sans-serif !important;

    direction: rtl !important;

    text-align: right !important;

    font-size: 14px !important;

    font-weight: 400 !important;

    line-height: 1.8 !important;

    opacity: 0.75 !important;

    margin-bottom: 14px !important;
}


/* =====================================================
   MARKDOWN
   ===================================================== */

.gradio-container .markdown,
.gradio-container .markdown *,
.gradio-container .prose,
.gradio-container .prose * {

    font-family:
        'Vazirmatn',
        sans-serif !important;
}


/* =====================================================
   LABELS
   ===================================================== */

.gradio-container label,
.gradio-container label span {

    font-family:
        'Vazirmatn',
        sans-serif !important;

    direction: rtl !important;

    text-align: right !important;
}


/* =====================================================
   TEXT INPUTS
   ===================================================== */

.gradio-container input,
.gradio-container textarea,
.gradio-container select {

    font-family:
        'Vazirmatn',
        sans-serif !important;

    direction: rtl !important;

    text-align: right !important;
}


/* =====================================================
   ALL BUTTONS
   ===================================================== */

.gradio-container button {

    font-family:
        'Vazirmatn',
        sans-serif !important;
}


/* =====================================================
   GARMENT BUTTONS
   ===================================================== */

.garment-button {

    width: 260px !important;

    min-width: 260px !important;

    max-width: 260px !important;

    height: 48px !important;

    min-height: 48px !important;

    flex: 0 0 260px !important;

    white-space: nowrap !important;

    font-family:
        'Vazirmatn',
        sans-serif !important;

    direction: rtl !important;

    text-align: center !important;
}


.garment-button-row {

    width: 100% !important;

    justify-content: center !important;

    align-items: center !important;

    gap: 16px !important;

    margin: 8px auto 16px auto !important;
}


/* =====================================================
   GARMENT UPLOAD
   ===================================================== */

.garment-upload-area {

    margin-top: 12px !important;
}


/* =====================================================
   STORE
   ===================================================== */

.store-panel {

    margin-top: 12px !important;

    padding: 24px !important;

    border-radius: 12px !important;

    text-align: center !important;
}


.store-panel,
.store-panel * {

    font-family:
        'Vazirmatn',
        sans-serif !important;

    direction: rtl !important;

    text-align: center !important;
}


/* =====================================================
   STATUS
   ===================================================== */

.status-box,
.status-box *,
.status-box textarea {

    font-family:
        'Vazirmatn',
        sans-serif !important;

    direction: rtl !important;

    text-align: right !important;
}


/* =====================================================
   GENERATE
   ===================================================== */

.generate-btn {

    font-family:
        'Inter',
        sans-serif !important;

    direction: ltr !important;

    text-align: center !important;

    font-size: 16px !important;

    font-weight: 700 !important;

    min-height: 50px !important;

    margin-top: 20px !important;
}


/* =====================================================
   RESULT VIEWER
   ===================================================== */

.result-viewer {

    width: 100% !important;

    display: flex !important;

    flex-direction: column !important;

    align-items: center !important;

    justify-content: center !important;

    gap: 12px !important;

    margin-top: 16px !important;

    overflow: visible !important;
}


/* =====================================================
   RESULT IMAGE
   ===================================================== */

.result-image {

    width: 100% !important;

    max-width: 700px !important;

    min-height: 400px !important;

    pointer-events: none !important;

    overflow: hidden !important;

    margin: 0 auto !important;
}


/* =====================================================
   RESULT NAVIGATION
   ===================================================== */

.result-navigation {

    width: 100% !important;

    display: flex !important;

    flex-direction: row !important;

    align-items: center !important;

    justify-content: center !important;

    gap: 16px !important;

    margin-top: 8px !important;

    direction: ltr !important;
}


/* =====================================================
   NAVIGATION BUTTONS
   ===================================================== */

.result-nav-button {

    width: 52px !important;

    min-width: 52px !important;

    max-width: 52px !important;

    height: 52px !important;

    min-height: 52px !important;

    border-radius: 50% !important;

    padding: 0 !important;

    font-family:
        'Inter',
        sans-serif !important;

    font-size: 28px !important;

    font-weight: 500 !important;

    direction: ltr !important;

    text-align: center !important;

    display: flex !important;

    align-items: center !important;

    justify-content: center !important;
}


/* =====================================================
   RESULT LABEL
   ===================================================== */

.result-label,
.result-label * {

    font-family:
        'Vazirmatn',
        sans-serif !important;

    direction: rtl !important;

    text-align: center !important;

    font-size: 15px !important;

    font-weight: 600 !important;
}


/* =====================================================
   RESULT COUNTER
   ===================================================== */

.result-counter,
.result-counter * {

    font-family:
        'Vazirmatn',
        sans-serif !important;

    direction: ltr !important;

    text-align: center !important;

    font-size: 14px !important;

    font-weight: 600 !important;

    opacity: 0.7 !important;
}


/* =====================================================
   REMOVE SCROLLBARS
   ===================================================== */

.block,
.column,
.row,
.form,
.result-viewer,
.result-navigation {

    overflow: visible !important;
}


/* =====================================================
   HIDE FOOTER
   ===================================================== */

footer,
.gradio-footer {

    display: none !important;
}


/* =====================================================
   HIDE API / SETTINGS
   ===================================================== */

button[aria-label*="API"],
button[aria-label*="Settings"],
button[title*="API"],
button[title*="Settings"] {

    display: none !important;
}

"""


# =========================================================
# GRADIO APP
# =========================================================

with gr.Blocks(
    title="پرو مجازی لباس"
) as app:

    # =====================================================
    # SESSION STATE
    # =====================================================

    history_state = gr.State([])

    current_index = gr.State(0)


    # =====================================================
    # HEADER
    # =====================================================

    gr.Markdown(
        "پرو مجازی لباس",
        elem_classes=["main-title"]
    )

    gr.Markdown(
        "لباس موردنظر خود را روی تصویر خودتان امتحان کنید",
        elem_classes=["main-subtitle"]
    )


    # =====================================================
    # PERSON
    # =====================================================

    gr.Markdown(
        "👤 تصویر شخص",
        elem_classes=["section-title"]
    )

    gr.Markdown(
        "تصویر شخص را آپلود کنید یا با دوربین عکس بگیرید.",
        elem_classes=["subtitle"]
    )

    person_image = gr.Image(
        label="تصویر شخص",

        type="pil",

        sources=[
            "upload",
            "webcam"
        ],

        show_label=False
    )


    # =====================================================
    # GARMENT
    # =====================================================

    gr.Markdown(
        "👕 انتخاب لباس",
        elem_classes=["section-title"]
    )

    gr.Markdown(
        "هر بار فقط یک تصویر لباس انتخاب کنید.",
        elem_classes=["subtitle"]
    )


    # =====================================================
    # GARMENT BUTTONS
    # =====================================================

    with gr.Row(
        elem_classes=["garment-button-row"]
    ):

        show_store_button = gr.Button(
            "🛍️ نمایش لباس‌های فروشگاه",

            variant="secondary",

            elem_classes=[
                "garment-button"
            ]
        )

        upload_garment_button = gr.Button(
            "📤 آپلود تصویر لباس",

            variant="secondary",

            elem_classes=[
                "garment-button"
            ]
        )


    # =====================================================
    # GARMENT UPLOAD
    # =====================================================

    with gr.Column(
        visible=False,

        elem_classes=[
            "garment-upload-area"
        ]
    ) as garment_upload_area:

        gr.Markdown(
            "📤 تصویر لباس"
        )

        garment_image = gr.Image(
            label="تصویر لباس",

            type="pil",

            sources=[
                "upload"
            ],

            show_label=False
        )


    # =====================================================
    # STORE
    # =====================================================

    with gr.Column(
        visible=False,

        elem_classes=[
            "store-panel"
        ]
    ) as garment_store_area:

        gr.Markdown(
            "🛍️ فروشگاه لباس"
        )

        gr.Markdown(
            "لباس‌های فروشگاه در این بخش نمایش داده خواهند شد."
        )

        gr.Markdown(
            "فروشگاه لباس بعداً به این بخش متصل می‌شود."
        )


    # =====================================================
    # STATUS
    # =====================================================

    status = gr.Textbox(
        label="وضعیت سیستم",

        interactive=False,

        lines=3,

        elem_classes=[
            "status-box"
        ]
    )


    # =====================================================
    # GARMENT BUTTON EVENTS
    # =====================================================

    upload_garment_button.click(
        fn=show_garment_upload,

        inputs=[],

        outputs=[
            garment_upload_area,
            garment_store_area,
            status
        ]
    )


    show_store_button.click(
        fn=show_garment_store,

        inputs=[],

        outputs=[
            garment_upload_area,
            garment_store_area,
            status
        ]
    )


    # =====================================================
    # GENERATE
    # =====================================================

    generate_button = gr.Button(
        "GENERATE ✨",

        variant="primary",

        elem_classes=[
            "generate-btn"
        ]
    )


    # =====================================================
    # RESULTS
    # =====================================================

    gr.Markdown(
        "نتیجه",
        elem_classes=["section-title"]
    )

    gr.Markdown(
        "نتیجه جدید در ابتدا قرار می‌گیرد و با دکمه‌های پایین تصویر بین نتایج جابه‌جا شوید.",
        elem_classes=["subtitle"]
    )


    # =====================================================
    # RESULT VIEWER
    # =====================================================

    with gr.Column(
        elem_classes=[
            "result-viewer"
        ]
    ):

        result_image = gr.Image(
            label="Result",

            type="pil",

            show_label=False,

            interactive=False,

            elem_classes=[
                "result-image"
            ]
        )


        with gr.Row(
            elem_classes=[
                "result-navigation"
            ]
        ):

            previous_button = gr.Button(
                "←",

                variant="secondary",

                elem_classes=[
                    "result-nav-button"
                ]
            )

            next_button = gr.Button(
                "→",

                variant="secondary",

                elem_classes=[
                    "result-nav-button"
                ]
            )


    # =====================================================
    # RESULT LABEL
    # =====================================================

    result_label = gr.Markdown(
        "Original",

        elem_classes=[
            "result-label"
        ]
    )


    # =====================================================
    # RESULT COUNTER
    # =====================================================

    result_counter = gr.Markdown(
        "0 / 0",

        elem_classes=[
            "result-counter"
        ]
    )


    # =====================================================
    # GENERATE EVENT
    # =====================================================

    generate_button.click(

        fn=generate,

        inputs=[
            person_image,
            garment_image,
            history_state
        ],

        outputs=[
            status,
            history_state,
            current_index,
            result_image,
            result_label,
            result_counter
        ]
    )


    # =====================================================
    # PREVIOUS EVENT
    # =====================================================

    previous_button.click(

        fn=previous_result,

        inputs=[
            history_state,
            current_index
        ],

        outputs=[
            current_index,
            result_image,
            result_label,
            result_counter
        ]
    )


    # =====================================================
    # NEXT EVENT
    # =====================================================

    next_button.click(

        fn=next_result,

        inputs=[
            history_state,
            current_index
        ],

        outputs=[
            current_index,
            result_image,
            result_label,
            result_counter
        ]
    )


# =========================================================
# LAUNCH
# =========================================================

if __name__ == "__main__":

    app.launch(
        css=custom_css
    )

