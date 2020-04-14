import collections
import sys
import subprocess
from subprocess import PIPE
import threading
import time
import os
from multiprocessing import Process

vari = open('variable').readlines()

for num,j in enumerate(vari):
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

file_2.close()

for proc in procs:
    proc.kill()


# procs = []
# ps = collections.OrderedDict()
# ts = []
# batch = []

# def time_p(p):
#     p.wait()
#     ps[p] = time.time() - ps[p]





# for num in varss:

#     os.chdir('./test_'+str(num))
#     with open(os.devnull, 'w') as fp:
#         proc = subprocess.Popen([sys.executable, 'simulate_changes.py', str([num, (num+1)%3])])
#     # proc = subprocess.Popen([sys.executable, 'simulate_changes.py', str(num)])
#     os.chdir('../')
#     batch.append([num,((num+1)%3)])
#     ps[proc] = time.time()
#     ts.append(threading.Thread(target=time_p, args=(proc,)))
    
#     # procs.append(proc)

    
#     # procs.append(proc)

# for t in ts:
#     t.start()

# for t in ts:
#     t.join()
    

# for prcs, p in zip(batch, ps):
#     print('%s took %s seconds' % (prcs, ps[p]))



def sort_list(list1, list2): 
  
    zipped_pairs = zip(list2, list1) 
  
    z = [x for _, x in sorted(zipped_pairs)] 
      
    return z 
    


for proc in procs:
    proc.kill()