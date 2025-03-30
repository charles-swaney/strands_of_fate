import sys
import os

ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC_PATH = os.path.join(ROOT_PATH, "src")

if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)
