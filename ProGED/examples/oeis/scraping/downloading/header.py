from urllib import request
import pandas as pd
import re
import time

start = time.perf_counter()
def header(id_):
    """Download title from HTML of the sequence of given id."""
    
    search = request.urlopen(f"https://oeis.org/search?q=id%3a{id_}&fmt=data")
    header = search.read().decode()
    # print(header)
    total = re.findall(r'''<a href=\"/A\d{6}\">A\d{6}</a>
                    
                    
                    <td width=5>
                    <td valign=top align=left>
                    ((.+\n)+)[ \t]+<td width=\d+>''', header)
    title = total[0][0]
    return [title]
# print(header("A000001"))


titles_filename = "../selection-process/titles.csv"
def download_headers(titles_filename=titles_filename, first_columns=-1):
    ids = pd.read_csv("../selection-process/oeis_selection.csv").columns[:first_columns]
    titles = {id_: header(id_) for id_ in ids}
    for id_, title in titles.items():
        print(id_, title)

    df = pd.DataFrame(titles)
    df.to_csv(titles_filename, index=False)
    return
# download_headers(titles_filename, -1)
# download_headers(titles_filename, 4)
# print(time.perf_counter() - start)
# __name__ = "__main__"

# post download:
if __name__ == "__main__":
    titles = pd.read_csv(titles_filename, index_col=0)
    print(titles.shape)
    print(titles)
    for id_, title in titles.items():
        print(id_, len(title[0]))
    print(min([len(title[0]) for _, title in titles.items()]))
