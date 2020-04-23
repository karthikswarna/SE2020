import collections
import sys
import subprocess
from subprocess import PIPE
import threading
import time
import os
from multiprocessing import Process
import time

vari = open('variable').readlines()

numm = int(sys.argv[1])

ulti_list = []

for i in range(2,2+numm):
    ulti_list.append(int(sys.argv[i]))




print('-------------------------------------------------------')
print(ulti_list)
print('-------------------------------------------------------')

# ulti_list = [1,3,4,5]

for num,j in enumerate(vari):
    if num in ulti_list:
        cmd1 = 'mkdir test_'+str(num)
        try:
            os.system(cmd1)
        except:
            pass
        cmd2 = 'copy variable test_'+str(num)
        cmd3 = 'copy target_new.py test_'+str(num)
        cmd4 = 'copy config.txt test_'+str(num)
        cmd5 = 'copy simulate_changes.py test_'+str(num)
        
        os.system(cmd2)
        os.system(cmd3)
        os.system(cmd4)
        os.system(cmd5)
        

    
    # os.system(cmd_run)

# for num,j in enumerate(vari):
#     cmd1 = 'rd /s /q test_'+str(num)
#     try:
#         os.system(cmd1)
#     except:
#         pass
    
    

procs = []
ps = collections.OrderedDict()
ts = []
batch = []

def time_p(p):
    p.wait()
    ps[p] = time.time() - ps[p]



varss = []
file_ = open("output", "w")

for num,file in enumerate(vari):
    if num in ulti_list:
        varss.append(num)
        os.chdir('./test_'+str(num))
        with open(os.devnull, 'w') as fp:
            proc = subprocess.Popen([sys.executable, 'simulate_changes.py', str([num])], stdout=file_)
        # proc = subprocess.Popen([sys.executable, 'simulate_changes.py', str(num)])
        os.chdir('../')
        batch.append(num)
        ps[proc] = time.time()
        ts.append(threading.Thread(target=time_p, args=(proc,)))
        
    # procs.append(proc)
    
    # procs.append(proc)

for t in ts:
    t.start()

for t in ts:
    t.join()

file_2 = open('output_param', 'w')

for prcs, p in zip(batch, ps):
    file_2.write('Parameter %s took %s seconds\n' % (prcs, ps[p]))



for proc in procs:
    proc.kill()


# procs = []
# ps = collections.OrderedDict()
# ts = []
# batch = []

# def time_p(p):
#     p.wait()
#     ps[p] = time.time() - ps[p]



# file_ = open("output", "a")

# giga = 0
# for num in varss:
#     giga = giga + 1
#     if(giga < 5):
#         os.chdir('./test_'+str(num))
#         with open(os.devnull, 'w') as fp:
#             proc = subprocess.Popen([sys.executable, 'simulate_changes.py', str([num, (num+1)%3])], stdout=file_)
#         # proc = subprocess.Popen([sys.executable, 'simulate_changes.py', str(num)])
#         os.chdir('../')
#         batch.append(str(num) + "," + str((num+1)%3))
#         ps[proc] = time.time()
#         ts.append(threading.Thread(target=time_p, args=(proc,)))
    
#     # procs.append(proc)

    
#     # procs.append(proc)

# for t in ts:
#     t.start()

# for t in ts:
#     t.join()
    
# file_2 = open('output_param', 'a')

# for prcs, p in zip(batch, ps):
#     file_2.write('Parameter %s took %s seconds\n' % (prcs, ps[p]))






file_.close()

# def sort_list(list1, list2): 
  
#     zipped_pairs = zip(list2, list1) 
  
#     z = [x for _, x in sorted(zipped_pairs)] 
      
#     return z 
    






ttt = int(sys.argv[1])

# Printing the fitness scores in output_param file.
file_2.write('  ====  ===  ====  =======  =======  ====\n')

while(True):
    file_3 = open('output', 'r')
    lines = file_3.readlines()
    a = 0
    for k in lines:
        if k.find("generation 4")!=-1:
            a = a + 1
    if a >= numm:
        break
    else:
        file_3.close()
    

print(" -----------------------------------------------------------------------------")
flag = False
for line in lines:
    if(flag == True):
        file_2.write(line)
        flag = False

    if line == "  ====  ===  ====  =======  =======  ====\n":
        flag = True

file_2.close()
file_3.close()






for proc in procs:
    proc.kill()