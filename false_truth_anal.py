import pandas as pd
fname = 'header_database_linear.csv'
csv = pd.read_csv(fname)

from blacklist import blacklist
from blacklist import no_truth, false_truth
from exact_ed import truth2coeffs

print('fail:', [i for i in csv.columns if i in no_truth and i in false_truth])


# bigger = [i for i in csv.columns if len(truth2coeffs(csv[i][0])) > 20 if i not in blacklist]
# print(2)

from all_ids import all_ids
csv_filename = 'linear_database_full.csv'
full = pd.read_csv(csv_filename, low_memory=False, nrows=0)

from exact_ed import check_truth

# correct = ['A000045', 'A000004', 'A000008']
# for i in correct[:10]:
#     print(check_truth(i, csv_filename)[0][0])
# for i in false_truth[:4]:
#     check = check_truth(i, csv_filename, oeis_friendly=15)[0]
#     print(i, check[1][:20])
#     print(i, check[2][:20])
#     print(check[0])
#


over50 = ['A352095', 'A296999', 'A004829', 'A235933', 'A166986', 'A293981', 'A071452', 'A002186', 'A335247', 'A004434', 'A003733', 'A212578', 'A071460', 'A092634', 'A135619', 'A277830', 'A289265', 'A133058', 'A117829', 'A055649', 'A242350', 'A014541', 'A105067', 'A343079', 'A337398', 'A182141', 'A346972', 'A007396', 'A117154', 'A108792', 'A293979', 'A170729', 'A100774', 'A075412', 'A192336', 'A342696', 'A125930', 'A192447', 'A071447', 'A087099', 'A324472', 'A125943', 'A336238', 'A008319', 'A337241', 'A018785', 'A328550', 'A243845', 'A118536', 'A341893', 'A125937', 'A224808', 'A003997', 'A118606', 'A341895', 'A003995', 'A044941', 'A187185', 'A003999', 'A214394', 'A176646', 'A293978', 'A030132', 'A194768', 'A194769', 'A071434', 'A118543', 'A034493', 'A027634', 'A337240', 'A098616', 'A355873', 'A249668', 'A160769', 'A173908', 'A339852', 'A117661', 'A133679', 'A187186', 'A132337', 'A109303', 'A007752', 'A118631', 'A170775', 'A003608', 'A346054', 'A071453', 'A131505', 'A309710', 'A343083', 'A187188', 'A338433', 'A197908', 'A247486', 'A053833', 'A071431', 'A071451', 'A118610', 'A003330', 'A117597', 'A008820', 'A187187', 'A306245', 'A108692', 'A071435', 'A008884', 'A157069', 'A056758', 'A118614']
over25 = ['A065025', 'A320034', 'A322558', 'A352095', 'A296999', 'A021980', 'A343086', 'A004829', 'A235933', 'A166986', 'A293981', 'A164012', 'A008900', 'A309554', 'A071452', 'A002186', 'A335247', 'A008877', 'A227018', 'A004434', 'A237988', 'A097864', 'A003733', 'A212578', 'A071460', 'A092634', 'A135619', 'A008878', 'A209880', 'A277830', 'A289265', 'A133058', 'A117829', 'A055649', 'A187183', 'A227006', 'A077069', 'A242350', 'A014541', 'A118512', 'A105067', 'A021976', 'A343079', 'A209879', 'A337398', 'A071831', 'A182141', 'A346972', 'A350414', 'A007396', 'A117154', 'A108792', 'A293979', 'A008880', 'A170729', 'A100774', 'A075412', 'A192336', 'A342696', 'A125930', 'A192447', 'A309791', 'A299252', 'A056064', 'A289188', 'A071447', 'A087099', 'A061993', 'A324472', 'A187184', 'A125943', 'A355021', 'A336238', 'A008319', 'A337241', 'A309302', 'A018785', 'A008896', 'A257093', 'A328550', 'A008899', 'A118618', 'A243845', 'A100476', 'A118536', 'A027640', 'A118615', 'A341893', 'A051629', 'A125937', 'A224808', 'A003997', 'A118606', 'A288692', 'A343078', 'A341895', 'A288550', 'A007300', 'A003995', 'A333348', 'A008882', 'A118634', 'A014527', 'A044941', 'A277384', 'A134720', 'A187185', 'A003999', 'A214394', 'A176646', 'A293978', 'A068045', 'A108053', 'A030132', 'A194768', 'A194769', 'A071434', 'A118543', 'A034493', 'A027634', 'A118609', 'A169091', 'A337240', 'A098616', 'A355873', 'A249668', 'A160769', 'A173908', 'A339852', 'A246088', 'A117661', 'A065024', 'A133679', 'A071832', 'A216127', 'A118530', 'A187186', 'A214156', 'A125917', 'A132337', 'A197708', 'A289840', 'A109303', 'A007752', 'A118631', 'A246086', 'A195201', 'A199629', 'A170775', 'A003608', 'A193455', 'A346054', 'A125920', 'A071453', 'A131505', 'A309710', 'A032444', 'A343083', 'A306979', 'A187188', 'A081749', 'A101757', 'A338433', 'A014268', 'A198070', 'A197908', 'A247486', 'A125939', 'A053833', 'A309494', 'A118633', 'A071431', 'A246079', 'A071451', 'A057615', 'A118610', 'A003330', 'A117597', 'A082505', 'A008820', 'A187187', 'A306245', 'A108692', 'A289841', 'A246092', 'A071435', 'A246087', 'A008879', 'A008884', 'A157069', 'A056758', 'A264758', 'A046701', 'A008897', 'A008898', 'A118614']
over100 = ['A296999', 'A004829', 'A235933', 'A166986', 'A293981', 'A071452', 'A335247', 'A004434', 'A003733', 'A212578', 'A071460', 'A092634', 'A135619', 'A277830', 'A133058', 'A055649', 'A242350', 'A105067', 'A182141', 'A117154', 'A108792', 'A293979', 'A170729', 'A100774', 'A075412', 'A125930', 'A087099', 'A324472', 'A337241', 'A328550', 'A243845', 'A118536', 'A341893', 'A224808', 'A003997', 'A341895', 'A044941', 'A003999', 'A214394', 'A176646', 'A293978', 'A030132', 'A194768', 'A194769', 'A071434', 'A098616', 'A249668', 'A160769', 'A173908', 'A339852', 'A117661', 'A133679', 'A109303', 'A007752', 'A170775', 'A346054', 'A187188', 'A338433', 'A197908', 'A247486', 'A053833', 'A071451', 'A003330', 'A008820', 'A306245', 'A071435', 'A008884', 'A157069']

first_few = 20
first_few = 10000
false_truth = over100[:first_few]
# false_truth = over100
# false_truth = over25

oeis_friendly=190
false_oeis_friendly = [id_ for id_ in false_truth
                       if not check_truth(id_, csv_filename, oeis_friendly=oeis_friendly)[0][0]]
print('oeis_friendly:', oeis_friendly, 'first_few:', first_few)
print(len(false_oeis_friendly), false_oeis_friendly[:10])
print(false_oeis_friendly)


