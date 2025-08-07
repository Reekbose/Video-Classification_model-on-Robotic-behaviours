import os
import cv2
import numpy as np
from glob import glob


def create_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def clean_name(video_path):
    name = os.path.basename(video_path)
    name = os.path.splitext(name)[0]  # Removes extension like .mp4, .avi
    return name


def save_fixed_frames(video_path, output_base_dir, target_frames=20):
    """
    Extract all frames from a video and save to a separate folder.
    """
    folder_name = clean_name(video_path)
    save_path = os.path.join(output_base_dir, folder_name)
    create_dir(save_path)

    print(f"Created/using folder: {save_path}")

    cap = cv2.VideoCapture(video_path)
    
    # Check if video opened successfully
    if not cap.isOpened():
        print(f"Error: Cannot open video file {video_path}")
        return
    
   
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count / fps if fps > 0 else 0
    
    print(f"Video info: {frame_count} frames, {fps:.2f} FPS, {duration:.2f}s")
    
    frames = []

    # Reading all frames from the video
    frame_number = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
        frame_number += 1
        
        # Progress indicator for long videos
        if frame_number % 100 == 0:
            print(f"Read {frame_number} frames...")

    cap.release()

    total_frames = len(frames)
    print(f"Successfully read {total_frames} frames")

    # Skip empty videos
    if total_frames == 0:
        print(f"Skipping {folder_name}: No frames found.")
        return

    # Sampling or Padding
    if total_frames >= target_frames:
        indices = np.linspace(0, total_frames - 1, target_frames, dtype=int)
        selected_frames = [frames[i] for i in indices]
        print(f"Sampled {target_frames} frames from {total_frames}")
    else:
        selected_frames = frames[:]
        last_frame = frames[-1]
        while len(selected_frames) < target_frames:
            selected_frames.append(last_frame)
        print(f"Padded to {target_frames} frames (original: {total_frames})")

    #Save frames
    saved_count = 0
    for i, frame in enumerate(selected_frames):
        frame_filename = os.path.join(save_path, f"{i:03d}.png")
        success = cv2.imwrite(frame_filename, frame)
        if success:
            saved_count += 1
        else:
            print(f"Failed to save frame {i}")

    print(f"{folder_name}: saved {saved_count}/{len(selected_frames)} frames")


if __name__ == "__main__":
    video_directory = r"D:\Desktop\Internship\Research Paper\Robot dataset\train"

    output_directory = r"D:\Desktop\Internship\Research Paper\Robot dataset\save"

    if not os.path.exists(video_directory):
        print(f"Video directory does not exist: {video_directory}")
        exit()

    video_extensions = ['*.mp4', '*.avi', '*.mov', '*.mkv', '*.wmv', '*.flv', '*.webm']
    video_files = []
    
    for ext in video_extensions:
        video_files.extend(glob(os.path.join(video_directory, ext)))
        video_files.extend(glob(os.path.join(video_directory, ext.upper())))

    print(f"Looking in directory: {video_directory}")
    print(f"Found {len(video_files)} videos.")
    
    if len(video_files) == 0:
        print("No video files found! Check:")
        print("  1. Directory path is correct")
        print("  2. Video files have supported extensions (.mp4, .avi, .mov, etc.)")
        print("  3. Files are directly in the directory (not in subdirectories)")
        
        # List all files in directory for debugging
        all_files = glob(os.path.join(video_directory, "*"))
        print(f"\nAll files in directory ({len(all_files)}):")
        for file in all_files[:10]:  # Show first 10 files
            print(f"  - {os.path.basename(file)}")
        if len(all_files) > 10:
            print(f"  ... and {len(all_files) - 10} more files")
    else:
        print("\nVideo files found:")
        for video_file in video_files:
            print(f"  - {os.path.basename(video_file)}")
        
        print(f"\nStarting frame extraction...")
        for video_file in video_files:
            print(f"\nProcessing: {os.path.basename(video_file)}")
            save_fixed_frames(video_file, output_directory, target_frames=20)