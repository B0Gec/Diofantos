# for i in range(9):
#     print((-1728)**i)


# ord 2
an = [1, 1]
an = [24, -896]
an = [1, -1]
c, d = -14, -1
c, d = -24, -2048
c, d = -48, 1024
c, d = -1, -1
print(an[0], f'\n{an[1]}')
for n in range(9):
    an += [c*an[-1] + d*an[-2]]
    print(an[-1])
