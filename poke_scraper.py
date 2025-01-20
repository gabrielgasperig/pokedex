import requests, six
import lxml.html as lh
from itertools import cycle, islice
import pandas as pd
from matplotlib import colors
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix

url = 'https://pokemondb.net/pokedex/all'

page = requests.get(url)

doc = lh.fromstring(page.content)

tr_elements = doc.xpath('//tr')

col = []
i = 0

for t in tr_elements[0]:
    i += 1
    name = t.text_content()
    print ('%d:"%s"'%(i, name))
    col.append((name, []))

[len(T) for T in tr_elements[:12]]

for j in range(1, len(tr_elements)):
    T = tr_elements[j]

    if len(T) != 10:
        break
    i=0

    for t in T.iterchildren():
        data = t.text_content()
        if i > 0:
            try:
                data = int(data)
            except:
                pass
        col[i][1].append(data)
        i += 1

[len(C) for (title, C) in col]

Dict = {title:column  for (title, column) in col}

df = pd.DataFrame(Dict)

df.head()

def str_bracket(word):
    list = [x for x in word]
    for char_ind in range(1, len(list)):
        if list[char_ind].isupper():
            list[char_ind] = ' ' + list[char_ind]
    fin_list = ''.join(list).split(' ')
    length = len(fin_list)
    if length > 1:
        fin_list.insert(1, '(')
        fin_list.append(')')
    return ' '.join(fin_list)

def str_break(word):
    list = [x for x in word]
    for char_ind in range(1, len(list)):
        if list[char_ind].isupper():
            list[char_ind] = ' ' + list[char_ind]
    fin_list = ''.join(list).split(' ')
    return fin_list

df['Name'] = df['Name'].apply(str_bracket)
df['Type'] = df['Type'].apply(str_break)
df.head()

df.to_json('pokemon_data.json')

df = pd.read_json('pokemon_data.json')
df = df.set_index(['#'])
df.head()

def max_stats(df, col_list):
    message = ''
    for col in col_list:
        stat = df[col].max()
        name = df[df[col] == df[col].max()] ['Name'].values[0]
        message += name + ' has the greatest '+ col + ' of ' + str(stat) + '.\n'
    return message

def min_stats(df, col_list):
    message = ''
    for col in col_list:
        stat = df[col].min()
        name = df[df[col] == df[col].min()] ['Name'].values[0]
        message += name + ' has the worst '+ col + ' of ' + str(stat) + '.\n'
    return message

stats = ['Attack' , 'Defense', 'HP', 'Sp. Atk', 'Sp. Def', 'Speed', 'Total']

scatter_matrix(df [stats], alpha=0.2, figsize=(10, 10), diagonal = 'kde')

scatter_matrix(df [stats[:-1]], alpha=0.2, figsize=(10, 10), diagonal = 'kde')

newDict = {}

stats_col = ["#", "Name", "Total", "HP", "Attack", "Defense", "Sp. Atk", "Sp. Def", "Speed"]

Dict['Type'] = df ['Type'].values

for col in stats_col:
    newDict[col] = []
    newDict['Type'] = []

for row in range(len(Dict['#'])):
    for t in Dict['Type'][row]:
        for col in stats_col:
            newDict[col].append(Dict[col][row])
        newDict['Type'].append(t)

new_df = pd.DataFrame(newDict)

new_df.head()

types = new_df['Type'].unique()

my_colors = list(six.iteritems(colors.cnames))
my_colors = list(islice(cycle(my_colors), None, len(new_df)))

def barh_stats():
    i = 0
    plt.figure(figsize=(15,5))
    plt.suptitle('Statistics', fontsize=15)
    
    for t in types:
        i += 1

        plt.subplot(121)
        plt.title('Mean')
        new_df[new_df['Type'] == t].mean().plot(kind='barh', color=my_colors)

        plt.subplot(122)
        plt.title('Standard Deviation')
        new_df[new_df['Type'] == t].std().plot(kind='barh', color=my_colors)
        
plt.legend(types,bbox_to_anchor=(1.3, 1.1))

barh_stats()