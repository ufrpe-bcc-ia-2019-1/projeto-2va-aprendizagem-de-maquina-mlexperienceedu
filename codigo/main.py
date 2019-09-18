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

data_list = os.listdir(path)

prep = PrepData(data_list)
prep.set_prefix(path)
# prep.set_sufix('.csv')


# prep.save_all_datasets()
pairs = permutations(data_list, 2)

# data_pairs = prep.to_pair_format(pairs)
pd.set_option('display.max_colwidth', -1)
bibles = {}

for b in data_list:
    bibles[b] = pd.read_csv(path + b, encoding="utf-8").drop_duplicates().reset_index(drop=True)

new_bibles = {}.fromkeys(data_list)


def collapse_verses(bibles, ref, verses_seq):
    path = '../datasets/Bíblia Completa/'
    for key, bible in zip(bibles.keys(), bibles.values()):
        script_seq = []
        for v_seq in verses_seq:
            verse_1 = bible.loc[
                (bible['Book'] == ref['Book']) &
                (bible['Chapter'] == ref['Chapter']) &
                (bible['Verse'] == v_seq)
                ]['Scripture'].to_string()

            verse_1 = ' '.join(verse_1.split())
            script_seq.append(verse_1)

        new_verse = ' '.join(script_seq)

        bible.replace(to_replace=script_seq[0], value=new_verse, regex=True, inplace=True)

        bible.to_csv(path + key, index=False)

        return bibles


file = open('collapsed.txt', 'w', encoding='utf-8')

for k, b in zip(bibles.keys(), bibles.values()):

    scrip = b['Scripture']
    file.write(k + '\n')
    for verse in scrip:
        search = re.search(r'(?<=(<sup>))[(][0-9]*[-][0-9]*[)]', verse)

        try:
            if search is not None:
                first = re.search(r'(?<=([(]))[0-9]*', search.group(0)).group(0)
                last = re.search(r'(?<=([-]))[0-9]*', search.group(0)).group(0)
                verses = np.arange(int(first), int(last))
                ind = Index(scrip).get_loc(verse)
                reference = b.loc[ind, :]
                print(reference)
                file.write(reference.to_string() + '\n')

                collapse_verses(bibles, reference, verses)

        except AttributeError:

            try:
                search = re.search(r'((?<=[(]\s))[0-9]*', verse)

                if search is not None:
                    print(verse)
                    first = search.group(0)
                    last = re.search(r'(?<=([-]\s))[0-9]*', verse)
                    if last is not None:
                        last = last.group(0)
                        verses = np.arange(int(first), int(last))
                        ind = b.loc[b['Scripture'] == verse].index.values.astype(int)[0]
                        print(ind)
                        reference = b.loc[ind, :]
                        print(reference)
                        file.write(reference.to_string())
                        bibles = collapse_verses(bibles, reference, verses)
            except Exception:
                file.write(Exception.__traceback__.__str__())

file.close()

noise = get_noise()
datasets = prep.clean_data(noise)

for k, b in zip(datasets.keys(), datasets.values()):
    b.to_csv(path + k, index=False)
