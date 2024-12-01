# Correcting import paths based on the new folder structure
from TextSteganography.Main import main as text_steg_main
from vs.Test import main as video_steg_main

def main():
    print("Welcome to the Steganography Tool!")
    print("Choose an option:")
    print("1: Text Steganography")
    print("2: Video Steganography")
    
    choice = input("Enter your choice (1 or 2): ")
    
    if choice == '1':
        print("\n--- Text Steganography ---")
        text_steg_main()  # Calls the main function of Text Steganography module
    elif choice == '2':
        print("\n--- Video Steganography ---")
        video_steg_main()  # Calls the main function of Video Steganography module
    else:
        print("[ERROR] Invalid choice! Please select either 1 or 2.")

if __name__ == "__main__":
    main()
