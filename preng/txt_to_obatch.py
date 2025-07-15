"""Generate batches for 0-shot experiments."""

### First method:
qs = open('data/test_cores25.txt').readlines()
# print(qs[:3])

# for q in qs:
#     # print(q)
#     # 1/0
#     content = q[len('[INST] '):-len(' [/INST] \n')]
#     # print(content)
#     prompt = f'{{"role": "user", "content": "{content}" }}'
#     print(prompt)


### Second (sophisticated) method:

template = open('trash/template_markdown.txt').read()
# print(template)
# print(' --- end --- ')

# print(template.replace('**[Paste your integer sequence here]**', '1, 4, 9, 16'))


# 1/0

for q in qs[105:110]:
    # print(q)
    # 1/0
    seq = q.split(': ')[1][:-len(' [/INST] \n')].replace(',', ', ')
    # content = q[len('[INST] '):-len(' [/INST] \n')].split()
    # print(seq)
    content = template.replace('**[Paste your integer sequence here]**', seq)
    content = content.replace('\n', '\\n')

    # print(content)
    prompt = f'{{"role": "user", "content": "{content}" }}'
    print(prompt)
    # 1/0


# whole prompt with examples (105-110): succes rate: 2/3  (one was MB hard)


