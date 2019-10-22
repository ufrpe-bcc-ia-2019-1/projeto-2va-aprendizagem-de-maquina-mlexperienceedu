from util.preprocess import PrepData
import pandas as pd

import os

print(os.listdir('datasets/'))
bible = pd.read_csv('datasets/portugues.csv')
bible_text = bible['Scripture']
