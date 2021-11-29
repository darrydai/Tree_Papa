import os
import subprocess
from time import sleep

 
res = subprocess.Popen('ps -ef | grep treePapa',stdout=subprocess.PIPE,shell=True)  
attn=res.stdout.readlines()  
counts=len(attn)  
print (counts)
# while True:
#     sleep(60)
if counts<5:    
    os.system('sudo reboot') 