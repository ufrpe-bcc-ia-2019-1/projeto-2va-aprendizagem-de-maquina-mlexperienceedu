import textwrap
from base64 import encode

from pandas import Index
from util import PrepData
from util import get_noise
from util import align_verses
from itertools import permutations
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import re
import os

# --- Tirando referências -----
path = '../datasets/Full Bible/'
prep = PrepData(path)
#align_verses(prep.get_datasets(), path)
prep.clean_data(get_noise(), True)


path = '../datasets/New Testament/'
prep = PrepData(path)
#align_verses(prep.get_datasets(), path)
prep.clean_data(get_noise(), True)
print('\nFinished !')
