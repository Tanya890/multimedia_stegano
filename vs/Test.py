import os
from stegano import lsb
import cv2
import math

# Function to split the message into parts
def split_message(message, num_parts):
    part_size = math.ceil(len(message) / num_parts)
    return [message[i:i + part_size] for i in range(0, len(message), part_size)]

# Function to extract frames from a video
def extract_frames(video_path, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    vidcap = cv2.VideoCapture(video_path)
    success, frame = vidcap.read()
    frame_count = 0

    while success:
        frame_path = os.path.join(output_dir, f"frame{frame_count}.png")
        cv2.imwrite(frame_path, frame)
        print(f"[INFO] Extracted frame: {frame_path}")
        success, frame = vidcap.read()
        frame_count += 1

    vidcap.release()
    print(f"[INFO] Total {frame_count} frames extracted.")
    return frame_count

# Function to encode message into frames
def encode_message_in_frames(message, input_frames_dir):
    frames = sorted(os.listdir(input_frames_dir), key=lambda x: int(x.strip('frame.png')))
    message_parts = split_message(message, len(frames))

    for i, part in enumerate(message_parts):
        frame_path = os.path.join(input_frames_dir, f"frame{i}.png")
        try:
            encoded_frame = lsb.hide(frame_path, part)
            encoded_frame.save(frame_path)
            print(f"[INFO] Encoded message part '{part}' in frame {frame_path}")
        except Exception as e:
            print(f"[ERROR] Could not encode frame {frame_path}: {e}")

# Function to combine frames into a video
def frames_to_video(input_frames_dir, output_video_path, fps):
    frames = sorted(os.listdir(input_frames_dir), key=lambda x: int(x.strip('frame.png')))
    if not frames:
        print("[ERROR] No frames found for video creation!")
        return

    first_frame = cv2.imread(os.path.join(input_frames_dir, frames[0]))
    height, width, layers = first_frame.shape
    fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Use AVI for lossless compression
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

    for frame in frames:
        frame_path = os.path.join(input_frames_dir, frame)
        out.write(cv2.imread(frame_path))

    out.release()
    print(f"[INFO] Video saved at {output_video_path}")

# Function to decode the message from frames
def decode_message_from_frames(output_frames_dir, num_encoded_frames):
    frames = sorted(os.listdir(output_frames_dir), key=lambda x: int(x.strip('frame.png')))
    decoded_message = []

    for i in range(num_encoded_frames):
        frame_path = os.path.join(output_frames_dir, f"frame{i}.png")
        try:
            secret = lsb.reveal(frame_path)
            if secret:
                decoded_message.append(secret)
                print(f"[INFO] Decoded message from frame {frame_path}: {secret}")
            else:
                print(f"[WARNING] No message found in frame {frame_path}")
        except Exception as e:
            print(f"[ERROR] Could not decode frame {frame_path}: {e}")

    if decoded_message:
        full_message = ''.join(decoded_message)
        print(f"[SUCCESS] Decoded Message: {full_message}")
        return full_message
    else:
        print("[ERROR] No message decoded. Ensure the video contains hidden data.")
        return None

# Main function
def main():
    action = input("Video Steganography: Encrypt or Decrypt\nEnter 'e' for Encryption or 'd' for Decryption: ")

    if action == 'e':  # Encryption
        input_video = input("Enter the path of the video to encrypt: ")
        input_frames_dir = "./ImageStegano/InputFrames"
        output_video = "./ImageStegano/output_video.avi"
        fps = 30

        # Step 1: Extract frames
        frame_count = extract_frames(input_video, input_frames_dir)

        # Step 2: Encode message
        message = input("Enter the message to encode: ")
        encode_message_in_frames(message, input_frames_dir)

        # Step 3: Combine frames into video
        frames_to_video(input_frames_dir, output_video, fps)
        print(f"[SUCCESS] Video with hidden message saved at {output_video}")

    elif action == 'd':  # Decryption
        input_video = input("Enter the path of the video to decrypt: ")
        output_frames_dir = "./ImageStegano/OutputFrames"

        # Step 1: Extract frames
        frame_count = extract_frames(input_video, output_frames_dir)

        # Step 2: Decode message
        num_encoded_frames = int(input("Enter the number of frames with encoded data: "))
        decode_message_from_frames(output_frames_dir, num_encoded_frames)

    else:
        print("[ERROR] Invalid option. Please enter 'e' or 'd'.")

if __name__ == "__main__":
    main()
