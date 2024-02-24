To build and run the environment for the above program, you will need to install the following Python libraries:

### Installation Guide

You can install these dependencies in your Python environment using the pip command. Open your terminal or command prompt and enter the following commands:

```
pip install Pillow pandas cryptography
```

Ensure your Python environment is already installed and configured. These commands will download and install the latest version of the libraries from the Python Package Index (PyPI).

#### Project Introduction


This project aims to demonstrate how to securely process and encrypt images while preserving data privacy.

The project utilizes the AES encryption algorithm in conjunction with PathORAM, ensuring the security and privacy of image data during loading processes.



#### Run Code

When running the program, you need to change the `input_folder_path` and `encrypted_images_folder` to your own paths. The `input_folder_path` represents the path to the original image dataset, while the `encrypted_images_folder` denotes the path where the encrypted dataset will be stored.

```
input_folder_path = 'D:\\COCO2014new\\test2014' 

encrypted_images_folder = 'D:\\COCO2014new\\test2014cry' 
```



#### Contributions

We welcome contributions of all kinds, whether it's feature improvements, bug fixes, or performance optimizations. Please submit Pull Requests or Issues through GitHub.