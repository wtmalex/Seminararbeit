import os

def fileList():
    temp = []
    for path, subdirs, files in os.walk('C:'):
        for name in files:
            if name.endswith('.py') or name.endswith('.out') or name.endswith('.hise'):
                temp.append(name)
                print(name)
    return temp
    
temp = fileList()
#print(temp)