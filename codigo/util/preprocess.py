from aifc import Error
from itertools import permutations

import pandas as pd
import matplotlib.pyplot as plt
import random
import re
import numpy as np
from numpy.random.mtrand import shuffle
from pandas import Series
import os


class PrepData:
    datasets = None
    datasets_list = []
    root_dir = ''
    data_pairs = {}

    def __init__(self, dir_path):
        self.root_dir = dir_path
        self.datasets_list = os.listdir(dir_path)
        self.datasets = {}.fromkeys(self.datasets_list)

    def set_root_dir(self, path_prefix):
        self.root_dir = path_prefix

    def get_prefix(self):
        return self.root_dir

    def get_dataset_list(self):
        return self.datasets_list

    def set_datasets(self, datasets):
        self.datasets = datasets

    def get_datasets(self):

        for name in self.datasets_list:

            path = self.root_dir + name

            try:
                self.datasets[name] = pd.read_csv(path, encoding='utf-8').drop_duplicates(subset='Scripture')

            except FileNotFoundError:
                return "The path " + path + " was not found."

        return self.datasets

    def clean_data(self, regex=None, auto_save=False):

        if regex is None:
            regex = []

        for name in self.datasets_list:
            print('\nCleaning: ', name)
            print('Progress: #', end='')
            path = self.root_dir + name

            try:
                dataset = pd.read_csv(path, encoding='utf-8')
            except FileNotFoundError:
                return "The path " + path + " was not found."

            for exp in regex:
                print('#', end='')
                dataset = dataset.replace(to_replace=exp, value='', regex=True)

            self.datasets[name] = dataset

            if auto_save is True:
                dataset.to_csv(path, index=False)

        return self.datasets

    def get_dataset(self, dataset_name):
        dataset = self.get_datasets()
        return dataset.get_value(dataset_name)

    def get_text_pairs(self):
        self.get_datasets()

        k_pairs = list(permutations(self.datasets.keys(), 2))

        print('\nCreating pairs: ')
        print('Progress: #', end='')

        for p in k_pairs:

            key = re.sub(r'\s[-]\sBíblia Completa.csv', '', str(p))
            key = re.sub(r'\s[-]\sNovo Testamento.csv', '', str(p))
            key = re.sub(r'\(', '', key)
            key = re.sub(r'\)', '', key)
            key = re.sub(r'[,]', ' -', key)
            key = re.sub(r'[\']', '', key)

            pair_text = []
            print('#', end='')
            self.datasets[p[0]]['Scripture'].align(self.datasets[p[1]]['Scripture'])

            for r_1, r_2 in zip(self.datasets[p[0]]['Scripture'],
                                self.datasets[p[1]]['Scripture']):

                try:

                    pair_text.append(' '.join(str(r_1).split()) + '\t' + ' '.join(str(r_2).split()) + '\n')

                except AttributeError:
                    print(AttributeError)

                    breakpoint()

            shuffle(pair_text)

            self.data_pairs[key] = pair_text

        return self.data_pairs

    def label_data(self, path):
        self.get_datasets()
        labels = []
        texts = []
        for key, data in zip(self.datasets.keys(), self.datasets.values()):

            for text in data['Scripture']:
                key = re.sub(r'\s-\sNovo\sTestamento.csv', '', key)
                labels.append(key)
                texts.append(text)

        df = pd.DataFrame({
            'text': texts,
            'label': labels
        })
        df.to_csv(path, index=False)

    def stemming(self):

        dataset = self.get_datasets()
        data = dataset[0]
        scripture = data['Scripture']

        for verse in scripture:

            tokens = verse.split(r'\s')

            for token in tokens:
                letter = token.split()
                print(letter)
                break

    def save_pairs(self, file_type):

        print('\nSaving pairs: ')
        print('Progress: #', end='')
        for key, text in zip(self.data_pairs.keys(), self.data_pairs.values()):

            path = self.root_dir + key + file_type
            print('#', end='')

            file = open(path, 'w', encoding='utf-8')

            for line in text:
                file.write(line)

            file.close()

    def collapse_verses(self, ref, verses_seq):

        for key, bible in zip(self.datasets.keys(), self.datasets.values()):

            script_seq = []
            for v_seq in verses_seq:
                check = bible.loc[
                    (bible['Book'] == ref['Book']) &
                    (bible['Chapter'] == ref['Chapter']) &
                    (bible['Verse'] == v_seq)
                    ]['Scripture'].empty

                verse_1 = bible.loc[
                    (bible['Book'] == ref['Book']) &
                    (bible['Chapter'] == ref['Chapter']) &
                    (bible['Verse'] == v_seq)
                    ]['Scripture'].to_string(index=False)

                if check is not True:
                    verse_1 = ' '.join(verse_1.split())
                    script_seq.append(verse_1)

            if len(script_seq) > 0:

                new_verse = ' '.join(script_seq)

                new_verse = re.sub(r'<sup>[(][0-9]*[-][0-9]*[)]<[/]sup>', '', new_verse)
                regexs = [r'[)]', r'[(]', r'[\[]', r'[\]]', r'[\{]', r'[\}]']
                to_str = [r'\)', r'\(', r'\]', r'\]', r'\{', r'\}']

                for res, to_str in zip(regexs, to_str):
                    script_seq[0] = re.sub(res, to_str, script_seq[0])

                try:
                    bible.replace(to_replace=script_seq[0], value=new_verse, regex=True, inplace=True)
                except re.error:
                    file = open('report/logs.txt', 'a', encoding='utf-8')
                    file.write(script_seq[0])
                    print(script_seq[0])
                    breakpoint()

                for v_seq in verses_seq[1:]:
                    try:
                        i = bible.loc[
                            (bible['Book'] == ref['Book']) &
                            (bible['Chapter'] == ref['Chapter']) &
                            (bible['Verse'] == v_seq)
                            ]['Scripture'].index.values.astype(int)
                        bible.drop(index=i, inplace=True)
                    except IndexError:
                        file = open('report/logs.txt', 'a', encoding='utf-8')
                        file.write(str(IndexError))
                        file.write(ref)
                        print(ref)
                        pass

                self.datasets[key] = bible

    def align_verses(self):
        global reference

        pd.set_option('display.max_colwidth', -1)

        for k, b in zip(self.datasets.keys(), self.datasets.values()):

            print('\nCollapsing verses : ', k, '...')
            print('\nProgress: #', end='')
            size = len(b['Scripture'].index.values.astype(int))
            step = 1/100
            total_done = 0
            temp = 0

            for verse, ind in zip(b['Scripture'], b['Scripture'].index.values.astype(int)):

                try:
                    search = re.search(r'(?<=<sup>)[(][0-9]*[-][0-9]*[)]', verse)
                    first = re.search(r'(?<=([(]))[0-9][0-9]*', search.group(0)).group(0)
                    last = re.search(r'(?<=([-]))[0-9][0-9]*', search.group(0)).group(0)
                    verses = np.arange(int(first), int(last) + 1)

                    reference = b.loc[ind, :]

                    if temp >= int(size * step):
                        total_done += temp
                        temp = 0
                        print('#', end='')

                    self.collapse_verses(reference, verses)
                except AttributeError:

                    try:

                        first = re.search(r'(?<=([(]\s))[0-9][0-9]*', verse).group(0)
                        last = re.search(r'(?<=-\s)[0-9][0-9]*', verse).group(0)

                        verses = np.arange(int(first), int(last) + 1)

                        if temp >= int(size * step):
                            total_done += temp
                            temp = 0
                            print('#', end='')

                        reference = b.loc[ind, :]

                        self.collapse_verses(reference, verses)
                    except AttributeError:
                        pass

                    except IndexError:
                        print(IndexError)
                        file = open('logs.txt', 'a', encoding='utf-8')
                        file.write(k + '\n')
                        file.write(str(b[b['Scripture'] == verse]))
                        file.write('Pattern: ' + r'(?<=(<sup>[(]))[0-9][0-9]*')
                        file.close()
                        pass

                except TypeError:
                    print(TypeError)
                    file = open('logs.txt ', 'a', encoding='utf-8')
                    file.write(k + '\n')
                    file.write(str(b[b['Scripture'] == verse]))
                    file.write('Pattern: ' + r'(?<=(<sup>[(]))[0-9][0-9]*')
                    file.close()
                temp += 1

            print('\nTotal done: {} Finished Successfully!'.format(total_done))

        for key, data in (self.datasets.keys(), self.datasets.values()):
            data.to_csv(self.root_dir + key, index=False)
