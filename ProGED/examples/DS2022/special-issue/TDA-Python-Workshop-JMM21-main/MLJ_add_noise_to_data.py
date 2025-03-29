import numpy as np
import matplotlib.pyplot as plt

def plot_noisy_data(data, save_plot=True, plot_path="", plot_name=""):

    t = data[:, 0]
    amplitudes = data[:, 1:]
    n_vars = np.size(amplitudes, 1)

    # plot the time series data
    fig1 = plt.figure()
    for ip in range(n_vars):
        plt.plot(t, amplitudes[:, ip])
    plt.title('Signal')
    plt.ylabel('Voltage (V)')

    fig2 = plt.figure()
    for ip in range(n_vars):
        plt.plot(t[1000:2000], amplitudes[1000:2000, ip])
    plt.title('Signal')
    plt.ylabel('Voltage (V)')

    # plot the phase plot
    fig3 = plt.figure()
    if n_vars == 2:
        plt.plot(amplitudes[:, 0], amplitudes[:, 1])
    elif n_vars == 3:
        ax = plt.axes(projection='3d')
        ax.plot3D(amplitudes[:, 0], amplitudes[:, 1], amplitudes[:, 2])
    elif n_vars == 4:
        plt.subplot(1, 2, 1)
        plt.plot(amplitudes[:, 0], amplitudes[:, 1])
        plt.subplot(1, 2, 2)
        plt.plot(amplitudes[:, 2], amplitudes[:, 3])
    plt.title('phase plot')

    if save_plot:
        fig1.savefig(plot_path + plot_name.format("truedata_timeplot", "png"), dpi=300)
        fig2.savefig(plot_path + plot_name.format("truedata_timeplot_part", "png"), dpi=300)
        fig3.savefig(plot_path + plot_name.format("truedata_phaseplot", "png"), dpi=300)

    plt.close('all')

def add_noise_to_data(data, target_noise_db=None, target_snr_db=None):

    # seed and general vars definition
    mean_noise = 0
    n_vars = np.size(data, 1) - 1

    # set the output
    data_out = np.empty_like(data)
    data_out[:, 0] = data[:, 0]

    # calculate signal power and power in db
    amplitudes = data[:, 1:]
    powers = amplitudes ** 2

    # Calculate signal avg power and convert to dB
    sig_avg_power = np.mean(powers, 0)
    sig_avg_db = 10 * np.log10(sig_avg_power)

    # Add noise based on either desired snr or noise
    if target_snr_db is not None:
        noise_avg_db = sig_avg_db - target_snr_db
        noise_avg_power = 10 ** (noise_avg_db / 10)
        for ivar in range(n_vars):
            noise = np.random.normal(mean_noise, np.sqrt(noise_avg_power)[ivar], len(powers))
            data_out[:, ivar+1] = amplitudes[:, ivar] + noise

    elif target_noise_db is not None:
        noise_avg_power = 10 ** (target_noise_db / 10)
        for ivar in range(n_vars):
            noise = np.random.normal(mean_noise, np.sqrt(noise_avg_power), len(powers))
            data_out[:, ivar+1] = amplitudes[:, ivar] + noise

    else:
        raise Exception('Either target_noise_db or target_snr_sb have to be defined.')

    return data_out