
import sys
from os.path import abspath,dirname

PARENT_PATH = dirname(dirname(abspath(__file__)))
sys.path.append(PARENT_PATH)