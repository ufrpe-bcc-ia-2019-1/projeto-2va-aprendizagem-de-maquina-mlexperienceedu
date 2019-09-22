from aifc import Error

import pandas as pd
import matplotlib.pyplot as plt
import random
import re
import numpy as np
from numpy.random.mtrand import shuffle
from pandas import Series
import os


def get_noise():
    livros = []
    penta = ['Gênesis', 'Êxodo', 'Levítico', 'Números', 'Deuteronômio']

    history = ['Josué', 'Juízes', 'Rute', '1 e 2 Samuel', '1 e 2 Reis', '1 e 2 Crônicas', 'Esdras', 'Neemias',
               'Tobias',
               'Judite', 'Ester', '1 e 2 Macabeus']

    poete = ['Jó', 'Salmo', 'Provérbios', 'Eclesiastes', 'Cântico dos Cânticos', 'Sabedoria', 'Eclesiástico']

    profe = ['Isaías', 'Jeremias', 'Lamentações', 'Baruc', 'Ezequiel', 'Daniel', 'Oséias', 'Joel', 'Amós', 'Abdias',
             'Jonas', 'Miquéias', 'Naum', 'Habacuque', 'Sofonias', 'Ageu', 'Zacarias', 'Malaquias']

    evan = ['Mateus', 'Marcos', 'Lucas', 'João']

    cartas = ['Atos', 'Romanos', '1 e 2 Coríntios', 'Gálatas', 'Efésios', 'Filipenses', 'Colossenses',
              '1 e 2 Tessalonicenses', '1 e 2 Timóteo', 'Tito', 'Filemon', 'Hebreus', 'Tiago', '1 e 2 Pedro',
              '1 a 3 João',
              'Judas', 'Apocalipse']

    livros.extend(penta)
    livros.extend(history)
    livros.extend(poete)
    livros.extend(profe)
    livros.extend(evan)
    livros.extend(cartas)
    noise = []

    for livro in livros:
        livro += ' [0-9]*[.]*[0-9]*[-]*[0-9]*[;]*'
        livro = livro.replace('1 e 2', '[0-9]')
        livro = livro.replace('1 a 3', '[0-9]')
        noise.append(livro)

    noise.append(r'[-][0-9][0-9]*')
    noise.append(r'<sup>[(][0-9]*[-][0-9]*[)]<[/]sup>')
    noise.append(r'<.*?>\w+\s[0-9]*[.][0-9]*[-]*[0-9]*<.*?>[,;]*')
    noise.append(r'<.*?>[0-9]*[.][0-9]*[-]*[0-9]*<.*?>[,;]*')
    noise.append(r'\w+\s[0-9][0-9]*[.][0-9][0-9]*')
    noise.append(r'<.*?>\w*[0-9]*[.]*[0-9]*[-]*[0-9]*[,;]*<.*?>')
    noise.append(r'<.*?>[,;]*')
    noise.append(r'[;]\s[)]')
    noise.append(r'[()]')
    noise.append(r'Series[(,\s)],\s[()]')
    noise.append(r'[(]\s[0-9]*\s[-]\s[0-9]*\s[)]')
    noise.append('Veja verso [0-9]*')
    noise.append(r'Series\(\[\], \)')
    noise.append(r'\\\\')
    noise.append(r'\[*\]')
    noise.append(r'\{*\}')


    return noise


def collapse_verses(bibles, ref, verses_seq, path):
    for key, bible in zip(bibles.keys(), bibles.values()):

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

            d_start = 1

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
                    file.write(str(IndexError))
                    file.write(ref)
                    print(ref)
                    pass

            bible.to_csv(path + key, index=False)


def align_verses(bibles, path):
    global reference

    pd.set_option('display.max_colwidth', -1)

    for k, b in zip(bibles.keys(), bibles.values()):

        print('\nCollapsing verses : ', k, '...')
        print('\nProgress: #', end='')
        for verse, ind in zip(b['Scripture'], b['Scripture'].index.values.astype(int)):

            try:
                search = re.search(r'(?<=<sup>)[(][0-9]*[-][0-9]*[)]', verse)
                first = re.search(r'(?<=([(]))[0-9][0-9]*', search.group(0)).group(0)
                last = re.search(r'(?<=([-]))[0-9][0-9]*', search.group(0)).group(0)
                verses = np.arange(int(first), int(last) + 1)

                reference = b.loc[ind, :]
                print('#', end='')

                collapse_verses(bibles, reference, verses, path)
            except AttributeError:

                try:

                    range = re.search(r'(?<=[(]\s)[0-9][0-9]*[-][0-9][0-9]*', verse).group(0)

                    first = re.search(r'[0-9][0-9]*', range).group(0)
                    last = re.search(r'(?<=-)[0-9][0-9]*', range).group(0)

                    verses = np.arange(int(first), int(last) + 1)
                    print('#', end='')

                    reference = b.loc[ind, :]

                    collapse_verses(bibles, reference, verses, path)
                except AttributeError:
                    pass

            except IndexError:
                print(IndexError)
                file = open('report/logs.txt', 'a', encoding='utf-8')
                file.write(k + '\n')
                file.write(str(b[b['Scripture'] == verse]))
                file.write('Pattern: ' + r'(?<=(<sup>[(]))[0-9][0-9]*')
                file.close()
                pass
            except TypeError:
                print(TypeError)
                file = open('report/logs.txt ', 'a', encoding='utf-8')
                file.write(k + '\n')
                file.write(str(b[b['Scripture'] == verse]))
                file.write('Pattern: ' + r'(?<=(<sup>[(]))[0-9][0-9]*')
                file.close()

        print('\nFinished Successfully!')


def save_pairs(data_pairs, dir_path):
    for key, text in zip(data_pairs.keys(), data_pairs.values()):

        path = dir_path + key

        file = open(path, 'w', encoding='utf-8')

        for line in text:
            file.write(line)

        file.close()


class PrepData:
    datasets = None
    datasets_list = []
    root_dir = ''

    def __init__(self, dir_path):
        self.root_dir = dir_path
        self.datasets_list = os.listdir(dir_path)
        self.datasets = {}.fromkeys(self.datasets_list)

    def set_root_dir(self, path_prefix):
        self.root_dir = path_prefix

    def get_prefix(self, path_prefix):
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

    def to_pair_format(self, pairs):

        pair_text = []
        data_pairs = {}.fromkeys(pairs)

        for p in pairs:
            print()
            self.datasets[p[0].encode('utf-8')]['Scripture'].align(
                self.datasets[p[1].encode('utf-8')]['Scripture'])

            for r_1, r_2 in zip(Series(self.datasets[p[0].encode('utf-8')]['Scripture']),
                                Series(self.datasets[p[1].encode('utf-8')]['Scripture'])):
                pair_text.append(' '.join(r_1.split()) + '\t' + ' '.join(r_2.split()) + '\n')
            shuffle(pair_text)
            key = re.sub(r'[(] | [)]', '', str(p))
            key = re.sub(r'[,]', '-', key)
            data_pairs[key] = pair_text

        return data_pairs
