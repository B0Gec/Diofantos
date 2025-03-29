
from urllib import request
# import pandas as pd
import re
# import time

ds_program = "https://ds2022.sciencesconf.org/resource/page/id/12"
search = request.urlopen(ds_program)
        # f"https://oeis.org/search?q=id%3a{id_}&fmt=data")
header = search.read().decode()
print(header)
# 1/0
total = re.findall(
# r'''<a href=\"/A\d{6}\">A\d{6}</a>
                
                
#                 <td width=5>
#                 <td valign=top align=left>
#                 ((.+\n)+)[ \t]+<td width=\d+>''', 
# "
# pdf
# r'''<a href="https://nextcloud.inrae.fr/s/7aqRXFPQK3W3pXc">pdf</a>''',
# r'''<a href="https://nextcloud.inrae.fr/s/\w{3,20}">pdf</a>''',
# r'''<p style="line-height: 1.38; text-align: justify; margin-top: 0pt; margin-bottom: 0pt;" dir="ltr"><em><span style="font-size: 11pt; font-family: Arial; color: #000000; background-color: transparent; font-weight: 400; font-variant: normal; text-decoration: none; vertical-align: baseline; white-space: pre-wrap;">Shapley Chains: Extending Shapley values to Classifier Chains - F </span></em><span style="font-size: 11pt; font-family: Arial; color: #000000; background-color: transparent; font-weight: 400; font-variant: normal; text-decoration: none; vertical-align: baseline; white-space: pre-wrap;">(<a href="https://nextcloud.inrae.fr/s/7aqRXFPQK3W3pXc">pdf</a>)</span></p>''',
r'''<a href="https://nextcloud.inrae.fr/s/7aqRXFPQK3W3pXc">pdf</a>)</span></p>''',
    header)
print(total)
print(len(total))
