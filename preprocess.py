import pandas as pd
import matplotlib.pyplot as plt
import re


def clean_data(path = 'raw_data/', names=[]):
  
  datasets = []
  
  for name in names:
    path = path+name+'.csv'
    dataset = pd.read_csv(path, encoding='utf-8')
    dataset = dataset.replace(to_replace='<.*?>*<.*?>', value='', regex=True)
    dataset = dataset.replace(to_replace='<.*?>', value='', regex=True)
    datasets.append(dataset)
    path = re.sub(name+'.csv','',path)
    

  return datasets

def save_dataframe(names, dataframes=[], path = 'raw_data/'):
 
  for name, dataframe in zip(names, dataframes):
    path = path+name+'.csv'
    dataframe.to_csv(path, index=False)
    path = path.replace(name+'.csv','')


def to_translation_format(raw_1, raw_2):

  filted_text = []

  for r_1, r_2 in zip(raw_1, raw_2):
 
    r_1 = ' '.join(str(r_1).split())
    r_2 = ' '.join(str(r_2).split())

    filted_text.append(r_1 + '\t' + r_2 + '\n')
    
  return filted_text


def to_file(data, path='data.txt'):
    file = open(path, 'w', encoding="utf-8")

    for line in data:
       file.write(line)

    file.close()

def calculate_time(results = {}):
      
  time_taken = 0

  for t in results['time']:
    time_taken += t

  print("Total time taken: {} sec {} hs".format(time_taken,time_taken/3600))




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

def plot_results(results, param1, param2, xlabel, ylabel, title):

    plt.plot(results[param1], results[param2])
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.show()
   

title = "Evolução da precisão"
xlabel = 'Quantidade exemplos usados para teste'
ylabel = 'Precisão utilizando 1 - distância de Hamming'

