import textwrap

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
    bibles[b] = pd.read_csv(path + b, encoding="utf-8")

new_bibles = {}.fromkeys(data_list)


def collapse_verses(bibles, ref):
    path = '../datasets/Bíblia Completa/'
    for key, bible in zip(bibles.keys(), bibles.values()):
        verse_1 = bible.loc[
            (bible['Book'] == ref['Book']) &
            (bible['Chapter'] == ref['Chapter']) &
            (bible['Verse'] == ref['Verse'])
            ]['Scripture'].to_string().replace(str(ind), '')

        verse_2 = bible.loc[
            (bible['Book'] == ref['Book']) &
            (bible['Chapter'] == ref['Chapter']) &
            (bible['Verse'] == ref['Verse'] + 1)
            ]['Scripture'].to_string().replace(str(ind + 1), '')

        verse_1 = re.sub(r'<sup>[(][0-9]*[-][0-9]*[)]</sup>', '',
                         ' '.join(verse_1.split()))
        verse_2 = ' '.join(verse_2.split())
        new_verse = verse_1 + verse_2

        try:

            bible.replace(to_replace=verse_1, value=new_verse, regex=True, inplace=True)

            bible.drop(index=ind + 1, inplace=True)

        except re.error:
            try:
                for ke, bi in zip(bibles.keys(), bibles.values()):

                    ver = bi.loc[
                        (bi['Book'] == ref['Book']) &
                        (bi['Chapter'] == ref['Chapter']) &
                        (bi['Verse'] == ref['Verse'])
                        ]['Scripture']

                    i = Index(bi['Scripture']).get_loc(ver)

                    bi.drop(index=i, inplace=True)
                    bi.drop(index=i + 1, inplace=True)
                    file.write('Indexes {} and {} dropped.\n'.format(i, i + 1))

            except Exception:

                file.write(Exception.__traceback__.__str__() + '\n')

        bible.to_csv(path + key, index=False)


file = open('collapsed.txt', 'w', encoding='utf-8')

for k, b in zip(bibles.keys(), bibles.values()):

    scrip = b['Scripture']
    file.write(k + '\n')
    for verse in scrip:
        search = re.search('(?<=(<sup>))[(][0-9]*[-][0-9]*[)]', verse)

        if search is not None:
            ind = Index(scrip).get_loc(verse)
            reference = b.loc[ind, :]
            print(reference)
            file.write(reference.to_string() + '\n')
            collapse_verses(bibles, reference)

        else:
            search = re.search(r'[(]\s[0-9]*\s[-]\s[0-9]*\s[)]', verse)

            if search is not None:
                ind = Index(scrip).get_loc(verse)
                reference = b.loc[ind,:]
                print(reference)
                file.write(reference.to_string())
                collapse_verses(bibles, reference)

file.close()

noise = get_noise()
datasets = prep.clean_data(noise)

for k, b in zip(datasets.keys(), datasets.values()):
    b.to_csv(path + k, index=False)
