import numpy as np
import matplotlib.pyplot as plt
import os
import read_output2 as readpy

#exec(open("./eff_mass.py").read())


def get_zero_line(z0, z1, hisez):                   #get the indices where Z is 0
    temp_first = z0 - hisez
    if 0 in temp_first:
        asd_first = np.nonzero(temp_first == 0.)[0][0]          #returns the index of the 0-valued element 
    else:
        print('No 0 in temp_first')
        return(0, 0)                #HEEEEEEEEEEEEY WHY NOT NONE NONE
    temp_last = z1 - hisez
    if 0 in temp_last:
        
        asd_last = np.nonzero(temp_last == 0.)[0][0]          #returns the index of the 0-valued element
        return(asd_first, asd_last)
    else:
        print('No 0 in temp_last')
        return(asd_first, 0)


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

    
outfiles = readpy.out_file_paths
hisefiles = readpy.hise_file_paths
storageb, storagev = [], []

for x,y in zip(hisefiles, outfiles):
    
    path_hise = x
    (z, f) = readpy.read_his(path_hise)
    result_z = np.array(z, dtype = float)               #array of z and F(z) values from hise
    result_f = np.array(f, dtype = float)
    
    path_out = y
    (out0, mean0) = readpy.read_out(path_out, ' ', 0)                   
    (out1, mean1) = readpy.read_out(path_out, ' ', 1)
    result_out0 = float(out0)                           #z and mean values from out
    result_out1 = float(out1)
    result_mean0 = float(mean0)
    result_mean1 = float(mean1)
    print('Mean values are ' + mean0 + ' and ' + mean1)
    
    
    (intsec1, intsec2) = get_zero_line(result_out0, result_out1, result_z)  #indeces where val is 0
    print('Index of 0val: ' + str(intsec1) , str(intsec2))

    (start0, start1) = mittlerwerte_start(intsec1, result_z, result_f)      #x-values of 2 left points
    deltay_left =  result_f[intsec1 + 3] - result_f[intsec1 + 2]             #diff of y-vals of 2 left points
    newy_left = result_f[intsec1 + 2] - (deltay_left/2)                       #calc the y-val at intersection

    (end0, end1) = mittlerwerte_end(intsec2, result_z, result_f)            #x-values of 2 right points
    deltay_right = result_f[intsec2 - 2] - result_f[intsec2 - 1]        #diff of y-vals of 2 right points
    newy_right = result_f[intsec2 - 1] - (deltay_right/2)                   #calc the y-val at intersec.
    
    storageb.append((result_mean0 / newy_right) * 100000000) #from cm to Å
    storagev.append((result_mean0 / newy_left) * 100000000)
    print('\n')
    
print(storageb)
print(storagev)

data2eVb = np.array([storageb[6], storageb[0], storageb[12]])
data20eVb = np.array([storageb[8], storageb[2], storageb[14]])
data200eVb = np.array([storageb[10], storageb[4], storageb[16]])
print(data2eVb)
print(data20eVb)
print(data200eVb)

data2eVf = np.array([storagev[7], storagev[1], storagev[13]])
data20eVf = np.array([storagev[9], storagev[3], storagev[15]])
data200eVf = np.array([storagev[11], storagev[5], storagev[17]])
print(data2eVf)
print(data20eVf)
print(data200eVf)

fig = plt.figure()
sput = fig.add_subplot(111)
a = [0,1,2,3,4,5]       #FOR TESTING THE LABELS AND TICKS
my_x = [' ', 'He', 'Ar', 'Xe', ' ', ' '] # '' at begin and end for formalities
b = [0.00e-09, 0.5e-09, 1e-09, 1.5e-09, 2e-09, 2.5e-09, 3.0e-09]
my_y =['0.00', '0.05', '0.10', '0.15', '0.20', '0.25', '0.30']
plt.xticks(a, my_x)
#plt.yticks(b, my_y)
plt.margins(0.25, 0.25)
plt.xlabel('Ion Species')
plt.ylabel('Sputtering Efficiency Y/F$_1$$_D$ [Å/eV]')
plt.title('Sputtering of Si, tilt=0°')
'''
sput.plot(1, data2eVb[0], 'ro')
sput.plot(2, data2eVb[1], 'ro')
sput.plot(3, data2eVb[2], 'ro')
'''

'''
sput.plot(1, data20eVb[0], 'go')
sput.plot(2, data20eVb[1], 'go')
sput.plot(3, data20eVb[2], 'go')
'''

'''
sput.plot(1, data200eVb[0], 'bo')
sput.plot(2, data200eVb[1], 'bo')
sput.plot(3, data200eVb[2], 'bo')
'''
sput.plot([1,2,3], data2eVb, 'r+-',  color = 'red', marker = 'v', linestyle = '--')
sput.plot([1,2,3], data20eVb, 'r+-',  color = 'green', marker = 'o', linestyle = '--')
sput.plot([1,2,3], data200eVb, 'r+-', color = 'blue',marker = '^', linestyle = '--')


sput.plot([1,2,3], data2eVf, 'r+-', label='2 keV', color = 'red', marker = 'v')
sput.plot([1,2,3], data20eVf, 'r+-', label='20 keV', color = 'green', marker = 'o')
sput.plot([1,2,3], data200eVf, 'r+-', label='200 keV', color = 'blue',marker = '^')

sput.legend()
plt.show()
