# Importing main functions from respective modules
from TextSteganography.Main import main as text_steg_main
from vs.Test import main as video_steg_main
from AudioStegano.audiostegnography import main as audio_steg_main
from ImageStegano.Imagesteagno import main as image_steg_main

def main():
    print("Welcome to the Steganography Tool!")
    print("Choose an option:")
    print("1: Text Steganography")
    print("2: Video Steganography")
    print("3: Audio Steganography")
    print("4: Image Steganography")
    
    choice = input("Enter your choice (1, 2, 3, or 4): ")
    
    if choice == '1':
        print("\n--- Text Steganography ---")
        text_steg_main()  # Calls the main function of Text Steganography module
    elif choice == '2':
        print("\n--- Video Steganography ---")
        video_steg_main()  # Calls the main function of Video Steganography module
    elif choice == '3':
        print("\n--- Audio Steganography ---")
        audio_steg_main()  # Calls the main function of Audio Steganography module
    elif choice == '4':
        print("\n--- Image Steganography ---")
        image_steg_main()  # Calls the main function of Image Steganography module
    else:
        print("[ERROR] Invalid choice! Please select either 1, 2, 3, or 4.")

if __name__ == "__main__":
    main()
