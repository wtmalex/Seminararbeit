import os

def hiseFileList():
    '''
    Returns a list of filepaths for .hise files
    '''
    temp = []
    filePaths = []
    for path, subdirs, files in os.walk('C:'):
        for name in files:
            if name.endswith('.hise'):
                if '_0_1' in name or '_0_semi' in name:     # _0_1 instead of 0_1 to prevent
                    temp.append(name)                       #             20_1 for example
                    filePaths.append(os.path.join(path, name))
    return (temp, filePaths)


def outFileList():
    '''
    Returns a list of filepaths for .out files
    '''
    temp = []
    filePaths = []
    for path, subdirs, files in os.walk('C:'):
        for name in files:
            if name.endswith('.out'):
                if '_0_1' in name or '_0_semi' in name:     # _0_1 instead of 0_1 to prevent
                    temp.append(name)                       #             20_1 for example
                    filePaths.append(os.path.join(path, name))
    return (temp, filePaths)


def read_out(fname, search_strings, column):        
    '''
    Reads an .out datafile
    Returns the value of z and the mean
    
    parameters: fname:          Name of the datafile
                search_strings: Tuple of strings, where the first string object is either 0_1 or semi
                                (0_1 for Forward-Sputter, semi for Backward-Sputter), and the second
                                string object is either Transmitted or Backscattered
                                (Transmitted for Forward-sputter, Backscattered for Backward-Sputter).
                column:         The column where the sought value can be found
    '''
    zvalue = 0
    f1 = open(fname)                                #2 filepointers, 1 to get z from geometry
    f2 = open(fname)                                #   and 1 to get the mean value
    
    for line in f1:                                 #get the z0 or z1 value
        if '&geometry' in line:
            f1.readline()
            temp = f1.readline()
            data = temp.split()
    if search_strings[0] == 'semi':
        zvalue = data[-4]
    if search_strings[0] == '0_1':
        zvalue = data[-1]

    if search_strings[0] in f2.name:                        #get mean value if semi file
        for secline in f2:
            if 'Yield' in secline:                          #find the line with 'Yield'
                for thriline in f2:
                    if search_strings[1] in thriline:       #find the next occurence of 'Backscattered'
                        for quadline in f2:
                            if 'mean value' in quadline:    #find the next occ. of 'mean_value'
                                mean_line = quadline        #save it, and stop the search
                                break
                mean_splitted = mean_line.split()
    f1.close()
    f2.close()
    
    if column == 1:
        return zvalue, mean_splitted[4]                     #return the z value and the mean
    elif column == 2:
        return zvalue, mean_splitted[6]
    else:
        print('Error at the columns')
        
    print('Could not get data properly, returning None instead')
    return None,None


def read_his(fname, column = 1):
    '''
    Reads an .out datafile
    Returns 2 lists with values from the file
    '''
    z, f_end = [], []
    f1 = open(fname)
    line = f1.readline()
    line = f1.readline()
    for line in f1:
        temp = line.strip()
        first = temp[0:temp.find(' ')]              #saves the first value from the row
        second = temp[temp.rfind(' '):]             #saves the last value from the row
                                                    #   (leaves a ' ' at the beginnning)
        second = second.strip()

        z.append(first)
        f_end.append(second)
    f1.close()
    return (z, f_end)                               #return the z and f value


(hise_files, hise_file_paths) = hiseFileList() 
(out_files, out_file_paths) = outFileList()




