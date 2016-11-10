import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
import os

def hiseFileList():
    temp = []
    filePaths = []
    for path, subdirs, files in os.walk('C:'):
        for name in files:
            if name.endswith('.hise'):
                if '_0_1' in name or '_0_semi' in name:     # _0_1 instead of 0_1 to prevent ...
                    temp.append(name)                       # 20_1 for example
                    filePaths.append(os.path.join(path, name))
    return (temp, filePaths)


def outFileList():
    temp = []
    filePaths = []
    for path, subdirs, files in os.walk('C:'):
        for name in files:
            if name.endswith('.out'):
                if '_0_1' in name or '_0_semi' in name:     # _0_1 instead of 0_1 to prevent ...
                    temp.append(name)                       # 20_1 for example
                    filePaths.append(os.path.join(path, name))
    return (temp, filePaths)


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
    
    f1.close()
    f2.close()    
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
(hise_files, hise_file_paths) = hiseFileList() #get all .hise files and their path
#print (hise_files)
#print(hise_file_paths)

(out_files, out_file_paths) = outFileList()
#print(out_files)
#print(out_file_paths)

'''
plt.title('test')
plt.plot(result_z, result_f, 'r+-', label = 'test')
plt.legend()
plt.show()
'''


'''
a = [2,3,4,5,6]       #FOR TESTING THE LABELS AND TICKS
b = [3,4,5,6,8]

my_x = ['', 'He', 'Ar', 'Xe', ' '] # '' at begin and end for formalities
plt.xticks(a, my_x)
plt.xlabel('Ion Species')
plt.ylabel('Sputtering Efficiency Y/F$_1$$_D$ [Å/eV]')
plt.title('Sputtering of Si, tilt=0°')

plt.plot(a,b, label= 'kek')
plt.legend()                        #little square at top right
plt.show()          #END OF TESTING
'''






