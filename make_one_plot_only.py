import numpy as np
import matplotlib.pyplot as plt
import os


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

def get_zero_line(z0, z1, hisez):                   #get the indices where Z is 0
    temp_first = z0 - hisez
    asd_first = np.nonzero(temp_first == 0.)[0][0]          #returns the index of the 0-valued element 
    temp_last = z1 - hisez
    asd_last = np.nonzero(temp_last == 0.)[0][0]          #returns the index of the 0-valued element 
    return (asd_first, asd_last)
    
def mittlerwerte_start(start, hisez, hisef):
    #start: result of get_zero_line
    print('topkek')
    print(hisez[start], hisez[start + 2])
    print(hisef[start], hisef[start + 2])
    temp0 = (hisez[start] + hisez[start + 2]) / 2
    
    print(hisez[start + 2], hisez[start + 4])
    print(hisef[start + 2], hisef[start + 4])
    temp1 = (hisez[start + 2] + hisez[start + 4]) / 2
    return (temp0, temp1)
    
def mittlerwerte_end(end, hisez, hisef):
    #end : result of get_zero_line
    print('topkek')
    print(hisez[end - 2], hisez[end])
    print(hisef[end - 2], hisef[end])
    temp0 = (hisez[end - 2] + hisez[end]) / 2
    
    print(hisez[end - 4], hisez[end - 2])
    print(hisef[end - 4], hisef[end - 2])
    temp1 = (hisez[end - 4] + hisez[end - 2]) / 2
    return (temp0, temp1)

file = '/IMSIL_output/ar2/ar2_0_1.hise'         #open 1 .hise file for testing
path = os.getcwd() + file
(z, f) = read_his(path)
result_z = np.array(z, dtype = float)
result_f = np.array(f, dtype = float)
print(result_z)
print(result_f)

file_out = '/IMSIL_output/ar2/ar2_0_1.out'      #open 1 .out file for testing
path_out = os.getcwd() + file_out
out0 = read_out(path_out, ' ', 0)
out1 = read_out(path_out, ' ', 1)

result_out0 = float(out0)
result_out1 = float(out1)
print (result_out0, result_out1)
# 6=10, 7=11 at indeces also the 2 F values after our given z

(intsec1, intsec2) = get_zero_line(result_out0, result_out1, result_z)
print('Index of 0val: ' + str(intsec1) , str(intsec2))

(start0, start1) = mittlerwerte_start(intsec1, result_z, result_f)        #TO GET THE POINTS + LINE
deltay =  result_f[intsec1 + 3] - result_f[intsec1 + 2]           #5.563111E+08 - 6.622265E+08 umgekehrt
newy = result_f[intsec1 + 2] - (deltay/2)
print('deltay=' + str(deltay) + ' newy=' + str(newy))

(end0, end1) = mittlerwerte_end(intsec2, result_z, result_f)
kappay = result_f[intsec2 - 2] - result_f[intsec2 - 1]
wevy = result_f[intsec2 - 2] - (kappay/2)
#print( result_f[intsec2 - 3],  result_f[intsec2 - 2], intsec2 - 3)
print('kappay=' + str(kappay) + ' wevy=' + str(wevy))

fig = plt.figure()
expo = fig.add_subplot(111)
something = expo.plot(result_z, result_f, 'r+-', label = 'z[n] / F[n]', color = 'blue')
expo.axvline(x=result_out0, label = 'z0', color = 'black')              #z from out
expo.axvline(x=result_out1, label = 'z1', color = 'black')      

expo.plot(start0, result_f[intsec1 + 2], 'ro')                         #Points at start
expo.plot(start1, result_f[intsec1 + 3], 'ro')
#expo.plot(start1, result_f[intsec1 + 3], 'ro')             #REMOVE, prolly duplicate somehow
expo.plot(0, newy, 'bo')                #HIDE YO KIDS, HODE YO HAXXES
expo.plot([start0, start1, 0], [result_f[intsec1 + 2], result_f[intsec1 + 3], newy], color = 'green')

expo.plot(end0, result_f[intsec2 - 1], 'ro')                         #Points at end
expo.plot(end1, result_f[intsec2 - 2], 'ro')
expo.plot(40, kappay, 'bo')                #HIDE YO KIDS, HODE YO HAXXES
expo.plot([40, end0, end1], [kappay, result_f[intsec2 - 1], result_f[intsec2 - 2]], color = 'green')

expo.set_title('Extrapolate')
expo.legend()
plt.show()


'''
from scipy.interpolate import interp1d
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
'''
f = interp1d(result_z, result_f)
expo.plot(result_z, f(result_z), 'r+-', label = 'z[n] / F[n]', color = 'blue')
'''
'''
print('random stuff')
yvalue = something[0].get_ydata()
print(yvalue)
idx = np.where(yvalue == yvalue[0])
print(idx)
expo.plot([0], [f(result_z)[7]] , 'ro')
'''