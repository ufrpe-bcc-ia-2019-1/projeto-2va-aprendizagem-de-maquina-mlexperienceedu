from preprocess import *
import matplotlib.pyplot as plt
import numpy as np 
noise = [
    '[1-2] Timóteo [1-9].[1-200]',
    'Miquéias 5.2',
    
]
datasets = clean_data(regex=[], names=['guarani'])

save_dataframe(['guarani'], datasets)

bible_1 = pd.read_csv('raw_data/guarani.csv')
bible_2 = pd.read_csv('raw_data/portugues.csv')

data = to_translation_format(bible_1['Scripture'], bible_2['Scripture'])

to_file(data, path='raw_data/gu-pt.txt')

results = obtain_results('test_result.txt', ['acc'])

plt.bar(np.arange(3), height=results['acc'])
plt.xticks(np.arange(3),('Karajá', 'Tukano', 'Guarani'))
plt.show()
score = np.array([])
print(np.var([1, 2, 3], dtype=np.float32, axis=0))