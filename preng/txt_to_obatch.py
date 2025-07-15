qs = open('data/test_cores25.txt').readlines()
# print(qs[:3])

for q in qs:
    # print(q)
    # 1/0
    content = q[len('[INST] '):-len(' [/INST] \n')]
    # print(content)
    prompt = f'{{"role": "user", "content": "{content}" }}'
    print(prompt)


