import re
# re.findall(fi
# """"""'PRIMARY' (1):'VOLUME' (HB4):'THER' (1):T_gas[1]"""
# )o
#
raw_data = "'PRIMARY'\ (1):'VOLUME' (CB1):'THER' (1):T_gas[1]"

found = re.findall(r"""'PRIMARY' \(1\):.+:T_gas\[1\]""", raw_data)
# found = re.findall(r"""'PRIMARY\(1\):.+:T_gas\[1\]""", raw_data)
#found = re.findall(r"""'PRIMARY' \(1\):.+:T_gas\[1\]""", raw_data)
found = re.findall(r"""'PRIMARY'\\ \(1\):\w[1cea45x]{1,2}(.*):T_gas\[1\]""", raw_data)
# found = re.findall(r"""'PRIMARY""", r"""'PRIMARY""")
# found = re.findall(r"""'PRIMARY.+""", raw_data)
print(found)
# print(found[0][0] + found[0][1])
