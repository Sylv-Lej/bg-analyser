import cPickle as pickle
import matplotlib.pyplot as plt
weights = pickle.load(open('weights0.bin','r'))
print(weights[0])
plt.imshow(weights[0])
plt.show()
