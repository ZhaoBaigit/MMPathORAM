import os
import random
import math
import time
from PIL import Image
import pandas as pd
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import io
class TreeNode:
    def __init__(self):
        self.data = None
class PathORAM:
    def __init__(self, capacity):
        self.capacity = capacity
        self.tree_depth = math.ceil(math.log2(capacity + 1))
        self.tree_size = 2 ** (self.tree_depth + 1) - 1
        self.tree = [TreeNode() for _ in range(self.tree_size)]
        self.position_map = dict()

    def _get_path(self, leaf):
        path = []
        node_idx = leaf + self.tree_size // 2
        while node_idx >= 0:
            path.append(node_idx)
            node_idx = (node_idx - 1) // 2
        return path

    def _is_leaf(self, idx):
        return idx >= self.tree_size // 2

    def _get_random_leaf(self):
        return random.randint(0, self.capacity - 1)

    def access(self, block_id, new_data=None):
        if block_id not in self.position_map:
            self.position_map[block_id] = self._get_random_leaf()
        leaf = self.position_map[block_id]
        path = self._get_path(leaf)
        retrieved_data = None
        for node_idx in path:
            if self.tree[node_idx].data == block_id:
                retrieved_data = self.tree[node_idx].data
                self.tree[node_idx].data = None
        if new_data is not None:
            retrieved_data = new_data
        new_leaf = self._get_random_leaf()
        self.position_map[block_id] = new_leaf
        new_path = self._get_path(new_leaf)
        for node_idx in new_path:
            if self.tree[node_idx].data is None:
                self.tree[node_idx].data = retrieved_data
                break
        return retrieved_data
def encrypt_image(image_bytes, key):
    iv = os.urandom(16)
    padder = padding.PKCS7(128).padder()  # 128位块大小对应于AES块大小
    padded_data = padder.update(image_bytes) + padder.finalize()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_bytes = encryptor.update(padded_data) + encryptor.finalize()
    return iv + encrypted_bytes  # 返回包含IV的加密数据

def decrypt_image(encrypted_bytes, key):
    iv = encrypted_bytes[:16]
    ct = encrypted_bytes[16:]
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_data = decryptor.update(ct) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()  # 移除填充
    original_data = unpadder.update(padded_data) + unpadder.finalize()
    return original_data

def process_and_encrypt_images(input_folder_path, encrypted_images_folder, oram, key, max_images):
    image_extensions = (".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff")
    processed_images = 0
    for root, dirs, files in os.walk(input_folder_path):
        for file in files:
            if processed_images >= max_images:
                break
            if file.lower().endswith(image_extensions):
                image_path = os.path.join(root, file)
                with Image.open(image_path) as img:
                    img_byte_arr = io.BytesIO()
                    img.save(img_byte_arr, format=img.format)
                    original_data = img_byte_arr.getvalue()
                encrypted_data_with_iv = encrypt_image(original_data, key)
                encrypted_file_name = f"encrypted_{os.path.basename(image_path)}"
                encrypted_file_path = os.path.join(encrypted_images_folder, encrypted_file_name)               
                with open(encrypted_file_path, 'wb') as f:
                    f.write(encrypted_data_with_iv)
                oram.access(encrypted_file_name, encrypted_file_path)
                processed_images += 1

def read_and_reencrypt_images(encrypted_images_folder, oram, key):
    for encrypted_file_name in os.listdir(encrypted_images_folder):
        stored_path = oram.access(encrypted_file_name)
        if stored_path:  
            with open(stored_path, 'rb') as f: 
                file_content = f.read()
                iv = file_content[:16]
                encrypted_data = file_content[16:]
                original_data = decrypt_image(encrypted_data, key, iv)
                reencrypted_data, new_iv = encrypt_image(original_data, key)
                with open(stored_path, 'wb') as f:
                    f.write(new_iv + reencrypted_data)            
            oram.access(encrypted_file_name, stored_path)

def process_images(input_folder_path, encrypted_images_folder, oram, key):
    image_extensions = (".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff")
    for root, _, files in os.walk(input_folder_path):
        for file in files:
            if file.lower().endswith(image_extensions):
                image_path = os.path.join(root, file)
                with Image.open(image_path) as img:
                    img_byte_arr = io.BytesIO()
                    img.save(img_byte_arr, format='JPEG')  
                    original_data = img_byte_arr.getvalue()

                encrypted_data = encrypt_image(original_data, key)
                encrypted_file_name = f"encrypted_{os.path.basename(image_path)}"
                encrypted_file_path = os.path.join(encrypted_images_folder, encrypted_file_name)
                with open(encrypted_file_path, 'wb') as f:
                    f.write(encrypted_data)
                oram.access(encrypted_file_name, encrypted_file_path)


def main():
    input_folder_path = 'D:\\COCO2014new\\test2014' 
    encrypted_images_folder = 'D:\\COCO2014new\\test2014cry'  
    key = os.urandom(32)
    time_records = []
    if not os.path.exists(encrypted_images_folder):
        os.makedirs(encrypted_images_folder)

    for image_count in range(1000, 10001, 1000):
        start_time = time.time()
        oram = PathORAM(image_count)
        process_and_encrypt_images(input_folder_path, encrypted_images_folder, oram, key, max_images=image_count)
        read_and_reencrypt_images(encrypted_images_folder, oram, key)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Processing {image_count} images took {elapsed_time:.2f} seconds.")
        time_records.append({'ImageCount-1': image_count, 'Time': elapsed_time})
    df = pd.DataFrame(time_records)
    df.to_csv("encryption_times.csv", index=False)
if __name__ == "__main__":
    main()
