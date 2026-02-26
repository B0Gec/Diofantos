import glob
import hashlib


def shasum(files_pattern):
    sha1 = hashlib.sha1()

    for filename in sorted(glob.glob(files_pattern)):
        with open(filename, "rb") as f:
            sha1.update(f.read())

    return sha1.hexdigest()


if __name__ == '__main__':
    print(' '*45, shasum("EEDBench/polys/pds*.csv"))
