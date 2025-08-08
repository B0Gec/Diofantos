zshot = [58, 213, 321, 106, 123]
diof =  [61, 249, 392, 155, 149, 71]
mb =    [57, 259, 408, 168, 157, 73]

# 213/500   1k  # 321/1000  2k
# 106/1000  3k  # 123/1000  4k

total = 200 + 500 + 3*1000 + 300
# print(10 * sum(zshot)/total, '%')
for met in [zshot, diof, mb]:
    print(100 * sum(met)/total, '%')
