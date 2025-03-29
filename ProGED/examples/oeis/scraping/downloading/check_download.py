import re
import pandas as pd
# from save_new_bfiles import bseqs  # before csv

## -- Check scrap against gzipped oeis database -- ##
def check_scrap(seqs_dict: dict, is_bfile=False):
    # seqs = seqs_flat
    file2 = open("../selection-process/stripped_oeis_database.txt", "r")
    original = file2.read()
    file2.close()
    counter = 1
    for id_, seq in seqs_dict.items():
        # seq = seqs_dict[seq_id]
        # seq_id = "A000002"
        compare = re.findall(id_+".+\n", original)
        str_seq = id_ + " ,"
        # str_seq += "".join([str(term) + "," for term in seq])
        for term in seq:
            str_seq += str(term)+","
        str_seq += "\n"
        str_seq = [str_seq]
        orig, scraped = compare[0], str_seq[0]
        # print(orig, "this is what I found in original database. Compare with scraped:")
        # print(scraped)
        if not is_bfile:
            print("I can see, you are not using b-files. Those are more longer.")
            bool_ = orig == scraped
            assert orig == scraped
            print(counter, "Correct scrapping!!! found it" if bool_ else "scrapping FAILED!!!")
            assert len(orig) == len(scraped)
            print(len(orig), len(scraped))
        else:
            # print("Checking b-files! Let's see.")
            length = min(len(orig)-2, len(scraped)-2)  # Avoid \n.
            orig_cut = orig[:length]
            scraped_cut = scraped[:length]
            print(counter, id_, 'all good. string length:', length)
            assert len(orig_cut) == len(scraped_cut)
            assert orig_cut == scraped_cut
            bool_ = orig_cut == scraped_cut
            # print(counter, "Correct scrapping!!! found it" if bool_ else "scrapping FAILED!!!")
            if not bool_:
                print("scrapping FAILED!!!")
                print("orig:", orig_cut)
                print("scra:", scraped_cut)
                # print("orig:", orig, end="")
                # print("scra:", scraped, end="")
        counter += 1
    print("Seems scrapping is correct. Checking is done.")
    return
# check_scrap()
# check_scrap(bseqs, is_bfile=True)
# check_scrap(bseqs, is_bfile=True)
# print("end")

def check_out(is_bfile=False, has_titles=1, csv_filename: str ='oeis_selection.csv'):

    df = pd.read_csv(csv_filename)[has_titles:]
    # danger! in next line we should convert string terms to integers.
    bseqs = {id_: [int(term) for term in seq] for id_, seq in df.items()}

    # basic info, preview:
    # print(len(seqs), type(seqs), [len(seq) for _, seq in seqs.items()],
    #     [seq for _, seq in seqs.items()][0])  # preview
    # print(len(set(seqs)))

    from selection import basic_info
    basic_info(bseqs)
    check_scrap(bseqs, is_bfile=True)
    return

# check_out(csv_filename='oeis_dmkd.csv')
# check_out(csv_filename='../../linear_database.csv')
