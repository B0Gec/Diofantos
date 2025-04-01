# """
# Answer: the program is:
# lambda a_n : a_n[-1] + a_n[-2]
#
#
# Grammar:
# S = an[-1] + an[-2]
# Universal:
# an -> C | an-1
# an-5 ->
#
# """


import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt


a, lo, b = 0.3119966255265558, 0.0015961267324625574, 0.09970378577957718
#define three Gamma distributions
x = np.linspace(0, 40, 100)
# y1 = stats.gamma.pdf(x, a=5, scale=3)
# y2 = stats.gamma.pdf(x, a=2, scale=5)
# y3 = stats.gamma.pdf(x, a=4, scale=2)
# y1 = stats.gamma.pdf(x, a=1, scale=1)
# y2 = stats.gamma.pdf(x, a=2, scale=1)
# y3 = stats.gamma.pdf(x, a=3, scale=1)

# y1 = stats.gamma.pdf(x, a=1.1, scale=2)
# y2 = stats.gamma.pdf(x, a=1.3, scale=2)
# y3 = stats.gamma.pdf(x, a=1.4, scale=2)

# y1 = stats.gamma.pdf(x, a=2, scale=1)
# y2 = stats.gamma.pdf(x, a=2, scale=2)
# y3 = stats.gamma.pdf(x, a=2, scale=3)

# y1 = stats.gamma.pdf(x, a=2.5, scale=2)
# y2 = stats.gamma.pdf(x, a=3, scale=2)
# y3 = stats.gamma.pdf(x, a=2.54, scale=2)

# y1 = stats.gamma.pdf(x, a=a, scale=b)
y1 = stats.gamma.pdf(x, a=2.5, scale=2)
print(y1)

orders = [i for i in range(1, 50)]
firsts = stats.gamma.pdf(orders, a=2.5, scale=2)
# firsts = [float(f'{f:.1e}') for f in firsts]
print(firsts)
1/0

# y2 = stats.gamma.pdf(x, a=2.5, scale=2.2)
# y3 = stats.gamma.pdf(x, a=2.5, scale=2.4)
y2 = stats.gamma.pdf(x, a=2.5, scale=2.8)
y3 = stats.gamma.pdf(x, a=2.5, scale=4)

#add lines for each distribution
plt.plot(x, y1, 'r', label='shape=5, scale=3')
plt.plot(x, y2, 'g', label='shape=2, scale=5')
plt.plot(x, y3, 'b', label='shape=4, scale=2')

# Enable dense grid
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.minorticks_on()

# Set dense ticks for both axes
ax = plt.gca()
ax.xaxis.set_major_locator(plt.MultipleLocator(1))
ax.yaxis.set_major_locator(plt.MultipleLocator(0.02))
ax.xaxis.set_minor_locator(plt.MultipleLocator(0.2))
ax.yaxis.set_minor_locator(plt.MultipleLocator(0.005))


#add legend
plt.legend()

#display plot
plt.show()

# 1/0
a, lo, b = 0.3119966255265558, 0.0015961267324625574, 0.09970378577957718

import scipy.stats as stats    
alpha = 5
loc = 100.5
beta = 22
data = stats.gamma.rvs(alpha, loc=loc, scale=beta, size=10000)    
print(data)
print(type(data), data.shape)

# [ 202.36035683  297.23906376  249.53831795 ...,  271.85204096  180.75026301
#   364.60240242]

# Here we fit the data to the gamma distribution:

fit_alpha, fit_loc, fit_beta=stats.gamma.fit(data)
print(fit_alpha, fit_loc, fit_beta)
# (5.0833692504230008, 100.08697963283467, 21.739518937816108)

print(alpha, loc, beta)
# (5, 100.5, 22)

# data_per_order = [0.025538027719400922, 0.13529834268840946, 0.16990769067063924, 0.15910723311430927, 0.09172408289218163, 0.0729961958979543, 0.042669787981165705, 0.04301561543986593, 0.030219999467957757, 0.028783485408741455, 0.015509031417094518, 0.021255087653959726, 0.011093080790614775, 0.008858503365167194, 0.007528397754781729, 0.012582799074246495, 0.005373626665957277, 0.006969753398419835, 0.0046819717485568355, 0.010827059668537682, 0.005134207656087893, 0.005400228778164986, 0.003697693596871592, 0.007102763959458381, 0.0037774999334947196, 0.004016918943364103, 0.0032454576893405336, 0.0060652815833577185, 0.0028464260062248943, 0.0037774999334947196, 0.0034316724747944986, 0.005480035114788114, 0.002394190098693836, 0.0028730281184326037, 0.0021813732010321617, 0.00414992950440265, 0.002207975313239871, 0.0024207922109015455, 0.001968556303370488, 0.003085845016094278, 0.0017823415179165226, 0.002553802771940092, 0.0017025351812933946, 0.003112447128301987, 0.002074964752201325, 0.002021760527785906, 0.0015961267324625576, 0.0024739964353169643, 0.0017557394057088132, 0.001729137293501104]
data_per_order = [960, 5086, 6387, 5981, 3448, 2744, 1604, 1617, 1136, 1082, 583, 799, 417, 333, 283, 473, 202, 262, 176, 407, 193, 203, 139, 267, 142, 151, 122, 228, 107, 142, 129, 206, 90, 108, 82, 156, 83, 91, 74, 116, 67, 96, 64, 117, 78, 76, 60, 93, 66, 65]
print(len(data_per_order))
1/0
data_per_order = data_per_order[:10]

fit_alpha, fit_loc, fit_beta=stats.gamma.fit(data_per_order)
print(fit_alpha, fit_loc, fit_beta)

import matplotlib.pyplot as plt
import numpy as np

# Example data
x = np.linspace(0, 10, 100)
y = np.sin(x)

# Create plot
plt.plot(x, y)

# Enable grid
plt.grid(which='both', linestyle='--', linewidth=0.5)

# Enable minor ticks
plt.minorticks_on()

# Customize major and minor ticks
plt.gca().xaxis.set_major_locator(plt.MultipleLocator(1))
plt.gca().xaxis.set_minor_locator(plt.MultipleLocator(0.2))
plt.gca().yaxis.set_major_locator(plt.MultipleLocator(0.5))
plt.gca().yaxis.set_minor_locator(plt.MultipleLocator(0.1))

# Show plot
plt.show()
