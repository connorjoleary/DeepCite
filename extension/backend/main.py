import claim
import os

CWD_FOLDER = os.path.dirname(os.path.abspath(__file__))

sys.path.append(os.path.abspath("/tokenizer_files/tokenizer.py"))
import tokenizer as token

def main():
    print("Hello, World")
