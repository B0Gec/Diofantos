from functools import reduce as foldl

# sez = [isfail,
#         ]
#
# all = fail + nonmanual + nonid + idoeis
#
# fail = not we found
# manually = is_checked
#
# we_found


dic = {'a': (True, False, False, True),
       'b': (False, False, True, False),
       'c': (False, True, False, True),
       }
l = ['b', 'c', 'a',]

def f(aggregated: tuple, list_item: str):

    # now -> f, m, i, o
    # idoeis = id_reconst
    # nonid = is_checked and not is_reconst
    # nonmanual = we_found and not is_checked
    # fail = not we_found

    # summand = [f, m, i, o]
    to_add = dic[list_item]  # tuple
    # f, m, i, o = aggregated
    # print('to_add:', to_add)

    # fs, ms, is, os = aggregated

    zipped = zip(aggregated, to_add)

    # return [ f+fs, m+ms, i+is, o+os for fs, ms, is, os in before]
    return tuple(map(lambda x: x[0] + x[1], zipped))


print(foldl(f, l, (0, 0, 0, 0)))
print(f((1,2,3,4,), 'c'))


# fails, nonmanuals, nonids, ioeis =
#     fold f (0, 0, 0, 0) files
#
#
# fails = fails + no job
