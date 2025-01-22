# Diofantos

Diofantos is an algorithm implemented in Python for the discovery of exact equations from integer sequences.

You can cite my paper: https://doi.org/10.3390/math12233745 

This branch is the latest release of Diofantos, corresponding to the published paper, an updated version of [First releas: paper version](https://github.com/B0Gec/Diofantos/releases/tag/v1.0.1_d2024_02_26).

## How to set up Diofantos

To reproduce results, one could use container as an alternative to installing Python dependencies listed below.

Otherwise, go ahead and install the dependencies in a new python environment.

After that, you can clone the repository, but I recommend getting only (instead of all 7GB results) the following files:

    exact_ed.py
    diophantine_solver.py
    doones.py
    linear_database_newbl.csv
    cores_test.csv
    sindy_oeis.py

The list above is not checked so please make sure there are no import errors.

### Get essential files via git

I find it easiest to use git to make an efficient clone to automatically download the essential files to try out the method. Run these commands in terminal: 
```bash
git clone -n --depth=1 --filter=tree:0 https://github.com/B0Gec/Diofantos
cd Diofantos
git restore --source cf66eec6d45f6cbc0bc5d0b2da0361332a811484 exact_ed.py diophantine_solver.py doones.py cores_test.csv sindy_oeis.py
```

In the end download linear_database_newbl.csv manually since it is stored as git lfs (large files).

And ignore files under the GitHub "Assets" section.

## Simple example of Diofantos' execution in terminal:

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
- script for running Diofantos and SINDy-based approaches: `doones.py`
- Diofantos code: `exact_ed.py`
- SINDy based approaches: `sindy_oeis.py`
- Results: directories `results` and `results_oeis`

## Features
- algebraic equations with variables `n`, `a(n-k)` for all *k* up to chosen order and
their combinations up to degree *d*.

## Dependencies
- [Diophantine](https://pypi.org/project/Diophantine/)
- numpy
- scipy
- sympy
- pytest (optional)

# Usage examples of script `doones.py` in first version (26.2.2024)
- Diofantos for Fibonacci sequence in _core_ database:
     `python doones.py --task_id 14 --exper_id output_dir`



