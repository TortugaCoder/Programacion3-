import numpy as np
import matplotlib.pyplot as plt

n = np.arange(0, 50, 1)
y = np.cos(n)

y[y < 0] = 0

print(y)

plt.stem(n,y)
plt.show()