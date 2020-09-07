import cv2

###############################################################################
# Text and Binary Conversion
###############################################################################
def text2binary(text):
    return ''.join([ format(ord(c), "08b") for c in text ])

def binary2text(binary):
    # Pad binary until it is multiple of 8
    if len(binary) % 8 > 0: binary += "0" * (8 - len(binary) % 8)
    # Convert binary to bytes
    binary = int(binary, 2)
    text = binary.to_bytes((binary.bit_length() + 7) // 8, "big")
    # Decode bytes to text
    return text.decode(encoding="ascii", errors="ignore")

###############################################################################
# Image Steganography
###############################################################################

# Hides message into image
# imageFile: filepath to image
# textFile: filepath to text message
# bit: Position of byte to hide data. 0(LSB) 7(MSB)
# r,g,b: Uses the channel if set to True
def hide(imagefile, textfile, bit=0, r=True, g=True, b=True):
    # Read image
    image = cv2.imread(imagefile)
    height, width = image.shape[:2]
    # Read text file
    file = open(textfile, "r")
    text = file.read()
    # Encode message to binary
    binary = text2binary(text)
    # Message pointer
    i = 0
    # Convert bit mask
    mask = 1 << bit
    # Iterate each pixel in the image
    for h in range(height):
        for w in range(width):
            # Get value of pixels
            pixel = image[h][w]
            # Hide data in LSB
            if i < len(binary) and r:
                pixel[0] = (pixel[0] & ~mask) | (int(binary[i]) << bit)
                i += 1
            if i < len(binary) and g:
                pixel[1] = (pixel[1] & ~mask) | (int(binary[i]) << bit)
                i += 1
            if i < len(binary) and b:
                pixel[2] = (pixel[2] & ~mask) | (int(binary[i]) << bit)
                i += 1
    # Output image
    cv2.imwrite("output.png", image)

# Extract message from image
# imageFile: filepath to image
# bit: Position of byte to extract data. 0(LSB) 7(MSB)
# r,g,b: Uses the channel if set to True
def show(filename, bit=0, r=True, g=True, b=True):
    # Read image
    image = cv2.imread(filename)
    height, width = image.shape[:2]
    # Binary string
    binary = ""
    # Iterate each pixel in the image
    for h in range(height):
        for w in range(width):
            # Get value of pixel
            pixel = image[h][w]
            # Extract bits
            if r: binary += str((pixel[0] >> bit) % 2)
            if g: binary += str((pixel[1] >> bit) % 2)
            if b: binary += str((pixel[2] >> bit) % 2)
    # Convert binary to text
    text = binary2text(binary)
    print(text)

def main():

    # Hide secret message rgb,lsb,xy
    hide("image.png", "secret.txt")
    # Extract hidden data
    show("output.png")


if __name__ == '__main__':
    main()
