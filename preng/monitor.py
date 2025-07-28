"""Monitor how many jobs and which were successfully finished."""


loc = 'results/obat-dasco25-10k'

import os

ls = sorted(os.listdir(loc))
print(ls)

print(f'Last finished job: {ls[-1]}')

print(f'Number of successful jobs: {len(ls)}')

success_task_ids = [file[:5] for file in ls]
print(f'Successful jobs: {success_task_ids}')

fails = [y for i in range(10000) if (y:=f'{i:0>5}') not in success_task_ids]
print(f'fails: {fails}')

fail_bins_detailed = [(f'{i*100}+', (b:=[y for f in fails if i*100 <= (y:= int(f)) and y < (i+1)*100 ]), len(b), i*100, (i+1)*100) for i in range(100)]
fail_bins = {f'{i*100}-{(i+1)*100}': len([y for f in fails if i*100 <= (y:= int(f)) and y < (i+1)*100 ]) for i in range(100)}

print(f'Fail bins detailed: {fail_bins_detailed}')
print(f'Fail bins: {fail_bins}')
# pretty print:
for key, value in fail_bins.items():
    print(f'{key}: {value}')


print(f'Latest results: {ls[-15:]}')
