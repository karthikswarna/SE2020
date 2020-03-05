import collections
import sys
import subprocess
import threading
import time
from multiprocessing import Process

param = int(sys.argv[1])
print(param)

def func_1():
    for i in range(10):
        time.sleep(2)
        f = open('variable').readlines()
        
        fw = open('variable','w')
        for num,i in enumerate(f):
            if num == param:
                fw.write(str(int(i)+1) + '\n')
            else:
                fw.write(str(int(i)) + '\n')    
        fw.close()

def func_2():
    proc = subprocess.Popen([sys.executable, 'target_new.py'])

if __name__ == '__main__':
    p1 = Process(target=func_1)
    p1.start()
    p2 = Process(target=func_2)
    p2.start()
    p1.join()
    p2.join()
    
