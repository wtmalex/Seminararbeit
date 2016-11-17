import numpy as np
import matplotlib.pyplot as plt
import os

def hiseFileList():            #get the list of .hise files
    temp = []
    filePaths = []
    for path, subdirs, files in os.walk('C:'):
        for name in files:
            if name.endswith('.hise'):
                if '_0_1' in name or '_0_semi' in name:     # _0_1 instead of 0_1 to prevent
                    temp.append(name)                       #             20_1 for example
                    filePaths.append(os.path.join(path, name))
    return (temp, filePaths)


def outFileList():            #get the list of .out files
    temp = []
    filePaths = []
    for path, subdirs, files in os.walk('C:'):
        for name in files:
            if name.endswith('.out'):
                if '_0_1' in name or '_0_semi' in name:     # _0_1 instead of 0_1 to prevent
                    temp.append(name)                       #             20_1 for example
                    filePaths.append(os.path.join(path, name))
    return (temp, filePaths)


def read_out(fname, search_strings, column):        #read .out datafile
    zvalue = 0
    f1 = open(fname)                                #2 filepointers, 1 to get z from geometry
    f2 = open(fname)                                #   and 1 to get the mean value
    
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

    if '_0_1' in f2.name:                           #get mean value if _0_1 file
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


(hise_files, hise_file_paths) = hiseFileList() 

(out_files, out_file_paths) = outFileList()






