import textwrap
from base64 import encode

from pandas import Index
from util import PrepData

from itertools import permutations
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import re
import os

# --- Tirando referências -----
path = '../datasets/New Testament/'
prep = PrepData(path)
#align_verses(prep.get_datasets(), path)
#prep.clean_data(get_noise(), True)


datasets = prep.get_datasets()
prep.get_text_pairs()
prep.set_root_dir('../datasets/pairs/')
prep.save_pairs('.txt')


#align_verses(prep.get_datasets(), path)
#prep.clean_data(get_noise(), True)
#print('\nFinished !')


