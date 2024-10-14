import heapq
import os
from collections import defaultdict, Counter


# Node class for the Huffman Tree
class Node:
    def __init__(self, char=None, freq=None):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq


# Build frequency dictionary from the text file
def build_frequency(file_path):
    with open(file_path, "r") as file:
        text = file.read()
    return Counter(text)


# Build Huffman Tree from the frequency dictionary
def build_huffman_tree(freq_dict):
    heap = []
    for char, freq in freq_dict.items():
        heapq.heappush(heap, Node(char, freq))

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = Node(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)

    return heapq.heappop(heap)


# Generate Huffman codes from the Huffman Tree
def generate_codes(node, code="", codes={}):
    if node is None:
        return

    if node.char is not None:
        codes[node.char] = code

    generate_codes(node.left, code + "0", codes)
    generate_codes(node.right, code + "1", codes)
    return codes


# Compress the text file and save the binary output
def compress(file_path, output_path, huffman_codes):
    with open(file_path, "r") as file:
        text = file.read()

    encoded_text = "".join([huffman_codes[char] for char in text])

    # Save encoded data as binary
    with open(output_path, "wb") as out_file:
        byte_array = bytearray()
        for i in range(0, len(encoded_text), 8):
            byte = encoded_text[i : i + 8]
            byte_array.append(int(byte, 2))

        out_file.write(byte_array)


# Save the Huffman Tree structure for decompression
def save_huffman_tree(output_path, huffman_tree, freq_dict):
    with open(output_path, "w") as out_file:
        out_file.write(str(freq_dict))


# Read the Huffman Tree structure for decompression
def load_huffman_tree(file_path):
    with open(file_path, "r") as in_file:
        freq_dict = eval(in_file.read())
    return build_huffman_tree(freq_dict)


# Decompress the binary file back to text
def decompress(input_path, output_path, huffman_tree):
    with open(input_path, "rb") as file:
        bit_string = ""
        byte = file.read(1)
        while byte:
            byte = ord(byte)
            bits = bin(byte)[2:].rjust(8, "0")
            bit_string += bits
            byte = file.read(1)

    decoded_text = decode_huffman_data(bit_string, huffman_tree)

    with open(output_path, "w") as out_file:
        out_file.write(decoded_text)


# Decode the bit string using the Huffman Tree
def decode_huffman_data(encoded_data, huffman_tree):
    decoded_text = []
    current_node = huffman_tree

    for bit in encoded_data:
        if bit == "0":
            current_node = current_node.left
        else:
            current_node = current_node.right

        if current_node.char is not None:
            decoded_text.append(current_node.char)
            current_node = huffman_tree

    return "".join(decoded_text)


# Get file size in KB
def get_file_size(file_path):
    return os.path.getsize(file_path) / 1024.0


def huffman_compression(input_file):
    # Step 1: Build frequency dictionary
    freq_dict = build_frequency(input_file)

    huffman_tree = build_huffman_tree(freq_dict)

    huffman_codes = generate_codes(huffman_tree)

    compressed_file = input_file + ".huff"
    compress(input_file, compressed_file, huffman_codes)

    save_huffman_tree(input_file + ".tree", huffman_tree, freq_dict)

    print(f"File '{input_file}' compressed successfully as '{compressed_file}'.")
    return compressed_file


def huffman_decompression(compressed_file, tree_file):
    huffman_tree = load_huffman_tree(tree_file)

    decompressed_file = compressed_file.replace(".huff", "_decompressed.txt")
    decompress(compressed_file, decompressed_file, huffman_tree)

    print(
        f"File '{compressed_file}' decompressed successfully as '{decompressed_file}'."
    )
    return decompressed_file


def main():
    input_file = "Text.txt"
    print(f"Original file size: {get_file_size(input_file):.2f} KB")

    compressed_file = huffman_compression(input_file)
    print(f"Compressed file size: {get_file_size(compressed_file):.2f} KB")

    # Decompress the file
    tree_file = input_file + ".tree"
    decompressed_file = huffman_decompression(compressed_file, tree_file)
    print(f"Decompressed file size: {get_file_size(decompressed_file):.2f} KB")


if __name__ == "__main__":
    main()
