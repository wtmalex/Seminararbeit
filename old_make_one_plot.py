import numpy as np
import matplotlib.pyplot as plt
import os

#exec(open("./make_one_plot_only.py").read())


def read_out(fname, search_strings, column):        #read .out datafile
    zvalue = 0
    f1 = open(fname)
    f2 = open(fname)
    
    for line in f1:                                 #get the z0 or z1 value
        if '&geometry' in line:
            f1.readline()
            temp = f1.readline()
            data = temp.split()
    if column == 0:
        zvalue = data[-4]
    if column == 1:
        zvalue = data[-1]

    if 'semi' in f2.name:                           #get mean value if semi file
        for secline in f2:
            if 'Yield' in secline:
                asd = f2.readlines()[0:36]
                q = asd[35]
                r = q.split()
                print('the mean value of Backscattered stuff is: ' + r[6])

    if '_0_1' in f2.name:                           #get mean value if 0_1 file
        for secline in f2:
            if 'Yield' in secline:
                asd = f2.readlines()[0:51]           #read 51 lines, and save the last
                q = asd[50]
                r = q.split()
                print('the mean value of Transmitted stuff is: ' + r[6])
                
    return zvalue, r[6]                      #return the z value and the mean


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
    return (z, f_end)                               #return the z and f value


def get_zero_line(z0, z1, hisez):                   #get the indices where Z is 0
    temp_first = z0 - hisez
    asd_first = np.nonzero(temp_first == 0.)[0][0]          #returns the index of the 0-valued element 
    temp_last = z1 - hisez
    asd_last = np.nonzero(temp_last == 0.)[0][0]          #returns the index of the 0-valued element
    return(asd_first, asd_last)


def mittlerwerte_start(start, hisez, hisef):
    #start: result of get_zero_line
    temp0 = (hisez[start] + hisez[start + 2]) / 2
    temp1 = (hisez[start + 2] + hisez[start + 4]) / 2
    return (temp0, temp1)


def mittlerwerte_end(end, hisez, hisef):
    #end : result of get_zero_line
    temp0 = (hisez[end - 2] + hisez[end]) / 2
    temp1 = (hisez[end - 4] + hisez[end - 2]) / 2
    return (temp0, temp1)

    
    

file = '/IMSIL_output/ar2/ar2_0_1.hise'         #open 1 .hise file for testing
path = os.getcwd() + file
(z, f) = read_his(path)
result_z = np.array(z, dtype = float)               #array of z and F(z) values from hise
result_f = np.array(f, dtype = float)
#print(result_z)
#print(result_f)

file_out = '/IMSIL_output/ar2/ar2_0_1.out'      #open 1 .out file for testing
path_out = os.getcwd() + file_out
(out0, mean0) = read_out(path_out, ' ', 0)                   
(out1, mean1) = read_out(path_out, ' ', 1)
result_out0 = float(out0)                           #z and mean values from out
result_out1 = float(out1)
result_mean0 = float(mean0)
result_mean1 = float(mean1)
print('out0,\t out1, \t mean0,\t mean1')
print (str(result_out0) + '\t' + str(result_out1) + '\t' + str(result_mean0) + '\t' + str(result_mean1))

(intsec1, intsec2) = get_zero_line(result_out0, result_out1, result_z)  #indeces where val is 0
#print('Index of 0val: ' + str(intsec1) , str(intsec2))

(start0, start1) = mittlerwerte_start(intsec1, result_z, result_f)      #x-values of 2 left points
#print('start0=' + str(start0) + ' start1=' + str(start1))
deltay_left =  result_f[intsec1 + 3] - result_f[intsec1 + 2]             #diff of y-vals of 2 left points
newy_left = result_f[intsec1 + 2] - (deltay_left/2)                       #calc the y-val at intersection
#print('deltay_left=' + str(deltay_left) + ' newy_left=' + str(newy_left))

(end0, end1) = mittlerwerte_end(intsec2, result_z, result_f)            #x-values of 2 right points
deltay_right = result_f[intsec2 - 2] - result_f[intsec2 - 1]        #diff of y-vals of 2 right points
newy_right = result_f[intsec2 - 1] - (deltay_right/2)                   #calc the y-val at intersec.
#print( result_f[intsec2 - 2],  result_f[intsec2 - 1], intsec2 - 3)
#print('deltay_right=' + str(deltay_right) + ' newy_right=' + str(newy_right))

fig = plt.figure()
expo = fig.add_subplot(111)
something = expo.plot(result_z, result_f, 'r+-', label = 'z[n] / F[n]', color = 'blue')
expo.axvline(x=result_out0, label = 'z0', color = 'black')              #z from out
expo.axvline(x=result_out1, label = 'z1', color = 'black')      
                        #POINTS + THE LINE AT START START
expo.plot(start0, result_f[intsec1 + 2], 'go')                         
expo.plot(start1, result_f[intsec1 + 3], 'go')
expo.plot(result_out0, newy_left, 'ro')                #HIDE YO KIDS, HODE YO HAXXES
expo.plot([start0, start1, result_out0], [result_f[intsec1 + 2], result_f[intsec1 + 3], newy_left],
                    color = 'green')
                        #POINTS + THE LINE AT START END
                        #POINTS + THE LINE AT END START
expo.plot(end0, result_f[intsec2 - 1], 'go')                        
expo.plot(end1, result_f[intsec2 - 2], 'go')
expo.plot(result_out1, newy_right, 'ro')                #HIDE YO KIDS, HODE YO HAXXES
expo.plot([result_out1, end0, end1], [newy_right, result_f[intsec2 - 1], result_f[intsec2 - 2]],
                    color = 'green')
                        #POINTS + THE LINE AT END END

print('Acquired values are: [' + str(result_out0) + '\t,' + str(newy_left) + '] on left')
print('                     [' + str(result_out1) + '\t,' + str(newy_right) + '] on right')
'''
savethis = open('save.txt', 'a')
savethis.write(str(result_mean0 / newy_right) + '\n')
savethis.close()
'''                    
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