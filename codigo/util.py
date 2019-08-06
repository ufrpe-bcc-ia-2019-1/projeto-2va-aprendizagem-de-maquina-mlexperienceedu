import pandas as pd
import matplotlib.pyplot as plt
import re

class prepData():
      
  datasets = None
  datasets_names = []
  prefix = ''
  sufix = ''

  def __init__(self, datasets_names=[]):
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
      path = path.replace(name + self.sufix,'')

    return self.datasets

  def save_pairs(self,file_names=[], texts=[]):
    
    for file_name, text in zip(file_names, texts):
      path = self.prefix + file_name + self.sufix

      file = open(path, 'w', encoding='utf-8')

      for line in text:
        file.write(line)
      
      file.close()

  def save_all_datasets(self):
        
    for name, data in zip(self.datasets_names, self.datasets.values()):
      path = self.prefix + name + self.sufix
      
      data.to_csv(path, index=False)
      path = path.replace(name + self.sufix,'')

  def to_pair_format(self, raw_1, raw_2, data_index):

    pair_text = []

    for r_1, r_2 in zip(raw_1[data_index], raw_2[data_index]):
  
      r_1 = ' '.join(str(r_1).split())
      r_2 = ' '.join(str(r_2).split())

      pair_text.append(r_1 + '\t' + r_2 + '\n')

    return pair_text




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
   

