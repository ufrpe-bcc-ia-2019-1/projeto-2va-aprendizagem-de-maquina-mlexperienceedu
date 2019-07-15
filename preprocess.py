import pandas as pd
plot.pyplot.plot(('xEpoch', 'yLoss', data=results))
import matplotlib as mat

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

def obtain_results():

    file = open('results.txt', 'r')
    results = { 'epoch': [],
                'loss': [] }

    epoch = []
    loss = []
    


    line = True
    while line:
        result = []
        for i in range(3):
            line = file.readline()
            result.append(line.lower().split())

        line = file.readline()

        index = result[1].index('epoch')
        epoch.append(int(result[1][index+1]))
        index = result[1].index('loss')
        loss.append(float(result[1][index+1]))
        
        
    file.close()


    results['epoch'] = epoch
    results['loss'] = loss
   
    return results

results = obtain_results()
print(results)
mat.pyplot.plot('xEpoch', 'yLoss', data=results)