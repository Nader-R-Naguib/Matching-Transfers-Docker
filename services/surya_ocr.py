import os
from PIL import Image
from surya.foundation import FoundationPredictor
from surya.detection import DetectionPredictor
from surya.recognition import RecognitionPredictor

DEVICE = "cpu" 

# --- OPTIMIZATION: Load models globally ONCE ---
# This prevents loading 3GB of models into memory for every single screenshot
print("Loading Surya OCR Models into memory (This takes a moment...)")
foundation = FoundationPredictor(device=DEVICE)
det = DetectionPredictor(device=DEVICE)
rec = RecognitionPredictor(foundation)
print("Surya OCR Models loaded successfully.")

def load_image(path: str) -> Image.Image:
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")

    img = Image.open(path)
    img = img.convert("RGB")
    return img

def upscale(img: Image.Image, scale: float = 2.0) -> Image.Image:
    if scale is None or scale <= 1.0:
        return img
    w, h = img.size
    return img.resize((int(w * scale), int(h * scale)), resample=Image.BICUBIC)

def sort_key_textline(text_line) -> float:
    """Sort lines top-to-bottom using min y from polygon."""
    try:
        return min(pt[1] for pt in text_line.polygon)
    except Exception:
        return 0.0

def run_surya_ocr(image_path: str, scale: float = 2.0):
    # 1) Load
    img = load_image(image_path)

    # 2) Upscale
    img = upscale(img, scale=scale)

    # NOTE: img.show() was removed here to prevent crashes on headless servers/Docker

    print("Processing OCR...")
    # 3) Surya expects a list of PIL images (Using global predictors)
    results = rec([img], det_predictor=det)

    if not results:
        return []

    ocr_result = results[0]

    # Extract lines
    text_lines = list(getattr(ocr_result, "text_lines", []) or [])
    if not text_lines:
        return []

    # Sort for nicer reading
    text_lines = sorted(text_lines, key=sort_key_textline)

    extracted = []
    for tl in text_lines:
        txt = (getattr(tl, "text", "") or "").strip()
        if not txt:
            continue
        conf = getattr(tl, "confidence", None)
        poly = getattr(tl, "polygon", None)
        extracted.append((txt, conf, poly))

    return extracted


if __name__ == "__main__":
    # Updated to a generic path for safety
    target_path = "test_image.png"
    if os.path.exists(target_path):
        try:
            out = run_surya_ocr(target_path, scale=2.0)

            print("\n--- EXTRACTED TEXT (Surya) ---")
            if not out:
                print("(No text detected)")
            else:
                for i, (txt, conf, poly) in enumerate(out, 1):
                    conf_str = f"{conf:.3f}" if isinstance(conf, (int, float)) else "N/A"
                    print(f"{i:02d}. [{conf_str}] {txt}")

        except Exception as e:
            print("ERROR:", e)
    else:
        print(f"Please place a '{target_path}' in the root folder to test directly.")