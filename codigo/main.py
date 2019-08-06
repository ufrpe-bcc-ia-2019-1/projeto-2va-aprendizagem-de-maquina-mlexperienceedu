from util import prepData
import matplotlib.pyplot as plt
import numpy as np 

noise = [
    '[1-2] Timóteo [1-150].[1-200]',
    'Miquéias [1-150].[1-200]',
]

prep = prepData(['guarani', 'karaja', 'xavante', 'tukano','portugues'])

prep.set_prefix('raw_data/')
prep.set_sufix('.csv')

datasets = prep.clean_data(regex=noise)

pair = prep.to_pair_format(datasets['portugues'], datasets['guarani'], 'Scripture')

prep.save_all_datasets()