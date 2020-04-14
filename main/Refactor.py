from multiprocessing import Process
import time
import sys
import re


# from multiprocessing import Process

# def func1():
#   print 'func1: starting'
#   for i in xrange(10000000): pass
#   print 'func1: finishing'

# def func2():
#   print 'func2: starting'
#   for i in xrange(10000000): pass
#   print 'func2: finishing'

# file = open('variable', 'r').readlines()
# print(int(file[0]))


# def func1():
#     file = open('variable', 'r').readlines()
#     return int(file[0])

file = open('environment.py', 'r').read()
variable = open('variable', 'w')
filew = open('target_new.py', 'w')

vari = re.findall(r"[ \n\t]+[a-zA-Z_]+[ ]*[=][ ]*[0-9]+", file)

# print(vari)

variables = {}

for i in vari:
    le = i.split('=')[0].strip()
    re = i.split('=')[1].strip()
    
    
    if len(le)>=3 and int(re) != 0 and int(re) != 1:
        variables[le] = re

# print(variables)

file = open('environment.py', 'r').readlines()

index = 0

for key in variables.keys():
    filew.write('#Variable '+str(index)+': '+key+'\n')
    variable.write(str(variables[key])+'\n')
    filew.write('def '+str(key)+'():\n\tfile = open("variable", 'r').readlines()'+'\n\ttry:\n\t\t'+'return int(file['+str(index)+'])\n\texcept:\n\t\treturn '+str(variables[key])+'\n\n')
    index = index + 1
    # print(key)

# print("---------------------------------------------")

for i in file:
    temp = 0
    if i.find('=')!=-1:
        # print(i)
        left = i.split('=')[0]
        # print(left)
        for key in variables.keys():
            if left.find(key) != -1:
                # print(i.strip())
                newi = left.rstrip() + '_c = ' + left.strip() + '()'
                # print(newi)
                filew.write(newi+'\n')
                temp = 1
    if temp == 0:
        newi = i
        for key in variables.keys():
            if i.find(key) != -1:
                # print(i)
                newi = newi.replace(key, key+'()')
                newi = newi.replace('self.'+key, key)
        filew.write(newi)
            
        # print(i)
    # for key in variables.keys():
    #     if i.find(key) != -1:
    #         print(i.strip())
        


# vari = {}

# index = 0

# for i in file:
#     if '=' not in i:
#         newi = i
#         for key in vari.keys():
#             print(key)
#             print(i)
#             if i.find(key) != -1:
#                 print("found")
#                 newi = newi.replace(key, key+'()')
#         filew.write(newi)

#     elif '=' in i:
#         line = i.strip()
#         left = line.split('=')[0].strip()
#         right = line.split('=')[1].strip()
#         variable.write(str(right) + '\n')
#         vari[left] = right
#         filew.write('def '+str(left)+'():\n\tfile = open("variable", 'r').readlines()'+'\n\t'+'return int(file['+str(index)+'])\n')
#         index = index + 1
        
