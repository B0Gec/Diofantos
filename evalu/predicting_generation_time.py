"""
Predict time needed to generate n expressions for benchmark based on previous runs.
"""

import numpy as np


def disco_predict_time(data: tuple) -> list[float]:
    """
    Data = [( num_expressions, time_in_seconds ), ...]
    """
    # lhs = A*sol = b
    steps, time = np.array([i[0] for i in data]), np.array([i[1] for i in data])
    steps, rhs = tuple(np.array(i).reshape(-1,1) for i in [steps, time])
    squares = steps*steps
    lhs = squares
    # lhs = np.hstack((squares, steps))
    # lhs = np.hstack((lhs, steps*0 + 1 ))
    print(f'{squares = }')
    print(f'{lhs = }')
    print(f'{rhs = }')

    # rhs = time.reshape(-1, 1)  # = b
    # print(rhs)
    # A = np.array([[data[]], [1, data_points[1]]])
    # sol = np.linalg.solve(lhs, rhs)

    sol = np.linalg.lstsq(rhs, lhs)[0][0]
    sol_round = [round(s, 2) for s in sol]
    # sol_round = [s for s in sol]
    print(f'solution: {sol}')
    print(f'rounded solution: {sol_round}')

    return sol

# candidate:
print('\n      ', [int(i) for i in np.array([(1/72) *x**2 + (-1/3.4)*x  for x in [54, 161, 82, 278]])])
print('truth:', [i[1] for i in [(54, 26), (161, 280), (82, 70), (278, 985), (846, 11520), (846, 80245)]])
# coefs = disco_predict_time( [(54, 26), (161, 280), (82, 70), (278, 985)])
# print('\nPredicting time: ', coefs)
predict_time = lambda x: f'For {x} steps, it will take approx. {int(((1/72) *x**2 + (-1/3.4)*x)/(60)/60)} hours.'
print('\nPredicting time: ', predict_time(54))
[print(predict_time(i)) for i in [54, 161, 82, 278, 846]]
[print(predict_time(i)) for i in [500, 1000, 2000, 5000, 10000]]
# [print(predict_time(i)) for i in [500, 1000, 5000, 10000]]
# For 54 steps, it will take approx. 0 days.
# For 161 steps, it will take approx. 0 days.
# For 82 steps, it will take approx. 0 days.
# For 278 steps, it will take approx. 0 days.
# For 500 steps, it will take approx. 55 minutes.
# For 1000 steps, it will take approx. 226 minutes or 3 hours.
# For 2000 steps, it will take approx. 15 hours.
# For 5000 steps, it will take approx. 96 hours or 4 days.
# For 10000 steps, it will take approx. 16 days.
# 1/0


# polynomial only: 890 const eqs .. 1h25min
