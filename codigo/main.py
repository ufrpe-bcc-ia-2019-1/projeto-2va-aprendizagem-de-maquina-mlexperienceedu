import textwrap
from base64 import encode

from pandas import Index
from util import PrepData
from util import get_noise
from itertools import permutations
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import re
import os

# --- Tirando referências -----

path = '../datasets/Bíblia Completa/'

text = open('../datasets/pairs/(\'Português - Bíblia Completa.csv\', \'Guarani Mbyá - Bíblia Completa.csv\').txt', 'r', encoding='utf-8')

file = open('gu-pt.txt', 'w', encoding='utf-8')
for line in text:
    line = re.sub(r'[0-9]*[-][0-9]*[;]*', '', line)
    file.write(line)
file.close()
