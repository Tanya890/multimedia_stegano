def encryption(key, message):
    print("Result: ", end='')
    for i in str(message):
        new_char = chr((ord(i) + key - 32) % 95 + 32)  # Keeps within printable ASCII range (32-126)
        print(new_char, end='')
    print()  # To ensure proper newline after result
