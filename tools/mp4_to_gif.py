import os
from moviepy import VideoFileClip
from PIL import Image
from tqdm import tqdm  # To display progress
import numpy as np

def plot_video_to_gif(video_folder, speed=5, resize_factor=0.5):
    # Walk through all files in the directory and its subdirectories
    for root, _, files in os.walk(video_folder):
        # Process each .mp4 file in the folder
        for video in tqdm([file for file in files if file.endswith(".mp4")], desc=f"Processing folder {root}", unit="video"):
            video_path = os.path.join(root, video)
            gif_output_path = os.path.join(root, os.path.splitext(video)[0] + ".gif")  # Same name, different extension

            # Process the video file and create a GIF
            create_gif_from_video(video_path, gif_output_path, speed, resize_factor)

def create_gif_from_video(video_path, output_gif, speed=5, resize_factor=0.5):
    frames = []
    
    with VideoFileClip(video_path) as clip:
        # Extract frames at a reduced speed (frame rate adjusted by speed)
        frame_rate = clip.fps / speed
        for t in np.arange(0, clip.duration, 1 / frame_rate):  # Extract frames at intervals
            frame = clip.get_frame(t)
            img = Image.fromarray(frame)  # Convert frame to PIL Image

            # Resize the image to make the GIF smaller
            if resize_factor != 1:
                img = img.resize((int(img.width * resize_factor), int(img.height * resize_factor)))

            frames.append(img)
    
    # Save the frames as a GIF with adjusted duration and loop
    frames[0].save(output_gif, save_all=True, append_images=frames[1:], duration=1000 // speed, loop=0)
    
    print(f"GIF file {output_gif} created successfully!")

# Usage example:
plot_video_to_gif(r"C:\Users\Lenovo\Desktop\v2xscenes.github.io-main\v2xscenes.github.io-main\static\videos", speed=3.5, resize_factor=1)

