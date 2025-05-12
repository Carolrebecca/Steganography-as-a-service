from PIL import Image

# Binary end marker (8 bits = 1 byte)
END_MARKER = '11111110'

def encode_message(image_path, message, output_path):
    img = Image.open(image_path)
    img = img.convert('RGB')
    data = list(img.getdata())

    binary_message = ''.join(format(ord(char), '08b') for char in message)
    binary_message += END_MARKER  # append end marker

    new_data = []
    message_index = 0

    for pixel in data:
        r, g, b = pixel
        if message_index < len(binary_message):
            r = (r & ~1) | int(binary_message[message_index])
            message_index += 1
        if message_index < len(binary_message):
            g = (g & ~1) | int(binary_message[message_index])
            message_index += 1
        if message_index < len(binary_message):
            b = (b & ~1) | int(binary_message[message_index])
            message_index += 1
        new_data.append((r, g, b))

    img.putdata(new_data)
    img.save(output_path)

def decode_message(image_path):
    img = Image.open(image_path)
    img = img.convert('RGB')
    data = list(img.getdata())

    binary_message = ''
    for pixel in data:
        for color in pixel[:3]:
            binary_message += str(color & 1)

    message = ''
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i+8]
        if byte == END_MARKER:
            break
        message += chr(int(byte, 2))

    return message
