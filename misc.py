import numpy as np
import matplotlib.pyplot as plt
#%%

plt.figure()
for t in np.arange(20,40):
    Pskin = 0.31121 * np.exp((18.678 - (t/234.5)) * (t/(257.14+t)))
    plt.scatter(t,Pskin)
