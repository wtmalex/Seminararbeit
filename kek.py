import numpy as np
import matplotlib.pyplot as plt

asd = open('save.txt')
z, f_end = [], []
print(asd.name)
for line in asd:
    temp = line.strip()
    #first = temp[0:temp.find(' ')]
    #second = temp[temp.rfind(' '):]             #leaves a ' ' at the beginnning
    #second = second.strip()

    #z.append(first)
    #f_end.append(second)
    f_end.append(temp)
asd.close()

print(z, f_end)

#x = np.array(z, dtype = float)
y = np.array(f_end, dtype = float)

print( y)

fig = plt.figure()
expo = fig.add_subplot(111)

expo.plot([0,1,2], y, 'r+-', label = 'ASD')
expo.plot(0, y[0], 'bo')
expo.plot(1, y[1], 'ro')
expo.plot(2, y[2], 'go')
expo.set_title('Extrapolate')
expo.legend()
plt.show()
