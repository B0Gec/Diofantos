import openai
import os

pgdir = './ProGED/'
print(os.listdir(pgdir))
# 1/0
files = [
        'README.md',
        # 'ProGED/equation_discoverer.py',
        ]
code = dict()

for i in files:
    f = open(pgdir + i, 'r')
    source_code = f.read()[:-1]
    code[i] = source_code
    f.close()

print(code, type(code), len(str(code)))

# def crawl(pgdir, subenty):
    
#     for i in os.listdir[pgdir]:
#         if os.isdir(pgdir + i):


cg = False
# cg = True
if cg:
    fkey = open(".api_key", 'r')
    api_key = fkey.read()[:-1]
    fkey.close()

    openai.api_key = api_key

    completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
        # {"role": "user", "content": "Tell the world about the ChatGPT API in the style of a pirate."}
        # {"role": "user", "content": f"Write me a python script to perform equation discovery or symbolic regression task with the softwere called ProGED which source code is presented by the following dictionary: {code}."}
        {"role": "user", "content": f"How should I run ProGED to discover equations from dataset in my .csv file? Where ProGED instructions are here: {code}."}
      ]
    )

    print(2)
    print(completion.choices[0].message.content)
    print(3)
