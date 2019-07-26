from preprocess import *
import matplotlib.pyplot as plt
import numpy as np 

bible_1 = pd.read_csv('raw_data/guarani.csv')
bible_2 = pd.read_csv('raw_data/portugues.csv')

data = to_translation_format(bible_1['Scripture'], bible_2['Scripture'])

to_file(data, path='raw_data/gu-pt.txt')

results = obtain_results('test_result.txt', ['acc'])

plt.bar(np.arange(3), height=results['acc'])
plt.xticks(np.arange(3),('Karajá', 'Tukano', 'Guarani'))
plt.show()