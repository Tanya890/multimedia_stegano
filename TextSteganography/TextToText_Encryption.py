def encode_bit(bit):
    return "\u200b" if bit == "0" else "\u200c"

def TextToText_Encryption(text, message):
    binary_message = "".join(format(ord(i), "08b") for i in message)
    midpoint = len(text) // 2

    # Ensure the cover text is long enough
    if len(text) < len(binary_message):
        print("Error: Cover text too short to hide the message.")
        return

    hidden_message = ''.join(encode_bit(bit) for bit in binary_message)
    print(text[:midpoint] + hidden_message + text[midpoint:])
