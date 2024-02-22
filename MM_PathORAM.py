import os
import random
import math
import time
from PIL import Image

start_time = time.time()

class TreeNode:
    def __init__(self):
        self.data = None

class ReadOnlyPathORAM:
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
        return path[::-1]

    def _is_leaf(self, idx):
        return idx >= self.tree_size // 2

    def _get_random_leaf(self):
        return random.randint(0, self.capacity - 1)

    def access(self, file_path):
        leaf = self.position_map.get(file_path, None)
        if leaf is None:  # If file_path is not in position_map, return None
            return None
        path = self._get_path(leaf)

        retrieved_file = None
        for node_idx in path:
            if self.tree[node_idx].data == file_path:
                retrieved_file = self.tree[node_idx].data
                break
        return retrieved_file

def process_image(oram, image_path):
    retrieved_file = oram.access(image_path)
    if retrieved_file:
        with Image.open(retrieved_file) as img:
            pass  # 对图像进行你想要的操作

input_folder_path = 'D:\\COCO2014new\\test2014'  # 替换为你的文件夹路径
image_extensions = (".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff")
image_files = []    #存储每张图片路径
for root, _, files in os.walk(input_folder_path):
    for file in files[:1000]:
        if file.lower().endswith(image_extensions):
            image_path = os.path.join(root, file)
            image_files.append(image_path)

#oram = ReadOnlyPathORAM(len(image_files))
oram = ReadOnlyPathORAM(40775)
# 加载文件路径到PathORAM
for i, file_path in enumerate(image_files):
    leaf = oram._get_random_leaf()
    oram.position_map[file_path] = leaf
    oram.tree[leaf + oram.tree_size // 2].data = file_path

# 直接循环处理每个图像
for image_path in image_files:
    process_image(oram, image_path)

end_time = time.time()
elapsed_time = end_time - start_time

print(f"Program running time: {elapsed_time:.2f} seconds")
