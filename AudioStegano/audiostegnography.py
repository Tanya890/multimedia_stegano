import wave
from cryptography.fernet import Fernet

# Audio Steganography Class
class AudioSteganography:
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
    
    # Encrypt the message using Fernet encryption
    def _encrypt_message(self, message):
        return self.cipher.encrypt(message.encode())

    # Decrypt the message using Fernet encryption
    def _decrypt_message(self, encrypted_message):
        return self.cipher.decrypt(encrypted_message).decode()

    # Hide encrypted message in audio file
    def hide_message(self, audio_path, message, output_path):
        # Encrypt the message and convert to binary
        encrypted_message = self._encrypt_message(message)
        message_bin = self._message_to_bin(encrypted_message.decode('utf-8')) + '1111111111111110'  # Delimiter
        
        # Open the audio file
        audio = wave.open(audio_path, mode='rb')
        frame_bytes = bytearray(list(audio.readframes(audio.getnframes())))
        
        # Embed binary message into least significant bits of audio data
        message_index = 0
        for i in range(len(frame_bytes)):
            if message_index < len(message_bin):
                frame_bytes[i] = (frame_bytes[i] & ~1) | int(message_bin[message_index])
                message_index += 1
            else:
                break

        # Write the modified bytes to a new audio file
        modified_audio = wave.open(output_path, 'wb')
        modified_audio.setparams(audio.getparams())
        modified_audio.writeframes(bytes(frame_bytes))
        modified_audio.close()
        audio.close()
        print(f"Message hidden successfully in {output_path}")

    # Extract hidden message from audio file
    def retrieve_message(self, audio_path):
        audio = wave.open(audio_path, mode='rb')
        frame_bytes = bytearray(list(audio.readframes(audio.getnframes())))
        
        binary_data = ""
        for byte in frame_bytes:
            binary_data += str(byte & 1)

        # Extract binary message up to the delimiter
        delimiter = '1111111111111110'
        encrypted_message_bin = binary_data.split(delimiter)[0]

        # Convert binary to encrypted string and decrypt the message
        encrypted_message = self._bin_to_message(encrypted_message_bin)
        return self._decrypt_message(encrypted_message.encode('utf-8'))

# Usage Example:
def main():
    # Create an AudioSteganography object with encryption
    audio_steg = AudioSteganography()

    # Audio and message details
    audio_path = r"C:\Users\anike\Desktop\multimedia_stegano-1\AudioStegano\input_audio.wav"
    output_path = r"C:\Users\anike\Desktop\multimedia_stegano-1\AudioStegano\output_audio.wav"

    message = "Secret message hidden in audio"  # Message to hide

    # Hide the message in the audio file
    audio_steg.hide_message(audio_path, message, output_path)

    # Retrieve the hidden message
    hidden_message = audio_steg.retrieve_message(output_path)
    print("Retrieved Message:", hidden_message)
    print("Encryption Key (Save this!):", audio_steg.key.decode())
if __name__ == "__main__":
    main()
