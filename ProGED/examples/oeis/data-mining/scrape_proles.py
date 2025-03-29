filename = '../results/result50kscale40terms.txt'
import os
print(2)
if os.getcwd()[-11:] == 'ProGED_oeis':
    filename = 'ProGED_oeis/examples/oeis/' + filename
outputfile = open(f"{filename}", "r")
print(os.getcwd())
print(3)
results = outputfile.read()
print(4)
import re
found = re.findall("nekaj", "nekaj nekaj ali dela")
found = re.findall("We found an equation..", results)
found = re.findall("NO EQS", results)
print(found)
print(len(found))

found2 = re.findall("We found an equation..", results)
print(found2)
print(len(found2))
print(len(found) + len(found2))

