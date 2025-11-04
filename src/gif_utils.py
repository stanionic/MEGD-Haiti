import os
import imageio
from PIL import Image
from flask import current_app

def create_gif_from_images(image_paths, output_path, duration=1.0):
    """
    Create a GIF from a list of image paths.

    :param image_paths: List of paths to images
    :param output_path: Path to save the GIF
    :param duration: Duration between frames in seconds
    :return: Path to the created GIF or None if failed
    """
    try:
        images = []
        for img_path in image_paths:
            if os.path.exists(img_path):
                img = Image.open(img_path)
                # Resize to a consistent size (e.g., 300x300) to avoid issues
                img = img.resize((300, 300), Image.Resampling.LANCZOS)
                images.append(img)
            else:
                print(f"Image not found: {img_path}")
                return None

        if not images:
            print("No images to create GIF")
            return None

        # Save as GIF
        images[0].save(output_path, save_all=True, append_images=images[1:], duration=int(duration * 1000), loop=0)
        print(f"GIF created successfully: {output_path}")
        return output_path
    except Exception as e:
        print(f"Error creating GIF: {str(e)}")
        return None

def get_ad_gif_path(ad_id):
    """
    Get the path for the GIF file for a given ad_id.

    :param ad_id: The ad ID
    :return: Path to the GIF file
    """
    upload_folder = current_app.config['UPLOAD_FOLDER']
    return os.path.join(upload_folder, f"{ad_id}_gif.gif")

def generate_ad_gif(ad):
    """
    Generate a GIF for an ad if it has multiple images.

    :param ad: The Ad object
    :return: Path to the GIF or None
    """
    if ad.media_type != 'images':
        return None

    image_list = ad.images.split(',') if ad.images else []
    if len(image_list) < 2:
        return None  # Need at least 2 images for a GIF

    upload_folder = current_app.config['UPLOAD_FOLDER']
    image_paths = [os.path.join(upload_folder, img.strip()) for img in image_list]

    gif_path = get_ad_gif_path(ad.ad_id)

    # Check if GIF already exists
    if os.path.exists(gif_path):
        return gif_path

    # Create GIF
    return create_gif_from_images(image_paths, gif_path)
