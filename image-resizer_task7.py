import os
from PIL import Image

input_folder = r'E:\VS\Python\Internship_elevate_labs_python\Image_resizer\images-resize'
output_folder = r'E:\VS\Python\Internship_elevate_labs_python\Image_resizer\images-output'
target_size = (800, 600)  # 📏 Desired size (width, height)

os.makedirs(output_folder, exist_ok=True)


for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)


        with Image.open(input_path) as img:
            resized_img = img.resize(target_size, Image.LANCZOS)
            resized_img.save(output_path)

print("✅ All images resized and saved to:", output_folder)