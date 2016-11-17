# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import os
import read_output2 as readpy

#exec(open("./eff_mass.py").read())

def get_zero_line_0_1(z, hisez):                   #get the indices where Z_1 is 0
    temp_last = z - hisez
    if 0 in temp_last:
        asd_last = np.nonzero(temp_last == 0.)[0][0]          #returns the index of the 0-valued element
        return asd_last
    else:
        print('No 0 in temp_last')
        return 0
        
def get_zero_line_semi(z, hisez):                   #get the indices where Z_0 is 0
    temp_first = z - hisez
    if 0 in temp_first:
        asd_first = np.nonzero(temp_first == 0.)[0][0]          #returns the index of the 0-valued element
        return asd_first
    else:
        print('No 0 in temp_first')
        return 0

def mittlerwerte_start(start, hisez, hisef):        #start: result of get_zero_line
    temp0 = (hisez[start] + hisez[start + 2]) / 2
    temp1 = (hisez[start + 2] + hisez[start + 4]) / 2
    return (temp0, temp1)


def mittlerwerte_end(end, hisez, hisef):            #end : result of get_zero_line
    temp0 = (hisez[end - 2] + hisez[end]) / 2
    temp1 = (hisez[end - 4] + hisez[end - 2]) / 2
    return (temp0, temp1)

hisefiles = readpy.hise_file_paths    
outfiles = readpy.out_file_paths

hisefiles_0_1 = []                                  #separating hise and out files into 2-2 parts
hisefiles_semi = []                                 #   1 for semi and 1 for _0_1
outfiles_0_1 = []
outfiles_semi = []

for i in hisefiles:                                 #fill them
    if '0_1' in i:
        hisefiles_0_1.append(i)
        
for i in hisefiles:
    if '0_semi' in i:
        hisefiles_semi.append(i)

for i in outfiles:
    if '0_1' in i:
        outfiles_0_1.append(i)

for i in outfiles:
    if '0_semi' in i:
        outfiles_semi.append(i)

storageb, storagev = [], []                         #list to store the values to be plotted

###############################################################################################
###################### Saving the values from _0_1 files (Vorwaerts) ##########################
for x,y in zip(hisefiles_0_1, outfiles_0_1):
    
    path_hise = x
    (z, f) = readpy.read_his(path_hise)                 #note: prints path
    result_z = np.array(z, dtype = float)               #array of z and F(z) values from hise
    result_f = np.array(f, dtype = float)
    
    path_out = y
    (out1, mean1) = readpy.read_out(path_out, ' ', 1)   #note: prints mean value
    result_out1 = float(out1)                           #the z_1 value and mean of Transmitted
    result_mean1 = float(mean1)

    intsec = get_zero_line_0_1(result_out1, result_z)   #index where val is 0
    (end0, end1) = mittlerwerte_end(intsec, result_z, result_f)            #x-values of 2 right points
    deltay_right = result_f[intsec - 2] - result_f[intsec - 1]        #diff of y-vals of 2 right points
    newy_right = result_f[intsec - 1] - (deltay_right/2)                   #calc the y-val at intersec.
    
    storageb.append((result_mean1 / newy_right) * 100000000)        #from cm to Å
    print('\n')

###############################################################################################
###################### Saving the values from semi files (Rueckwaerts) ######################## 
for x,y in zip(hisefiles_semi, outfiles_semi):
    
    path_hise = x
    (z, f) = readpy.read_his(path_hise)
    result_z = np.array(z, dtype = float)               #array of z and F(z) values from hise
    result_f = np.array(f, dtype = float)
    
    path_out = y
    (out0, mean0) = readpy.read_out(path_out, ' ', 0)                   
    result_out0 = float(out0)                           #the z_0 value and mean of Backscattered
    result_mean0 = float(mean0)

    intsec= get_zero_line_semi(result_out0, result_z)   #index where val is 0
    (start0, start1) = mittlerwerte_start(intsec, result_z, result_f)       #x-values of 2 left points
    deltay_left =  result_f[intsec + 3] - result_f[intsec + 2]          #diff of y-vals of 2 left points
    newy_left = result_f[intsec + 2] - (deltay_left/2)                       #calc the y-val at intersec.
    
    storagev.append((result_mean0 / newy_left) * 100000000)         #from cm to Å
    print('\n')


print(storageb)
print(storagev)    

data2eVb = np.array([storageb[3], storageb[0], storageb[6]])
data20eVb = np.array([storageb[4], storageb[1], storageb[7]])
data200eVb = np.array([storageb[5], storageb[2], storageb[8]])

data2eVf = np.array([storagev[3], storagev[0], storagev[6]])
data20eVf = np.array([storagev[4], storagev[1], storagev[7]])
data200eVf = np.array([storagev[5], storagev[2], storagev[8]])


fig = plt.figure()
sput = fig.add_subplot(111)
a = [0,1,2,3,4,5]                        #to "convert" the x-values into Elements
my_x = [' ', 'He', 'Ar', 'Xe', ' ', ' '] # '' at begin and end for formalities
plt.xticks(a, my_x)
plt.margins(0.25, 0.25)
plt.xlabel('Ion Species')
plt.ylabel('Sputtering Efficiency Y/F$_1$$_D$ [Å/eV]')
plt.title('Sputtering of Si, tilt=0')

sput.plot([1,2,3], data2eVb, 'r+-',  color = 'red', marker = 'v', linestyle = '--')
sput.plot([1,2,3], data20eVb, 'r+-',  color = 'green', marker = 'o', linestyle = '--')
sput.plot([1,2,3], data200eVb, 'r+-', color = 'blue',marker = '^', linestyle = '--')

sput.plot([1,2,3], data2eVf, 'r+-', label='2 keV', color = 'red', marker = 'v')
sput.plot([1,2,3], data20eVf, 'r+-', label='20 keV', color = 'green', marker = 'o')
sput.plot([1,2,3], data200eVf, 'r+-', label='200 keV', color = 'blue',marker = '^')

sput.legend()
plt.show()