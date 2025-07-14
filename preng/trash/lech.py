import requests

import datetime

now = datetime.datetime.now()
print(now)

url = open('data/test_url.txt', 'r').read().strip('\n')
print(url)
q = "Could you give me a recursive equation in a form of a Python code for the following number sequence: 1,3,10,35,126,462,1716,6435,24310,92378,352716,1352078,5200300,20058300,77558760,300540195,1166803110,4537567650"
# q = "Could you give me a recursive equation in a form of a Python code for the following number sequence: 1,1,2,3,5,8,13,21 ?"
mathstral = "mathstral:7b-v0.1-fp16"
cogito = "cogito:70b"
phi = "phi4-reasoning:14b-plus-fp16"
qwen3 = "qwen3:32b"

data = {
    # "model": mathstral,
    # "model": cogito,
    # "model": phi,
    "model": qwen3,
    "prompt": q,
    "stream": False,
    # "think": False,
    # "think": True
}

headers = {"Content-Type": "application/json"}
response = requests.post(url, json=data, headers=headers)

result = response.json()

print(result['response'])
print()
print(result['model'])
# print()
# print(result['duration'])

print(datetime.datetime.now())
