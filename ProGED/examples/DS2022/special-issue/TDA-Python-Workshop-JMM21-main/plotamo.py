#plot
import pandas as pd
import matplotlib.pyplot as plt

traj_names = ["lorenzA", "lorenzB", "lorenzC", "lorenzD", "lorenzE"]
lorenzs = []

place = "data/"
for name in traj_names:
    lorenz_pd = pd.read_csv(place + name + '_data.csv')
    lorenz = lorenz_pd.to_numpy()[:, 1:]
    lorenzs += [lorenz]

# fig1 = plt.figure()
cnt = -1
for traj in lorenzs:
    cnt += 1
    fig1 = plt.figure()
    ax = fig1.add_subplot(projection='3d')

    # plt.plot(traj[:, 0], traj[:, 1])
    ax.scatter(traj[:, 0], traj[:, 1], traj[:, 2], label='P1', s=1)
    plt.title(f'{traj_names[cnt]}')
    # fig1.savefig(f'{traj_names[cnt]}.png', dpi=300)
plt.show()
    # plt.plot(fig1)
plt.title('Signal')
# plt.show()
plt.ylabel('Voltage (V)')
