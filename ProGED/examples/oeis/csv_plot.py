# Libraries
import numpy as np
import matplotlib.pyplot as plt


import os, sys
import requests, re, time
import pandas as pd
from bs4 import BeautifulSoup

# if __name__ == '__main__':

url = "http://oeis.org/wiki/Index_to_OEIS:_Section_Rec"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, '
                  'like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
}
f = requests.get(url, headers=headers)
# f = requests.get(url)
# print(f.content)
# 1/0
soup = BeautifulSoup(f.content, 'html.parser')
# print(soup.prettify())
# print(soup)

# a. find all oeis ids
ids = soup.find_all('a', text=re.compile(r'A\d{6}'))
# ids = soup.find_all(text=r'A\w{6}')
# ids_txt = [i.text for i in ids]
ids_txt = ids
print(len(ids_txt))  # 2022.12.02: 34384
print(len(ids))
print(len(set(ids_txt)))  # 2022.12.02: 34371  (all good, i.e. doublets)
# Current total success (33787/34371, i.e. 584 lost scrapped into csv 2022.12.02).
# linseqs:  34384 or 34371  (100%)
# csv:  34384 or 34371  (100%)

# # Check for doublets:
# #   - (list vs set: 34384 vs. 34371) checked out: some sequences have e.g. order 3 and 4. So all good.
# counter = dict()
# for id_ in ids_txt:
#     # if ids_txt[id_] += 1
#     # counter[id_] = 1 \
#     if id_ not in counter:
#         counter[id_] = 1
#     else:
#         counter[id_] += 1
# doublets =  [(k, i) for k, i in counter.items() if i>1]
# print(doublets)
# print(len(ids))

# b. get webpage tree or dictionary of key: [list of sequences]
"""
linseqs = dictionary of orders as keys and values as lists of seqs of linear recursive order.
idea:
  linseqs -> seqsd = dict( id: seq) -> pd.Dataframe(seqsd).sorted.to_csv()

for seq in seqs: bfile2list
"""

# start = 100
start = 13800
scale_tree = 10
# scale_tree = 1000
# scale_tree = 30000
# scale_tree = 10**5
# scale_tree = 40000
# scale_tree = 25000
scale_tree = 1000000
# print(scale_tree)
# linseqs['7'] = [None]
# scale_tree = 13900

# linseqs['131071'] = [None]
start = 0
# scale_tree = 10**6

# order = '8'
# linseqs['8'] = [None]

verbosity = False
# verbosity = True

linseqs = dict()
for id in ids[start:scale_tree]:
    parent = id.parent
    truth = re.findall(r'\([-\d, \{\}\.\"\']*\)', parent.text)
    if truth == []:
        if verbosity:
            print('first empty:', parent.text)
        truth = re.findall(r'\(-*\d[-, \{\}\w\'\"\.\d\(\)]*\):', parent.text)
    # if truth == []:
    #     print(parent.text)
    #     truth = re.findall(r'\((-*\d[, \{\}\w\'\"\.\d\(\)]*).+\):', parent.text)
    #     print(truth)
    if truth == []:
        print(parent.text)
        truth = [truth]
    truth = truth[0]

    if parent.previous_sibling is None:
        previous = parent.parent.previous_sibling.previous_sibling
        if previous.name == 'h4':
            title = previous.text
            order = re.findall(r'(\d+)', title)[0]
            if order not in linseqs:
                linseqs[order] = [(truth, id.text)]
            else:
                linseqs[order] += [(truth, id.text)]
        else:
            linseqs[order] += [(truth, id.text)]
            if previous.name not in linseqs:
                pass
                # linseqs[previous.name] = [previous]
            else:
                pass
                # linseqs[previous.name] += [previous]
    else:
        linseqs[order] += [(truth, id.text)]

#  b.1 check linseqs
print(len(linseqs))
# print([(seqs, len(linseqs[seqs])) for seqs in linseqs])
print(sum(len(linseqs[seqs]) for seqs in linseqs))

# ids_list = []
# for _, seqs in linseqs.items():
#     ids_list += seqs
# print(ids_list, len(ids_list))
#
# reconst = []
# for seqs in linseqs.values():
#     reconst += seqs
# print(f'reconstructed: {len(reconst)}')
# ids_raw = {id.text for id in ids[start:scale_tree]}
# print(f'wanna reconstruct: {len(ids_raw)}')
# reconsts = set(reconst)
# print(set(ids_raw).difference(reconsts))
# # print(reconst[:14])
# # print(prob in reconsts)
#
# till_order = 10 ** 16
# till_order = 10
# if verbosity:
#     for order, seqs in list(linseqs.items()):
#         if int(order) < till_order:
#             print(f'order: {order}')
#             for truth, seq in seqs:
#                 # print(int(order) * "  " + f'\\_ {seq}   order: {order}')
#                 print("  " + f'\\_ {truth}: {seq}   order: {order}')
#


# sum([len(linseqs[order]) for order in linseqs if int(order)>25])

limit = 2000
# limit = 100
# limit = 20
# limit = 21

addage = "for orders < " + str(limit)
orders = [int(key) for key in linseqs if int(key)<=limit]
per_orders = [len(linseqs[key]) for key in linseqs if int(key)<=limit]

# relevant_seqs = [linseqs[key] for key in linseqs if int(key)<=limit]
relevant_seqs_fold = [[seq_id for coeffs, seq_id in linseqs[key]] for key in linseqs if int(key)<=limit]
relevant_seqs = []
for order_pack in relevant_seqs_fold:
    relevant_seqs += order_pack


# relevant_seqs = [len(linseqs[key]) for key in linseqs if int(key)<=limit]
print(relevant_seqs)  # Relevant sequences.

# print([i for i in relevant_seqs if i<2])
all_seqs = [len(linseqs[key]) for key in linseqs]
print('n_of_relevant_seqs', len(relevant_seqs))
print('n_of_all_seqs', sum(all_seqs))
print('diff', sum(all_seqs) - len(relevant_seqs))

print(orders)



with open('../../../relevant_seqs.txt', 'w') as file:  # Use.
    file.write(str(relevant_seqs))
    # file.write('Hi there!')

with open('../../../relevant_seqs.txt', 'r') as file:  # Use.
    # file.read('Hi there!')
    text = file.read()

saved_seqs = re.findall(r'A\d{6}', text)
print(saved_seqs)
print(len(saved_seqs))



# Make a random dataset:
# height = [3, 12, 5, 18, 45]
height = per_orders
# bars = ['A', 'B', 'C', 'D', 'Z']
bars = orders
y_pos = np.arange(len(bars))
# plt.ylabel =

# Create bars
# plt.bar(y_pos, height, label='num seq', zorder=0)




# plt.grid(linestyle='--', axis='y', alpha=0.7)
# minor_ticks = np.arange(0, 6000, 20)
# plt.set_yticks(minor_ticks, minor=True)
plt.grid(visible=True, which='both', axis='both', zorder=3)
threshold = 100
sporadity = 2
# def sparse(l: list): return l[:threshold]+l[threshold::sporadity]
# height = sparse(height)
# bars = sparse(bars)
# y_pos = sparse(y_pos)


plt.bar(y_pos, height, label='num seq', zorder=0)
# a.grid(visible=True, which='both', axis='both', zorder=3)

# Create names on the x-axis
plt.xticks(y_pos, bars, rotation='vertical')

plt.ylabel('number of sequences')
plt.xlabel('order')
plt.title('number of sequences per order')

# Show graphic
plt.show()
plt.clf()
