# ImageAnnotationTool.py

import os
import cv2
import glob

INPUT_IMAGE_FOLDER = "C:/Users/khossain/Downloads/June_17_26/"
OUTPUT_DATASET_FOLDER = "C:/Users/khossain/Downloads/label_images/"

IMG_EXTENSIONS = ["*.jpg", "*.jpeg", "*.png", "*.bmp"]

MAX_DISPLAY_WIDTH = 1200
MAX_DISPLAY_HEIGHT = 800
SAVE_CROP_SIZE = (224, 224)

labels = {
    "h": "Healthy",
    "d": "Disease"
}

os.makedirs(OUTPUT_DATASET_FOLDER, exist_ok=True)
for label_name in labels.values():
    os.makedirs(os.path.join(OUTPUT_DATASET_FOLDER, label_name), exist_ok=True)

drawing = False
ix, iy = -1, -1
current_box_display = None
image_display = None
clone_display = None
scale = 1.0


def resize_for_display(img):
    h, w = img.shape[:2]

    scale_w = MAX_DISPLAY_WIDTH / w
    scale_h = MAX_DISPLAY_HEIGHT / h
    scale_factor = min(scale_w, scale_h, 1.0)

    new_w = int(w * scale_factor)
    new_h = int(h * scale_factor)

    resized = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)
    return resized, scale_factor


def mouse_draw(event, x, y, flags, param):
    global ix, iy, drawing, image_display, clone_display, current_box_display

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
        current_box_display = None

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            image_display = clone_display.copy()
            cv2.rectangle(image_display, (ix, iy), (x, y), (0, 255, 0), 2)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False

        x1, y1 = min(ix, x), min(iy, y)
        x2, y2 = max(ix, x), max(iy, y)

        current_box_display = (x1, y1, x2, y2)

        image_display = clone_display.copy()
        cv2.rectangle(image_display, (x1, y1), (x2, y2), (0, 255, 0), 2)


def save_crop(original_img, box_display, label_name, original_filename, crop_id, scale_factor):
    x1, y1, x2, y2 = box_display

    x1_original = int(x1 / scale_factor)
    y1_original = int(y1 / scale_factor)
    x2_original = int(x2 / scale_factor)
    y2_original = int(y2 / scale_factor)

    if x2_original - x1_original < 10 or y2_original - y1_original < 10:
        print("Selected region too small. Try again.")
        return crop_id

    crop = original_img[y1_original:y2_original, x1_original:x2_original]

    # Resize every crop to same size for AI model
    crop_resized = cv2.resize(crop, SAVE_CROP_SIZE, interpolation=cv2.INTER_AREA)

    label_folder = os.path.join(OUTPUT_DATASET_FOLDER, label_name)
    os.makedirs(label_folder, exist_ok=True)

    base_name = os.path.splitext(os.path.basename(original_filename))[0]
    save_name = f"{base_name}_{label_name}_{crop_id}.jpg"
    save_path = os.path.join(label_folder, save_name)

    cv2.imwrite(save_path, crop_resized)
    print(f"Saved resized crop: {save_path} | Size: {SAVE_CROP_SIZE}")

    return crop_id + 1


def load_all_images(folder):
    image_paths = []
    for ext in IMG_EXTENSIONS:
        image_paths.extend(glob.glob(os.path.join(folder, ext)))
    image_paths.sort()
    return image_paths


def print_instructions():
    print("\n==============================")
    print(" Tomato Dataset Labeling Tool ")
    print("==============================")
    print("Mouse:")
    print("  Draw rectangle around healthy or disease region")
    print("")
    print("Keyboard:")
    print("  h = save crop as Healthy")
    print("  d = save crop as Disease")
    print("  a = add new label/class")
    print("  r = reset current drawing")
    print("  n = next image")
    print("  q = quit")
    print("==============================\n")


image_paths = load_all_images(INPUT_IMAGE_FOLDER)

if len(image_paths) == 0:
    print(f"No images found in folder: {INPUT_IMAGE_FOLDER}")
    exit()

print_instructions()

cv2.namedWindow("Tomato Dataset Labeler", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Tomato Dataset Labeler", MAX_DISPLAY_WIDTH, MAX_DISPLAY_HEIGHT)
cv2.setMouseCallback("Tomato Dataset Labeler", mouse_draw)

crop_counter = 1

for img_path in image_paths:
    original = cv2.imread(img_path)

    if original is None:
        print(f"Could not read image: {img_path}")
        continue

    clone_display, scale = resize_for_display(original)
    image_display = clone_display.copy()
    current_box_display = None

    print(f"\nCurrent image: {img_path}")
    print(f"Display scale: {scale:.3f}")

    while True:
        display = image_display.copy()

        cv2.putText(
            display,
            "Draw box | h=Healthy | d=Disease | a=Add Label | r=Reset | n=Next | q=Quit",
            (20, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 0, 255),
            2
        )

        cv2.imshow("Tomato Dataset Labeler", display)

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            cv2.destroyAllWindows()
            print("Labeling stopped.")
            exit()

        elif key == ord("n"):
            print("Moving to next image.")
            break

        elif key == ord("r"):
            image_display = clone_display.copy()
            current_box_display = None
            print("Drawing reset.")

        elif key == ord("a"):
            new_key = input("Enter keyboard shortcut for new label, example: m: ").strip().lower()
            new_label = input("Enter new label name, example: Severe_Drought: ").strip()

            if new_key and new_label:
                labels[new_key] = new_label
                os.makedirs(os.path.join(OUTPUT_DATASET_FOLDER, new_label), exist_ok=True)
                print(f"Added new label: {new_key} = {new_label}")

        elif key != 255 and chr(key) in labels:
            if current_box_display is None:
                print("No region selected. Draw a box first.")
                continue

            label_name = labels[chr(key)]
            crop_counter = save_crop(
                original,
                current_box_display,
                label_name,
                img_path,
                crop_counter,
                scale
            )

            image_display = clone_display.copy()
            current_box_display = None

cv2.destroyAllWindows()
print("All images finished.")