import argparse
import os
from pbm2bin import convert_file

VERSION = "1.0.1"

def main():
    args = _arg_parser().parse_args()
    file_name, extension = os.path.splitext(args.filename)

    if extension != ".pbm":
        print(f"Error: The file '{args.filename}' is not a .pbm file.")
        return

    file_data = convert_file(args.filename, True, True)

    if file_data is None:
        return # Error message is already printed

    try:
        # Read GTP file and replace image data with new contents
        file_data = replace_file_bytes("image.gtp", 58, file_data)

        with open(file_name + ".gtp", 'wb') as file:
            file.write(file_data)
    except FileNotFoundError as e:
        print(f"{e}")
    except PermissionError:
        print("Error: Permission denied. Cannot write to the file.")
    except OSError as e:
        print(f"An unexpected OS error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def _arg_parser():
    parser = argparse.ArgumentParser(description=f"Portable BitMap to GTP file converter")

    parser.add_argument(
        "--version", action="version", version=f"pbm2gtp v{VERSION}; (c) 2026 Vitomir Spasojević",
    )
    parser.add_argument(
        "filename", type=str, help="PBM file to convert"
    )

    return parser


def replace_file_bytes(filename, offset, new_bytes):
    # Read the file in binary mode
    with open(filename, 'rb') as f:
        file_content = f.read()

    # Calculate checksum (it is sum of new bytes checksum and old checksum)
    checksum = (sum(new_bytes) & 0xFF + (0xFF - int(file_content[-1]))) & 0xFF
    # Replace the image data and a checksum (last byte)
    return file_content[:offset] + new_bytes + file_content[offset + len(new_bytes):-1] + (0xFF - checksum).to_bytes(1, 'little')


if __name__ == "__main__":
    main()