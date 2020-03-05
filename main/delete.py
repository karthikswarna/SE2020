import collections
import sys
import subprocess
import threading
import time
import os
from multiprocessing import Process

vari = open('variable').readlines()

for num,j in enumerate(vari):
    cmd1 = 'rd /s /q test_'+str(num)
    try:
        os.system(cmd1)
    except:
        pass