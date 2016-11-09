import numpy as np
import matplotlib.pyplot as plt
import os

from scipy import interpolate

#exec(open("./make_one_plot_only.py").read())

def read_out(fname, search_strings, column):        #read .out datafile
    f1 = open(fname)
    for line in f1:
        if '&geometry' in line:
            f1.readline()
            temp = f1.readline()
            data = temp.split()
            #print (line)
            #print (temp)
            #print (data)
            #print(data[-1])
    if column == 0:
       return data[-4]
    if column == 1:
        return data[-1]
    return None
    
def read_his(fname, column = 1):                    #read .hise datafile
    z, f_end = [], []
    f1 = open(fname)
    print(f1.name)
    line = f1.readline()
    line = f1.readline()
    for line in f1:
        temp = line.strip()
        first = temp[0:temp.find(' ')]
        second = temp[temp.rfind(' '):]             #leaves a ' ' at the beginnning
        second = second.strip()

        z.append(first)
        f_end.append(second)
    f1.close()
    return (z, f_end)

def get_first_line(z0, hisez, hisef):
    a = 1


file = '/IMSIL_output/ar2/ar2_0_1.hise'         #open 1 .hise file for testing
path = os.getcwd() + file
(z, f) = read_his(path)
result_z = np.array(z, dtype = float)
result_f = np.array(f, dtype = float)
print(result_z)
print(result_f)

file_out = '/IMSIL_output/ar2/ar2_0_1.out'      #open 1 .out file for testing
path_out = os.getcwd() + file_out
result_out0 = read_out(path_out, ' ', 0)
result_out1 = read_out(path_out, ' ', 1)
print (result_out0, result_out1)

get_first_line(result_out0, result_z, result_f)


'''
fig = plt.figure()
expo = fig.add_subplot(111)
expo.plot(result_z, result_f, 'r+-', label = 'z[n] / F[n]', color = 'blue')
expo.axvline(x=float(result_out0), label = 'z0', color = 'black')
expo.axvline(x=float(result_out1), label = 'z1', color = 'black')


expo.set_title('Extrapolate')
expo.legend()
plt.show()
'''
'''
plt.title('test')
plt.plot(result_z, result_f, 'r+-', label = 'test')
plt.legend()
plt.show()
'''






'''
def extrap1d(interpolator):
    xs = interpolator.x
    ys = interpolator.y
    
    def pointwise(x):
        if x < xs[0]:
            return ys[0] + (x-xs[0]) * (ys[1]-ys[0]) / (xs[1]-xs[0])
        elif x > xs[-1]:
            return ys[-1] + (x-xs[-1]) * (ys[-1]-ys[-2]) / (xs[-1]-xs[-2])
        else:
            return interpolator(x)
            
    def ufunclike(xs):
        return array(map(pointwise, array(xs)))
    
    return ufunclike    
'''