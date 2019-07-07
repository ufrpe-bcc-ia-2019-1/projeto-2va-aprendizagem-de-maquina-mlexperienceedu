import pandas as pd
import numpy as np


guarani = pd.read_csv('guarani.csv',encoding ='utf8')
ntlh = pd.read_csv('NTLH.csv',encoding ='utf8')

raw_1 = guarani['Scripture']

raw_2 = ntlh['Scripture']

gu_pt = []
for verse_g, verse_p in zip(raw_1, raw_2):
    gu_pt.append(verse_g + "\t" + verse_p + "\n")

d = {'txt': raw_data}


df = pd.DataFrame(data=d)
file = df.to_csv('gu-pt.txt')