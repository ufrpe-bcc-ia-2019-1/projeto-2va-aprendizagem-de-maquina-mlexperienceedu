import pandas as pd
import matplotlib.pyplot as plt

guarani = pd.read_csv('raw_data/guarani.csv', encoding='utf-8')
pt_br = pd.read_csv('raw_data/portugues.csv', encoding='utf-8')

guarani = guarani['Scripture']
pt_br = pt_br['Scripture']


def to_translation_format(raw_1, raw_2):

    filter_text = []

    for r_1, r_2 in zip(raw_1, raw_2):

        r_1 = ' '.join(r_1.split())
        r_2 = ' '.join(r_2.split())

        filter_text.append(r_1 + '\t' + r_2 + '\n')
        
    return filter_text


def to_file(data, path='gu-pt_v1.txt'):
    file = open(path, 'w', encoding="utf-8")

    for line in data:
       file.write(line)

    file.close()


data = to_translation_format(guarani, pt_br)

to_file(data)

def obtain_results(file_name, param = []):

    results = {}

    for p in param:
        results[p] = []

    file = open(file_name, 'r')
   
    line = file.readline()
    while line:
      
      data = line.lower().split()

      for p in param:
        index = data.index(p)
        results[p].append(float(data[index+1]))

      line = file.readline()

    file.close()

    return results

results = obtain_results('raw_data/results.txt', ['time'])

time_taken = 0

for t in results['time']:
      time_taken += t

print(time_taken/3600)
print("Epoch necessárias: {} ".format(400/(time_taken/3600)))

def plot_results(results, param1, param2, xlabel, ylabel, title):

    plt.plot(results[param1], results[param2])
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.show()
   

title = "Evolução da precisão"
xlabel = 'Quantidade exemplos usados para teste'
ylabel = 'Precisão utilizando 1 - distância de Hamming'

#plot_results(results, 'test', 'acc', xlabel, ylabel, title)