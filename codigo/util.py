import pandas as pd
import matplotlib.pyplot as plt
import random


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
        livro += ' [0-9]*.[0-9]*'
        livro = livro.replace('1 e 2', '[0-9]')
        livro = livro.replace('1 a 3', '[0-9]')
        noise.append(livro)
    noise.append('<.*?>|<.*?>.*?<.*?>')

    return noise


class PrepData:
    datasets = None
    datasets_names = []
    prefix = ''
    sufix = ''

    def __init__(self, datasets_names):
        self.datasets_names = datasets_names
        self.datasets = {}.fromkeys(datasets_names)

    def set_prefix(self, path_prefix):
        self.prefix = path_prefix

    def set_dataset_names(self, datasets_names):
        self.datasets_names = datasets_names

    def set_sufix(self, file_sufix):
        self.sufix = file_sufix

    def get_prefix(self, path_prefix):
        return self.prefix

    def get_dataset_names(self, datasets_names):
        return self.datasets_names

    def get_sufix(self, file_sufix):
        return self.sufix

    def read_all(self, regex=[]):

        for name in self.datasets_names:

            path = self.prefix + name + self.sufix

            try:
                dataset = pd.read_csv(path, encoding='utf-8')
                self.datasets[name] = dataset
            except:
                return "The path " + path + " was not found."

        return self.datasets

    def clean_data(self, regex=[]):

        for name in self.datasets_names:

            path = self.prefix + name + self.sufix

            try:
                dataset = pd.read_csv(path, encoding='utf-8')
            except:
                return "The path " + path + " was not found."

            for exp in regex:
                dataset = dataset.replace(to_replace=exp, value='', regex=True)

            self.datasets[name] = dataset
            path = path.replace(name + self.sufix, '')

        return self.datasets

    def save_pairs(self, file_names=[], texts=[]):

        for file_name, text in zip(file_names, texts):
            path = self.prefix + file_name + self.sufix

            file = open(path, 'w', encoding='utf-8')

            for line in text:
                file.write(line)

            file.close()

    def save_all_datasets(self):

        for name, data in zip(self.datasets.keys(), self.datasets.values()):
            path = self.prefix + name + self.sufix

            data.to_csv(path, index=False)
            path = path.replace(name + self.sufix, '')

    def to_pair_format(self, pairs):

        pair_text = []
        data_pairs = []
        for p in pairs:
            for r_1, r_2 in zip(self.datasets[p[0]]['Scripture'], self.datasets[p[1]]['Scripture']):
                r_1 = ' '.join(str(r_1).split())
                r_2 = ' '.join(str(r_2).split())
                pair_text.append(r_1 + '\t' + r_2 + '\n')
                random.shuffle(pair_text)
            data_pairs.append(pair_text)

        return data_pairs


class Result:

    def calculate_time(self, results={}):

        time_taken = 0

        for t in results['time']:
            time_taken += t

        print("Total time taken: {} sec {} hs".format(time_taken, time_taken / 3600))

    def obtain_results(self, file_name, param=[]):

        results = {}

        for p in param:
            results[p] = []

        file = open(file_name, 'r')

        line = file.readline()
        while line:

            data = line.lower().split()

            for p in param:
                index = data.index(p)
                results[p].append(float(data[index + 1]))

            line = file.readline()

        file.close()

        return results

    def plot_results(self, results, param1, param2, xlabel, ylabel, title):

        plt.plot(results[param1], results[param2])
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        plt.show()

    def save_epoch_results(self, epoch, loss, time):

        file = open('results.txt', 'a')
        file.write('epoch ' + epoch + ' loss ' + loss + ' time ' + time)
        file.close()

    def saving_result(self, treino, teste, acc):
        path = "raw_data/results/"
        file = open(path + "test_result.txt", 'a')

        file.write('Train ' + str(treino) + '\tTest ' + str(teste) + '\tAcc ' + str(acc) + '\n')

        file.close()
