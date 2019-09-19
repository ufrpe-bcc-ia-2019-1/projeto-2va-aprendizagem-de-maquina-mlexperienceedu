import textwrap
from base64 import encode

from pandas import Index
from util import PrepData
from util import align_verses
from itertools import permutations
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import re
import os

# --- Tirando referências -----

path = '../datasets/Novo Testamento/'

prep = PrepData(path)
bibles = prep.get_datasets()
align_verses(bibles, path)

prep.clear_data(prep.get_noise(), True)
