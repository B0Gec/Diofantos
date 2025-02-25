from exact_ed import poly_combinations, dataset, grid_sympy

combs = poly_combinations('non', 2, 2)
print(combs)

seq = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

# ds = dataset(seq, d_max=2, max_order=2, library='n')
ds = dataset(seq, d_max=2, max_order=2, library='non')
print(ds)
print(ds[1])
print(ds[1][0, :])
# 1/0
arr = ds[1]

for n in range(arr.rows):
    # print(  f'{arr[n, :][0]}  & {arr[n, :][1]} & {arr[n, :][2]} &  {arr[n, :][3]} '
    #         f'&  {arr[n, :][1]}^2 & {arr[n, :][1]} \cdot {arr[n, :][2]} & {arr[n, :][1]} \cdot {arr[n, :][3]} '
    #         f'&  {arr[n, :][2]}^2 & {arr[n, :][2]} \cdot {arr[n, :][3]} & {arr[n, :][3]}^2  \\\\')
    print(  f'{arr[n, :][0]}  & {arr[n, :][1]} & {arr[n, :][2]} &  '
            f'{arr[n, :][1]} ^2 & {arr[n, :][1]} \cdot {arr[n, :][2]} '
            f'&  {arr[n, :][2]}^2  \\\\')
    # print(ds[1][n, :])



'1 & 3 ^ 3 & 1 & 1 \cdot 1 & 1 & 3 \cdot 0 ^ 2 \\'
'1 & 4 ^ 3 & 2 & 2 \cdot 1 & 1 & 4 \cdot 1 ^ 2 \\'
'1 & 5 ^ 3 & 3 & 3 \cdot 2 & 2 & 5 \cdot 1 ^ 2 \\'
'1 & 6 ^ 3 & 5 & 5 \cdot 3 & 3 & 6 \cdot 2 ^ 2 \\'
'1 & 7 ^ 3 & 8 & 8 \cdot 5 & 5 & 7 \cdot 3 ^ 2 \\'
