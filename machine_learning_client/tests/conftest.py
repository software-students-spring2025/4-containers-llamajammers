# conftest.py - trying to make the ML Client stop failing
import os

os.environ["TORCH_CUDA_DISABLE"] = "1"
os.environ["CUDA_VISIBLE_DEVICES"] = ""
