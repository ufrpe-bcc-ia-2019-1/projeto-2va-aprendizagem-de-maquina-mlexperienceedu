import pandas as pd

guarani = pd.read_csv('raw_data/guarani.csv', encoding='utf-8')
pt_br = pd.read_csv('raw_data/NTLH.csv', encoding='utf-8')

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
