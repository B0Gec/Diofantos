# MoadeeB and Diofantos

This is a repo hosting MoadeeB and [Diofantos](https://doi.org/10.3390/math12233745), two algorithms for **discovering exact equations**, e.g. from integer sequences.

They are hosted in a separate branches, in branch [Diofantos](https://github.com/B0Gec/Diofantos/tree/Diofantos) and [MoadeeB](https://github.com/B0Gec/Diofantos/tree/MoadeeB), respectively.

However, you are currently viewing the main branch `oeis`, which is a development branch for them.

For first-time users or non-developers, this branch is not recommended for use. Instead, refer to the branches listed above. 

Releases of this repository are equivalents to commits of the two branches mentioned above.

TL;DR: Following the git procedure below (_Get essential files via git_), you get the same files from the above release/branch.

# Diofantos

For the Diofantos algorithm, please visit the corresponding branch, together with the installation instructions:
     https://github.com/B0Gec/Diofantos/tree/Diofantos

For Diofantos, you can cite this paper: https://doi.org/10.3390/math12233745

# MoadeeB

For the MoadeeB algorithm, please visit the corresponding branch, together with the installation instructions:
https://github.com/B0Gec/Diofantos/tree/MoadeeB


## How to set up MoadeeB or Diofantos

To reproduce results, one could use container as an alternative to installing Python dependencies listed below.

Otherwise, go ahead and install the dependencies in a new python environment.

For MoadeeB, you will also need the CoCoA software as described in Prerequisites below.

After that, you can clone the repository, but I recommend getting only (instead of all 7GB results) the following files:

    exact_ed.py
    diophantine_solver.py
    doones.py
    linear_database_newbl.csv
    cores_test.csv
    sindy_oeis.py
    gather_results.py
    mb_oeis.py
    mb_wrap.py
    cocoa_location.py 
    real-bench
    real_world_bench.py
    real_world_bench_evaluate.py


The list above is not checked so please make sure there are no import errors.

### Get essential files via git

I find it easiest to use git to make an efficient clone to automatically download the essential files to try out the method. 
Run these commands in terminal, while replacing <branch> with Diofantos or MoadeeB (end of git URL and repo directory remains "Diofantos" in both cases): 
```bash
git clone --single-branch --branch <branch> -n --depth=1 --filter=tree:0 https://github.com/B0Gec/Diofantos
cd Diofantos
git restore --source HEAD exact_ed.py diophantine_solver.py doones.py cores_test.csv sindy_oeis.py gather_results.py mb_oeis.py mb_wrap.py cocoa_location.py real-bench real_world_bench.py real_world_bench_evaluate.py
```

In the end, download `linear_database_newbl.csv` manually (182.8MB) from my Zenodo repository (https://doi.org/10.5281/zenodo.13767012), since it is stored as git lfs (large files) and they seem to be hard to download as a single file.


And ignore files under the GitHub "Assets" section of the GitHub's release page.

## Simple example of execution of MoadeeB/Diofantos in terminal:

```bash
python doones.py --task_id 14 --exper_id output_dir
```

will produce the output file `results/output_dir/00014_A000045.txt` with similar content:

```txt
While total time consumed by now, scale:15/164, seq_id:A000045, order:10 took:
 0.6 seconds, i.e. 0.01 minutes or 0.0 hours.
CORELIST True, SINDy False, GROUND_TRUTH False, SINDy_default True
Library: n, max_order 10, threshold: 0.1

by degree: 1 and order: 2. 
A000045: 
a(n) = a(n - 2) + a(n - 1)
truth: 


  -  checked against website ground truth.     
True  -  "manual" check if equation is correct.
```

This (Fibonacci) example was tested on 26.2.2024 and 18.2.2025.

## Apptainer/Singularity container:
- Results from paper can be reproduced by running the doones.py file from python from the Singularity container obtained 
  from the Singularity Hub in the following way:
- `apptainer remote add --no-login SylabsCloud cloud.sycloud.io`
- `singularity remote use SylabsCloud`
- `singularity pull library://bogec/diofantos/oeis:latest`
- run e.g.: `~/ProGED_oeis$ singularity exec oeis_latest.sif python3 doones.py --task_id 13 --exper_id reproduced_experiment`

## Experiments
- database of _linrec_ sequences: `linear_database_newbl.csv`
- database of _core_ sequences: `cores_test.csv`
- script for running MoadeeB, Diofantos and SINDy-based approaches: `doones.py`
- [Diofantos](https://doi.org/10.3390/math12233745) code: `exact_ed.py`
- MoadeeB code: `mb_oeis.py`, `mb_wrap.py`
- SINDy based approaches: `sindy_oeis.py`
- Results: directories `results` (also some in `results_oeis`)
    - results/goodmb  (MoadeeB only):
      - `mblinbs50`   linrec
      - `mbcor`      core
      - `mbtmord20r`  TM-OEIS n_input=15 (n_pred=1 and 10)
      - `mbtmN25`     TM-OEIS n_input=25 (n_pred=1 and 10)
    - results/good  (Diofantos and sindy only):
      - `dilin`      Diofantos linrec
      - `dicorrep`   Diofantos core
      - `silin`      SINDy-tuned linrec
      - `sicor1114`  SINDy-tuned core
      - `sdlin`      SINDy-default linrec
      - `sdcor2`     SINDy-default core
      - `transfoeis_acc2` Diofantos TM-OEIS n_input=25 (and n_pred=1 and 10)
      - `n15_acc`         Diofantos TM-OEIS n_input=15 (and n_pred=1 and 10)


## Features
- algebraic equations with variables `n`, `a(n-k)` for all *k* up to chosen order and
their combinations up to degree *d*.

## Dependencies
- [Diophantine](https://pypi.org/project/Diophantine/)
- numpy
- scipy
- sympy
- pytest (optional)

## Other prerequisites
We need the CoCoA software [apcocoa](https://apcocoa.uni-passau.de) containing Moeller-Buchberger algorithm (function IdealOfPoints).

After downloading, write the location of directory `apcocoa2_unix` into variable `cocoa_location`
inside of the `cocoa_location_secret.py` file, e.g. `cocoa_location_secret = '~/Documents/CoCoA/'`.



