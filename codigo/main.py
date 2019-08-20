from util import prepData
import matplotlib.pyplot as plt
import numpy as np 
import pandas as pd
import re

#--- Tirando referências -----
livros = []
penta = ['Gênesis', 'Êxodo', 'Levítico', 'Números', 'Deuteronômio']

history = ['Josué', 'Juízes', 'Rute', '1 e 2 Samuel', '1 e 2 Reis', '1 e 2 Crônicas', 'Esdras', 'Neemias', 'Tobias', 'Judite', 'Ester', '1 e 2 Macabeus']

poete = ['Jó', 'Salmo', 'Provérbios', 'Eclesiastes', 'Cântico dos Cânticos', 'Sabedoria', 'Eclesiástico']

profe = ['Isaías', 'Jeremias', 'Lamentações', 'Baruc', 'Ezequiel', 'Daniel', 'Oséias', 'Joel', 'Amós', 'Abdias', 'Jonas', 'Miquéias', 'Naum', 'Habacuque', 'Sofonias', 'Ageu', 'Zacarias', 'Malaquias']

evan = ['Mateus', 'Marcos', 'Lucas', 'João']

cartas = ['Atos', 'Romanos', '1 e 2 Coríntios', 'Gálatas', 'Efésios', 'Filipenses', 'Colossenses','1 e 2 Tessalonicenses', '1 e 2 Timóteo', 'Tito', 'Filemon', 'Hebreus', 'Tiago', '1 e 2 Pedro', '1 a 3 João', 'Judas', 'Apocalipse']

livros.extend(penta)
livros.extend(history)
livros.extend(poete)
livros.extend(profe)
livros.extend(evan)
livros.extend(cartas)

noise = []
for livro in livros:
    livro = livro + ' [0-9]*.[0-9]*'
    livro = livro.replace('1 e 2', '[0-9]')
    livro = livro.replace('1 a 3', '[0-9]')
    noise.append(livro)

prep = prepData(['guarani', 'karaja', 'xavante', 'tukano','portugues'])

prep.set_prefix('raw_data/')

prep.set_sufix('.csv')

datasets = prep.read_all()

gu_pt = prep.to_pair_format(datasets['guarani'], datasets['portugues'], 'Scripture')
ka_pt = prep.to_pair_format(datasets['karaja'], datasets['portugues'], 'Scripture')
xa_pt = prep.to_pair_format(datasets['xavante'], datasets['portugues'], 'Scripture')
tu_pt = prep.to_pair_format(datasets['tukano'], datasets['portugues'], 'Scripture')

names = ['gu-pt', 'ka-pt', 'xa-pt', 'tu-pt']
pairs = [gu_pt, ka_pt, xa_pt, tu_pt]
prep.set_prefix('raw_data/pairs/')
prep.set_sufix('.txt')
prep.save_pairs(names, pairs)
