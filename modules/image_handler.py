import base64

def encode_image(image_file):
    try:
        if not image_file:
            print("[❌ No image file provided]")
            return None

        image_file.seek(0)
        img_bytes = image_file.read()

        if not img_bytes:
            print("[❌ Image file empty]")
            return None

        encoded = base64.b64encode(img_bytes).decode("utf-8")
        return encoded

    except Exception as e:
        print(f"[❌ Image encoding error] {e}")
        return None
