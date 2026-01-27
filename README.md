# MoadeeB

MoadeeB - M&Ouml;eller-Buchberger Algorithm based Discovery of Exact Equations 

_"Taming Archimedes' Sand Reckoner to Unearth Exact Equations by Harvesting the Ideal of Points with well-known Commutative Algebra Tools."_

MoadeeB is an algorithm implemented in Python for the discovery of exact equations (e.g. from integer sequences).

## About the main (development, `oeis`) branch:
This is the branch of the latest code release of MoadeeB, while the main `oeis` branch is intended for development only. 
 
Therefore, consider the recommended usage of stable version, available in:
- this, _MoadeeB_ branch (https://github.com/B0Gec/Diofantos/tree/MoadeeB)
- a pre-release, equivalent to this branch: https://github.com/B0Gec/Diofantos/releases/tag/v2.0.0_m2025_2_15

TL;DR: Following the recommended git procedure below (_Get essential files via git_), you get the same files as from the above release/branch.


## How to set up MoadeeB

To reproduce results, one could use [container](https://github.com/B0Gec/Diofantos/tree/MoadeeB?tab=readme-ov-file#apptainersingularity-container) (instructions below) as an alternative to installing Python dependencies listed below.

Otherwise, go ahead and install the dependencies in a new python environment.

Nonetheless, you will also need the CoCoA software as described in Other prerequisites below.

After that, you can clone the repository, but I recommend getting only (instead of all 7GB results) the following files (or directories):

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

I find it easiest to use git to make an efficient clone to automatically download the essential files to try out the method. Run these commands in terminal: 
```bash
git clone --single-branch --branch MoadeeB -n --depth=1 --filter=tree:0 https://github.com/B0Gec/Diofantos
cd Diofantos
git restore --source HEAD exact_ed.py diophantine_solver.py doones.py cores_test.csv sindy_oeis.py gather_results.py mb_oeis.py mb_wrap.py cocoa_location.py real-bench real_world_bench.py real_world_bench_evaluate.py
```

In the end download `linear_database_newbl.csv` manually (182.8MB) from my Zenodo repository (https://doi.org/10.5281/zenodo.13767012), since it is stored as git lfs (large files) and they seem to be hard to download as a single file.

And ignore files under the GitHub "Assets" section of the GitHub's release page.

## Simple example of MoadeeB' execution in terminal:

```bash
python doones.py --task_id 14 --exper_id output_dir
```

will produce the output file `results/output_dir/00014_A000045.txt` with similar content:

```txt
orders_used: [2]
Exact ED for 15-th sequence of 164 in experiment set with id A000045 for first 200 terms with max order 20 while double checking against first 199 terms. took:
 1.1 seconds, i.e. 0.02 minutes or 0.0 hours.
CORELIST: True, METHOD: MB, SINDy: False (True also in case of MAVI), GROUND_TRUTH: False, SINDy_default: True, DEBUG: False, OEISformer: False
n_of_terms_ed: 200, N_OF_TERMS_ED: 200
Library: n, max_order 20, max_degree: 3, threshold: 0.1, 
n_more_terms: 10
Library: n, max_order 20, threshold: 0.1
  MB:  n_more_terms: 10 MAX_BITSIZE: 50

by degree: unknown_mb and order: 2.
eqs_explicit:
['a(n) = a(n-2) + a(n-1)']
non_linears:
['a(n) -a(n-1) -a(n-2)']
A000045: 
a(n) = a(n-2) + a(n-1)
truth: 
None

No ground truth :(  -  checked against website ground truth.     
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
- nine data sets of real-world benchmarks (in directory `real-bench`): `pitagora-triplets.csv`, `det.csv`, `tr.csv`, 
     `wheel.csv`, `euler.csv`, `riemann-roch.csv`, `symcomp.csv`, `symcomp6ratio_y2-x2diof.csv`, `symcomp10ratio_-3x2p3y2p3y.csv` 
  - were generated and evaluated by: `real_world_bench.py`, `real_world_bench_evaluate.py`
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

