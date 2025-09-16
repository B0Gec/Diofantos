"""open json file and print response (in not obscured way)"""

import os
import json

if __name__ == '__main__':
    DO_WRITE = False
    # DO_WRITE = True
    out_experiment = 'obat-cor25expert-unjsoned/'

    in_dir = 'results/'
    experiment = 'obat-cor25expert/'
    files = os.listdir(in_dir + experiment)
    print(files)
    for filename in files[:200]:
        # filename = files[0]
        print(filename)
        # 1/0

        json_file = open(in_dir + experiment + filename, 'r')
        # print(json_file)
        loaded = json.load(json_file)
        # print(loaded)
        # print(loaded['response'])

        ### WARNING!! WRITING OUT FILES!
        if DO_WRITE:
            txt_file = open(in_dir + out_experiment + filename + '.txt', 'w')
            txt_file.write(loaded['response'])
