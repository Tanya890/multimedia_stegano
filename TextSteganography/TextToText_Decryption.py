def decode_bit(bit):
    return "0" if bit == "\u200b" else "1"

def TextToText_Decryption(text):
    binary_message = ''.join(decode_bit(i) for i in text if i in ("\u200b", "\u200c"))
    result = "".join(chr(int(binary_message[i:i + 8], 2)) for i in range(0, len(binary_message), 8))
    return result  # Return the hidden message
