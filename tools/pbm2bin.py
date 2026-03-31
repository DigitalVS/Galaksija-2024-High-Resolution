import argparse
import os
import math

VERSION = "1.0.0"
WhiteChars = {0x09, 0x0A, 0x0D} # White space characters at the end of line: TAB, LF, CR

def main():
    args = _arg_parser().parse_args()
    file_name, extension = os.path.splitext(args.filename)

    if extension != ".pbm":
        print(f"Error: The file '{args.filename}' is not a .pbm file.")
        return

    file_data, width = convert_file(args.filename, args.padding)

    if file_data is None:
        return # Error message is already printed

    try:
        with open(file_name + ".bin", 'wb') as file:
            file.write(file_data)
    except FileNotFoundError:
        print("Error: The file was not found.")
    except PermissionError:
        print("Error: Permission denied. Cannot write to the file.")
    except OSError as e:
        print(f"An unexpected OS error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def _arg_parser():
    parser = argparse.ArgumentParser(description=f"Portable BitMap to binary file converter")

    parser.add_argument(
        "--version", action="version", version=f"pbm2bin v{VERSION}; (c) 2026 Vitomir Spasojević",
    )
    parser.add_argument(
        "-p", "--padding", action="store_false", help="fill the image to full height of 208 pixels at the bottom"
    )
    parser.add_argument(
        "filename", type=str, help="PBM file to convert"
    )

    return parser


def convert_file(filename, padding):
    try:
        with open(filename, 'rb') as file:
            bin_data = bytes()
            bytes_read = file.read(2)
            file_type = bytes_read.decode("utf-8")

            if file_type != "P4":
                print("File type is not raw Portable BitMap file type")
                return None, None

            file.read(1)  # Has to be new line byte
            line = read_line(file) # Read comment line or width and height line if there is no comment line

            if line[0] == 0x23: # 0x23 is ASCII '#' code for comment line beginning
                line = read_line(file) # Read width and height

            size = line.decode("utf-8").split(' ')
            width = int(size[0])
            height = int(size[1])

            for i in range(height): # For each line
                bin_line = file.read(width)

                for byte_value in bin_line:
                    bin_data += reverse_byte(byte_value).to_bytes(1, 'little')

            if padding and height < 208:
                bin_data = extend_bottom(bin_data, height, width)

            return bin_data, width
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
    except (IOError, UnicodeDecodeError):
        print(f"Error reading the file '{filename}'.")
    except PermissionError:
        print("Error: Permission denied. Cannot write to the file.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return None, None

def read_line(file):
    bytes_read = bytes()

    while True:
        one_byte = file.read(1)  # Read a single byte as a bytes object
        if not one_byte:
            break  # End of file (EOF) reached

        byte_value = one_byte[0]  # Get the integer value of the byte
        if byte_value in WhiteChars :  # Read until end of line
            break
        bytes_read = bytes_read + one_byte

    return bytes_read


def extend_bottom(image_bytes, height, width):
    add_length = (208 - height) * (math.ceil(width / 8))
    return image_bytes.rjust(add_length, b'\xFF')


def reverse_byte(b):
    """
    Reverses the bits of a single byte (integer 0-255) using bit manipulation.
    """
    reversed_byte = 0
    for i in range(8):
        reversed_byte <<= 1 # Shift the result left by 1 to make space for the new bit
        reversed_byte |= (b & 1) # Extract the least significant bit of 'b' and add it to the result
        b >>= 1 # Shift 'b' right by 1 to process the next bit
    return reversed_byte


if __name__ == "__main__":
    main()