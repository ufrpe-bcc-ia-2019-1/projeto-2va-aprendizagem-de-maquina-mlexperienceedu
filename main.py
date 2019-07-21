from preprocess import *

bible_1 = pd.read_csv('raw_data/tukano.csv')
bible_2 = pd.read_csv('raw_data/portugues.csv')

data = to_translation_format(bible_1['Scripture'], bible_2['Scripture'])

to_file(data, path='raw_data/tu-pt')