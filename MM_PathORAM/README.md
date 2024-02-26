To build and run the environment for the above program, you will need to install the following Python libraries:

### Installation Guide

You can install these dependencies in your Python environment using the pip command. Open your terminal or command prompt and enter the following commands:

```
pip install Pillow pandas
```

Ensure your Python environment is already installed and configured. These commands will download and install the latest version of the libraries from the Python Package Index (PyPI).

#### Project Introduction

This project employs the MM_PathORAM algorithm to load image data. We conducted tests to load 1,000, 2,000,... up to 10,000 images from the COCO datasets. The time taken to load the data is recorded in the "MM_PathORAMtimes.csv" file.


#### Run Code

When running the program, you need to change the `input_folder_path`  to your own paths. The `input_folder_path` represents the path to the original image dataset.

```
input_folder_path = 'yourdatapath' 
```



#### Contributions

We welcome contributions of all kinds, whether it's feature improvements, bug fixes, or performance optimizations. Please submit Pull Requests or Issues through GitHub.