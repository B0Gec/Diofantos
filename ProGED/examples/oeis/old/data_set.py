import re
peset = 50
i = 5
i = 1
def line_pure(i):
    return  f"a_{{{i+1}}} & " + f"{i} & " + "".join([f"a_{{{j}}} & " for j in range(i, 0, -1)]) + "0 & "*(peset+1-1 - (i+1) ) + " \\\\"

def line(i, maxi=5):
    stringi = ( f"{i} & "  
         + "".join([f"a_{{{j-1}}} & " for j in range(i, max(0, i+1-maxi), -1)]) 
         + "0 & " * max(maxi+1-1 - (i+1), 0) + "\\cdots & "
         + "".join([f"a_{{{j-1}}} & " for j in range(max(i+1-(peset-3), 0), 0, -1)]) 
         + "0 & " * (3-max(i+1-(peset-3), 0)) + f"a_{{{i+1-1}}} & " 
         + " \\\\")  
    # print(type(stringi))
    return stringi

array = [line(i, 5) for i in range(1, (peset-1)+1)]
# cells = [len(re.findall('&', line(i))) for i in range(1, (peset-1)+1)]
# print(cells, len(cells))
# 1/0
# array = "".join(array)
# print(array[0:3])
for i in array[0:5]:
    # print(i[:100])
    print(i)
for i in array[-3:]:
    print(i)

# print('line52', line(52))
print('c'*51)

