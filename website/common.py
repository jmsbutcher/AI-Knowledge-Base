
import os

def get_website_dir():
    dir = os.path.dirname(os.path.abspath(__file__))
    dir = dir.replace("\\\\wsl.localhost\\", "\\\\")
    return dir
