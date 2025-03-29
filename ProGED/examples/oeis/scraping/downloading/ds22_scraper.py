#
# # import pandas as pd
# import re
# # import time
#
# ds_program = "https://ds2022.sciencesconf.org/resource/page/id/12"
# search = request.urlopen(ds_program)
#         # f"https://oeis.org/search?q=id%3a{id_}&fmt=data")
# header = search.read().decode()
# print(header)
# # 1/0
# total = re.findall(
# # r'''<a href=\"/A\d{6}\">A\d{6}</a>
#
#
# #                 <td width=5>
# #                 <td valign=top align=left>
# #                 ((.+\n)+)[ \t]+<td width=\d+>''',
# # "
# # pdf
# # r'''<a href="https://nextcloud.inrae.fr/s/7aqRXFPQK3W3pXc">pdf</a>''',
# # r'''<a href="https://nextcloud.inrae.fr/s/\w{3,20}">pdf</a>''',
# # r'''<p style="line-height: 1.38; text-align: justify; margin-top: 0pt; margin-bottom: 0pt;" dir="ltr"><em><span style="font-size: 11pt; font-family: Arial; color: #000000; background-color: transparent; font-weight: 400; font-variant: normal; text-decoration: none; vertical-align: baseline; white-space: pre-wrap;">Shapley Chains: Extending Shapley values to Classifier Chains - F </span></em><span style="font-size: 11pt; font-family: Arial; color: #000000; background-color: transparent; font-weight: 400; font-variant: normal; text-decoration: none; vertical-align: baseline; white-space: pre-wrap;">(<a href="https://nextcloud.inrae.fr/s/7aqRXFPQK3W3pXc">pdf</a>)</span></p>''',
# r'''<a href="https://nextcloud.inrae.fr/s/7aqRXFPQK3W3pXc">pdf</a>)</span></p>''',
#     header)
# print(total)
# print(len(total))
#

from urllib import request
import requests
from bs4 import BeautifulSoup
# url = "https://www.rottentomatoes.com/top/bestofrt/"
ds_program = "https://ds2022.sciencesconf.org/resource/page/id/12"
# url = ds_program
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
# }
# f = requests.get(url, headers = headers)
ds = requests.get(ds_program)
print(ds.content)

# 1/0
# movies_lst = []
# soup = BeautifulSoup(f.content, 'lxml')
soup = BeautifulSoup(ds.content, 'html.parser')
print(soup.prettify())

print(soup)

import re
# vseh paperjev 38 al 39
# tag = soup.find_all('a', text='pdf')
# tag = soup.find_all(text='pdf')
# search = soup.find_all(href=re.compile('nextcloud'))
search = soup.find_all(href=re.compile('nextcloud'))

cut = 100

filenames = []
for n, pdf in enumerate(search[:cut]):
    # print(n)
    title = pdf.parent.text[:-6]
    if len(title) < 5:
        title = pdf.parent.parent.text[:-6]
        if len(title) < 5:
            title = pdf.parent.parent.text[:-6]
        if len(title) < 5:
            title = pdf.parent.parent.text[:-6]

        # for item in search:
    # [item for item in search][0]
    # print(item)
    # item = search[0]

    print(pdf['href'])
    pdf_url = pdf['href']
    pdf_soup = BeautifulSoup(requests.get(pdf_url).content, 'html.parser')
    search = pdf_soup.find(href=re.compile('nextcloud'))
    download_url = search['href']
    original_filename = download_url.split('/')[-1][:-4]
    filename = original_filename + '--' + title + '.pdf'
    print(filename)
    filenames.append(filename)

     ### ##  request.urlretrieve(download_url, filename)

    print(n+1)

print(filenames)
# check uniqueness:
bag = set()
for name in filenames:

# name = filenames[0]
# print(name)
    item = re.findall(r'DS22_paper_(\w+)--', name)[0]
# item = re.findall(r'......', name)
#     print(item)
    bag.add(item)
    print(item)
print(f'len before:{len(filenames)}')
print(f'len after:{len(bag)}')
for i in sorted(bag):
    print(i)
# print(sorted(bag))


# search = pdf_soup.find_all(class_='primary button')
