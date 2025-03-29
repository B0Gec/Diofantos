"""
File that scrapes webpage:
    http://oeis.org/wiki/Index_to_OEIS:_Section_Rec
for linearly recursive sequences.
Good for discovering exact linear integer equations by algorithm that solves
diophantine equations.

list of ids.
for id in list:
    seq = blist[id]

"""
import os, sys
import requests, re, time
import pandas as pd
from bs4 import BeautifulSoup

from exact_ed import timer

if __name__ == '__main__':

    url = "http://oeis.org/wiki/Index_to_OEIS:_Section_Rec"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, '
                      'like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
    }
    f = requests.get(url, headers = headers)
    # f = requests.get(url)
    # print(f.content)
    # 1/0
    soup = BeautifulSoup(f.content, 'html.parser')
    # print(soup.prettify())
    # print(soup)


    # a. find all oeis ids
    ids = soup.find_all('a', text=re.compile(r'A\d{6}'))
    # ids = soup.find_all(text=r'A\w{6}')
    # ids_txt = [i.text for i in ids]
    ids_txt = ids
    print(len(ids_txt))  # 2022.12.02: 34384
    print(len(ids))
    print(len(set(ids_txt)))  # 2022.12.02: 34371  (all good, i.e. doublets)
    # Current total success (33787/34371, i.e. 584 lost scrapped into csv 2022.12.02).
    # linseqs:  34384 or 34371  (100%)
    # csv:  34384 or 34371  (100%)


    # # Check for doublets:
    # #   - (list vs set: 34384 vs. 34371) checked out: some sequences have e.g. order 3 and 4. So all good.
    # counter = dict()
    # for id_ in ids_txt:
    #     # if ids_txt[id_] += 1
    #     # counter[id_] = 1 \
    #     if id_ not in counter:
    #         counter[id_] = 1
    #     else:
    #         counter[id_] += 1
    # doublets =  [(k, i) for k, i in counter.items() if i>1]
    # print(doublets)
    # print(len(ids))


    # b. get webpage tree or dictionary of key: [list of sequences]
    """
    linseqs = dictionary of orders as keys and values as lists of seqs of linear recursive order.
    idea: 
      linseqs -> seqsd = dict( id: seq) -> pd.Dataframe(seqsd).sorted.to_csv() 
     
    for seq in seqs: bfile2list
    """


    # start = 100
    start = 13800
    scale_tree = 10
    # scale_tree = 1000
    # scale_tree = 30000
    # scale_tree = 10**5
    # scale_tree = 40000
    # scale_tree = 25000
    scale_tree = 1000000
    # print(scale_tree)
    # linseqs['7'] = [None]
    # scale_tree = 13900

    # linseqs['131071'] = [None]
    start = 0
    # scale_tree = 10**6

    # order = '8'
    # linseqs['8'] = [None]


    verbosity = False
    # verbosity = True

    linseqs = dict()
    for id in ids[start:scale_tree]:
        parent = id.parent
        truth = re.findall(r'\([-\d, \{\}\.\"\']*\)', parent.text)
        if truth == []:
            if verbosity:
                print('first empty:', parent.text)
            truth = re.findall(r'\(-*\d[-, \{\}\w\'\"\.\d\(\)]*\):', parent.text)
        # if truth == []:
        #     print(parent.text)
        #     truth = re.findall(r'\((-*\d[, \{\}\w\'\"\.\d\(\)]*).+\):', parent.text)
        #     print(truth)
        if truth == []:
            print(parent.text)
            truth = [truth]
        truth = truth[0]

        if parent.previous_sibling is None:
            previous = parent.parent.previous_sibling.previous_sibling
            if previous.name == 'h4':
                title = previous.text
                order = re.findall(r'(\d+)', title)[0]
                if order not in linseqs:
                    linseqs[order] = [(truth, id.text)]
                else:
                    linseqs[order] += [(truth, id.text)]
            else:
                linseqs[order] += [(truth, id.text)]
                if previous.name not in linseqs:
                    pass
                    # linseqs[previous.name] = [previous]
                else:
                    pass
                    # linseqs[previous.name] += [previous]
        else:
            linseqs[order] += [(truth, id.text)]

    #  b.1 check linseqs
    print(len(linseqs))
    # print([(seqs, len(linseqs[seqs])) for seqs in linseqs])
    print(sum(len(linseqs[seqs]) for seqs in linseqs))

    ids_list = []
    for _, seqs in linseqs.items():
        ids_list += seqs
    print(ids_list, len(ids_list))

    reconst = []
    for seqs in linseqs.values():
        reconst += seqs
    print(f'reconstructed: {len(reconst)}')
    ids_raw = {id.text for id in ids[start:scale_tree]}
    print(f'wanna reconstruct: {len(ids_raw)}')
    reconsts = set(reconst)
    print(set(ids_raw).difference(reconsts))
    # print(reconst[:14])
    # print(prob in reconsts)


    till_order = 10**16
    till_order = 10
    if verbosity:
        for order, seqs in list(linseqs.items()):
            if int(order) < till_order:
                print(f'order: {order}')
                for truth, seq in seqs:
                    # print(int(order) * "  " + f'\\_ {seq}   order: {order}')
                    print("  " + f'\\_ {truth}: {seq}   order: {order}')




    # c.  downloading 4realz

    now = time.perf_counter()

    if os.getcwd()[-11:] == 'ProGED_oeis':
        from ProGED.examples.oeis.scraping.downloading.download import bfile2list
    else:
        from scraping.downloading.download import bfile2list

    csv_filename = "../../../linear_database.csv"


    # seqs_dict = dict()
    to_concat = []
    scale_per_ord = 1000000
    scale_per_ord = 100
    SCALE_COUNT = 10
    SCALE_COUNT = 15000
    # SCALE_COUNT = 20
    counter = 0
    escape = False
    PERIOD = 200
    # PERIOD = 5

    print(f'scale_per_ord:{scale_per_ord}')
    print(f'SCALE_COUNT:{SCALE_COUNT}')
    print(f'PERIOD:{PERIOD}')
    # scale_per_ord = 10
    MAX_SEQ_LENGTH = 200
    # MAX_SEQ_LENGTH = 6
    # MAX_SEQ_LENGTH = 15

    PARALLELIZE = True
    # PARALLELIZE = False
    PARALLEL_BATCH = 5000
    # PARALLEL_BATCH = 5
    INDEX = 0

    flags_dict = {argument.split("=")[0]: argument.split("=")[1]
                  for argument in sys.argv[1:] if len(argument.split("=")) > 1}
    INDEX = int(flags_dict.get("--index", INDEX))
    PARALLEL_BATCH = int(flags_dict.get("--batch", PARALLEL_BATCH))
    csv_filename = csv_filename[:-4] + str(INDEX) + csv_filename[-4:]
    print(f'INDEX:{INDEX}, PARALLEL_BATCH:{PARALLEL_BATCH}, csv_filename:{csv_filename}')

    if PARALLELIZE:
        # sorted_ids = sorted(list(set(ids_list)))[(INDEX*PARALLEL_BATCH):((INDEX+1)*PARALLEL_BATCH)]
        sorted_ids = sorted(ids_list, key=(lambda pair: pair[1]))
        csv_ids = sorted_ids[(INDEX * PARALLEL_BATCH): ((INDEX + 1) * PARALLEL_BATCH)]
        for truth, id in csv_ids:
            # print(id)
            if id == 'A001076':
                print(id)
            if id == 'A001076.1':
                print(id)
            to_concat += [pd.DataFrame({id: [truth] + [int(an) for an in bfile2list(id, max_seq_length=MAX_SEQ_LENGTH)]})]
            counter += 1

            if counter % PERIOD == 0:
                timer(now, f"Scraping one of the parallel batches of {counter} sequences ")
                print(f"counter: {counter}")
                df = pd.concat(to_concat, axis=1)
                df.sort_index(axis=1).to_csv(csv_filename, index=False)
                # df.sort_index(axis=1).to_csv(csv_filename[:-4] + str(INDEX) + csv_filename[-4:], index=False)
                print(f"{counter} sequences written to csv")
                print("check file: number of ids, file size?")
                # to_concat = []
    else:
        for order, ids in linseqs.items():
            if verbosity >= 2:
                print(order)
                print(ids[:scale_per_ord])
            for id in ids[:scale_per_ord]:
                # print([type(i) for i in [idii, idsii, orderii]])

                if counter <= SCALE_COUNT:
                    to_concat += [pd.DataFrame({id:  [int(an) for an in bfile2list(id, max_seq_length=MAX_SEQ_LENGTH)]})]
                    counter += 1
                    if counter % PERIOD == 0:
                        timer(now, f"Scraping {counter} sequences ")
                        print(f"counter: {counter}")
                        df = pd.concat(to_concat, axis=1)
                        df.sort_index(axis=1).to_csv(csv_filename, index=False)
                        print(f"{counter} sequences written to csv")
                        print("check file: number of ids, file size?")
                        # to_concat = []


            # seqs_dict[idi] = bfile2list(idii, max_seq_length=100)
    # pd.DataFrame(seqs_dict).sort_index(axis=1).to_csv(csv_filename, index=False)

    if to_concat != []:
        df = pd.concat(to_concat, axis=1)
    df.sort_index(axis=1).to_csv(csv_filename, index=False)

    def fix_cols(df: pd.DataFrame) -> list:
        # check weird columns names:
        errors = []
        for id in df.columns:
            weird_id = re.findall(r'A\d{6}\.\d+', id)
            if weird_id != [] or len(id)>7 or id[0] != 'A' or int(id[1]) not in (0, 1, 2, 3):
                df = df.drop(id, axis=1)
                print('weird_id:', weird_id)
                errors += [weird_id]
        return df, errors

    df = fix_cols(df)[0]
    df.sort_index(axis=1).to_csv(csv_filename, index=False)
    csv_filename_real = csv_filename
    # ef.sort_index(axis=1).to_csv(csv_filename, index=False)
    # # side effect are floats in csv, but maybe its unavoidable \_-.-_/
    # magnitude = [f'{min(df[col]):e}  ' + f'{max(df[col]):e}' for col in df.columns]
    # types = [type(df[col][0]) for col in df.columns]
    # for i in magnitude:
    #     print(i)
    # for i in types:
    #     print(i)


    # # Concatenate parallelized df-s
    # csv_filename = "linear_database.csv"
    # if os.getcwd()[-11:] == 'ProGED_oeis':
    #     csv_filename = "ProGED/examples/oeis/" + csv_filename
    # parallels = []
    # for index in range(7):
    #     df = pd.read_csv(csv_filename[:-4] + str(index) + csv_filename[-4:], low_memory=False)
    #     print(f'read csv w/ index:{index}')
    #     parallels += [df]
    # df = pd.concat(parallels, axis=1)
    # df.sort_index(axis=1).to_csv('linear_database.csv', index=False)
    # #
    # df = fix_cols(df)[0]
    # fix_cols(df)[1]





    # # # after download:
    # csv_filename = "linear_database0.csv"
    if os.getcwd()[-11:] == 'ProGED_oeis':
        csv_filename = "ProGED/examples/oeis/" + csv_filename

    print(csv_filename)
    check = pd.read_csv(csv_filename, low_memory=False)


    print("Read file from csv:")
    print(check)
    print(check.head())
    print(check.info)

    print(len(list(set(check.columns))))

    print(f" - - - -> Created csv: {csv_filename_real} <- - -")


    print('Checking for weird col names returned list:', fix_cols(check)[1])


    timer(now)

    # to_conc = [{key: seq} for key, seq in linseqs.items()]
    # cutoff = min(len(seq) for _, seq in seqs_dict.items())
    # for id_, seq in seqs_dict.items():
    #     print(id_, len(seq), seq)
    # cutoff
    # for orderii, idsii in linseqs.items():
    #     for idii in idsii[:scale]:
    #         seqs_dict[idii] = seqs_dict[idii][:cutoff]
    #
