from PIL import Image
from cryptography.fernet import Fernet

# Steganography Class: Uses OOP for better structure
class Steganography:
    def __init__(self, key=None):
        if key is None:
            self.key = Fernet.generate_key()
        else:
            self.key = key
        self.cipher = Fernet(self.key)
    
    # Convert message to binary
    @staticmethod
    def _message_to_bin(message):
        return ''.join([format(ord(char), '08b') for char in message])
    
    # Convert binary data to message
    @staticmethod
    def _bin_to_message(binary_data):
        all_bytes = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
        decoded_message = ''.join([chr(int(byte, 2)) for byte in all_bytes])
        return decoded_message
    
    # Encrypt the message using Fernet symmetric encryption
    def _encrypt_message(self, message):
        return self.cipher.encrypt(message.encode())

    # Decrypt the message using Fernet symmetric encryption
    def _decrypt_message(self, encrypted_message):
        return self.cipher.decrypt(encrypted_message).decode()

    # Embed the encrypted message into the image
    def hide_message(self, image_path, message, output_path):
        # Open the image
        image = Image.open(image_path)
        image_data = list(image.getdata())
        
        # Encrypt and then convert the message to binary
        encrypted_message = self._encrypt_message(message)
        message_bin = self._message_to_bin(encrypted_message.decode('utf-8')) + '1111111111111110'  # Delimiter

        # Embed the binary data into the image
        message_index = 0
        for i in range(len(image_data)):
            if message_index < len(message_bin):
                pixel = list(image_data[i])
                for j in range(3):  # Iterate over RGB values
                    if message_index < len(message_bin):
                        pixel[j] = (pixel[j] & ~1) | int(message_bin[message_index])
                        message_index += 1
                image_data[i] = tuple(pixel)
            else:
                break
        
        # Save the modified image
        image.putdata(image_data)
        image.save(output_path)
        print("Message hidden successfully in", output_path)

    # Extract the hidden message from the image
    def retrieve_message(self, image_path):
        image = Image.open(image_path)
        image_data = list(image.getdata())

        binary_data = ""
        for pixel in image_data:
            for color in pixel[:3]:  # Only take RGB values
                binary_data += str(color & 1)

        # Extract the binary message up to the delimiter
        delimiter = '1111111111111110'
        encrypted_message_bin = binary_data.split(delimiter)[0]

        # Convert binary to encrypted string and decrypt the message
        encrypted_message = self._bin_to_message(encrypted_message_bin)
        return self._decrypt_message(encrypted_message.encode('utf-8'))

# Usage Example:
if __name__ == "__main__":
    # Create a Steganography object with encryption
    steg = Steganography()

    # Image and message details
    image_path = "input_image.png"  # Input image
    output_path = "output_image.png"  # Output image
    message = "Confidential message for steganography"  # Message to hide

    # Hide the message in the image
    steg.hide_message(image_path, message, output_path)
    
    # Retrieve the hidden message
    hidden_message = steg.retrieve_message(output_path)
    print("Retrieved Message:", hidden_message)
    print("Encryption Key (Save this!):", steg.key.decode())

