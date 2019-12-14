from util.preprocess import PrepData
import pandas as pd

import os

print(os.listdir('Resources/'))
bible = pd.read_csv('Resources/portugues.csv')
bible_text = bible['Scripture']
