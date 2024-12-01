from Encryption import encryption
from Decryption import decryption
from TextToText_Encryption import TextToText_Encryption
from TextToText_Decryption import TextToText_Decryption

def main():
    print("Choose an option:")
    print("1: Caesar Cipher Encryption")
    print("2: Caesar Cipher Decryption")
    print("3: Text-to-Text Steganography Encryption (with optional Caesar Encryption)")
    print("4: Text-to-Text Steganography Decryption (with optional Caesar Decryption)")
    
    option = int(input("Enter your choice: "))
    
    if option == 1:
        key = int(input("Enter the key for encryption: "))
        message = input("Enter the message to encrypt: ")
        encryption(key, message)  # Call the encryption function
    
    elif option == 2:
        key = int(input("Enter the key for decryption: "))
        message = input("Enter the message to decrypt: ")
        decryption(key, message)  # Call the decryption function
    
    elif option == 3:  # Encrypt and hide
        cover_text = input("Enter the cover text: ")
        message = input("Enter the message to hide: ")
        key = int(input("Enter the key for encryption (or 0 to skip encryption): "))
        
        # Encrypt the message if key is not 0
        if key != 0:
            encrypted_message = ''.join(chr((ord(i) + key - 32) % 95 + 32) for i in message)
            print(f"Encrypted message: {encrypted_message}")
        else:
            encrypted_message = message
        
        # Now hide the encrypted message
        TextToText_Encryption(cover_text, encrypted_message)
    
    elif option == 4:  # Extract and decrypt
        encoded_text = input("Enter the encoded text: ")
        key = int(input("Enter the key for decryption (or 0 to skip decryption): "))
        
        # Extract hidden message first
        print("Extracting hidden message...")
        hidden_message = TextToText_Decryption(encoded_text)
        
        # Decrypt the message if key is not 0
        if key != 0:
            decrypted_message = ''.join(chr((ord(i) - key - 32) % 95 + 32) for i in hidden_message)
            print(f"Decrypted message: {decrypted_message}")
        else:
            print(f"Extracted message: {hidden_message}")
    
    else:
        print("Invalid option! Please select a valid choice.")

if __name__ == "__main__":
    main()
