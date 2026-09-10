from pathlib import Path
from PIL import Image, UnidentifiedImageError


class InputManager:
    """
    مدیریت و اعتبارسنجی اولیه ورودی‌های Virtual Try-On.
    """

    # فرمت‌های مجاز تصویر
    ALLOWED_FORMATS = {
        "JPEG",
        "PNG",
        "WEBP",
    }

    # حداقل ابعاد قابل قبول تصویر
    MIN_WIDTH = 256
    MIN_HEIGHT = 256

    # حداکثر حجم فایل: 15 مگابایت
    MAX_FILE_SIZE_MB = 15

    def validate_image(self, image):
        """
        بررسی می‌کند که ورودی یک تصویر معتبر و قابل پردازش باشد.

        ورودی:
            image → تصویر PIL یا مسیر فایل

        خروجی:
            (True, "تصویر معتبر است")
            یا
            (False, "پیام خطا")
        """

        # -----------------------------
        # 1. بررسی وجود ورودی
        # -----------------------------

        if image is None:
            return False, "❌ هیچ تصویری انتخاب نشده است."

        # -----------------------------
        # 2. اگر ورودی مسیر فایل است
        # -----------------------------

        if isinstance(image, (str, Path)):

            image_path = Path(image)

            if not image_path.exists():
                return False, "❌ فایل تصویر پیدا نشد."

            # بررسی حجم فایل
            file_size_mb = image_path.stat().st_size / (1024 * 1024)

            if file_size_mb > self.MAX_FILE_SIZE_MB:
                return False, (
                    f"❌ حجم تصویر بیش از "
                    f"{self.MAX_FILE_SIZE_MB} مگابایت است."
                )

            # تلاش برای باز کردن تصویر
            try:
                with Image.open(image_path) as opened_image:
                    opened_image.verify()

                # دوباره باز می‌کنیم چون verify تصویر را invalidate می‌کند
                with Image.open(image_path) as opened_image:
                    image = opened_image.copy()

            except UnidentifiedImageError:
                return False, "❌ فایل انتخاب‌شده یک تصویر معتبر نیست."

            except Exception:
                return False, "❌ تصویر خراب یا غیرقابل پردازش است."

        # -----------------------------
        # 3. بررسی نوع تصویر
        # -----------------------------

        if not isinstance(image, Image.Image):
            return False, "❌ نوع ورودی تصویر پشتیبانی نمی‌شود."

        # -----------------------------
        # 4. بررسی فرمت تصویر
        # -----------------------------

        image_format = image.format

        if image_format is not None:
            image_format = image_format.upper()

            if image_format not in self.ALLOWED_FORMATS:
                return False, (
                    f"❌ فرمت {image_format} پشتیبانی نمی‌شود. "
                    f"فرمت‌های مجاز: JPEG, PNG, WEBP"
                )

        # -----------------------------
        # 5. بررسی ابعاد
        # -----------------------------

        width, height = image.size

        if width < self.MIN_WIDTH or height < self.MIN_HEIGHT:
            return False, (
                f"❌ ابعاد تصویر خیلی کوچک است. "
                f"حداقل ابعاد موردنیاز "
                f"{self.MIN_WIDTH}×{self.MIN_HEIGHT} پیکسل است."
            )

        # -----------------------------
        # 6. بررسی اینکه تصویر واقعاً قابل خواندن است
        # -----------------------------

        try:
            image.load()

        except Exception:
            return False, "❌ تصویر قابل خواندن نیست یا خراب شده است."

        # -----------------------------
        # 7. همه بررسی‌ها موفق بودند
        # -----------------------------

        return True, "✅ تصویر معتبر و قابل پردازش است."

    def validate_person_image(self, image):
        """
        اعتبارسنجی اولیه تصویر شخص.
        """

        return self.validate_image(image)

    def validate_garment_image(self, image):
        """
        اعتبارسنجی اولیه تصویر لباس.
        """

        return self.validate_image(image)