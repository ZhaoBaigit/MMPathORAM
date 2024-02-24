import os
import random
import math
import time
from PIL import Image
import pandas as pd
start_time = time.time()

class TreeNode:
    def __init__(self):
        self.blocks = [{'data': None, 'is_dummy': True} for _ in range(4)]

class MM_PathORAM:
    def __init__(self, capacity):
        self.capacity = capacity
        self.tree_depth = math.ceil(math.log2(capacity + 1))
        self.tree_size = 2 ** (self.tree_depth + 1) - 1
        self.tree = [TreeNode() for _ in range(self.tree_size)]
        self.position_map = {}  

    def _get_path(self, leaf):
        path = []
        node_idx = leaf + self.tree_size // 2
        while node_idx >= 0:
            path.append(node_idx)
            node_idx = (node_idx - 1) // 2
        return path[::-1]

    def _get_random_leaf(self):
        return random.randint(0, self.capacity - 1)

    def access(self, file_path):
        position_info = self.position_map.get(file_path, None)
        if position_info is None:
            return None
        leaf, real_block_index = position_info
        path = self._get_path(leaf)
        retrieved_file = None
        for node_idx in path:
            node = self.tree[node_idx]

            for block in node.blocks:
                if block['data'] == file_path and not block['is_dummy']:
                    retrieved_file = block['data']
        return retrieved_file

def process_image(oram, image_path):
    retrieved_file = oram.access(image_path)
    if retrieved_file:
        with Image.open(retrieved_file) as img:
            Image.open(retrieved_file)
def main():
    input_folder_path = 'D:\\COCO2014new\\test2014'   
    image_extensions = (".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff")
    time_records = []
    for num_images in range(1000, 10001, 1000):
        start_time = time.time()
        image_files = []
        for root, _, files in os.walk(input_folder_path):
            for file in files[:num_images]:
                if file.lower().endswith(image_extensions):
                    image_path = os.path.join(root, file)
                    image_files.append(image_path)

        oram = MM_PathORAM(len(image_files))
        for file_path in image_files:
            leaf = oram._get_random_leaf()
            node = oram.tree[leaf + oram.tree_size // 2]
            real_block_index = random.randint(0, 3)
            for i in range(4):
                if i == real_block_index:
                    node.blocks[i] = {'data': file_path, 'is_dummy': False}
                else:
                    node.blocks[i]['is_dummy'] = True  
            oram.position_map[file_path] = (leaf, real_block_index)
        for image_path in image_files:
            process_image(oram, image_path)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Program running time: {elapsed_time:.2f} seconds")
        time_records.append({'ImageCount': num_images, 'Time': elapsed_time})
    df = pd.DataFrame(time_records)
    df.to_csv("MM_PathORAMtimes.csv", index=False)

if __name__ == "__main__":
    main()