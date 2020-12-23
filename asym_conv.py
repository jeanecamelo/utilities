import numpy as np
from statistics import mean
import matplotlib.pyplot as plt
import math
from datetime import datetime, timedelta

basin = []
cy = []
yyyymmddhh = []
technum = []
tech = []
tau = []
latns = []
lonew = []
vmax = []
mslp = []
ty = []
rad = []
windcode = []
rad1 = []
rad2 = []
rad3 = []
rad4 = []
rrp = []
mrd = []
gusts = []
eye = []
subregion = []
maxseas = []
initials = []
direction = [] 
speed = []
stormname = []
depth = []
seas = []
seascode = []
seas1 = []
seas2 = []
seas3 = []
seas4 = []

#load best track file
f = open('bal092008.dat','r')


for line in f:
    string_list = line.split(',') 
    basin.append(string_list[0])
    cy.append(float(string_list[1]))
    yyyymmddhh.append((string_list[2]))
    technum.append(string_list[3])
    tech.append(string_list[4])
    tau.append(string_list[5])
    latns.append(string_list[6])
    lonew.append(string_list[7])
    vmax.append(float(string_list[8]))
    mslp.append(float(string_list[9]))
    # ty.append(string_list[10])
    # rad.append(float(string_list[11]))
    # windcode.append((string_list[12]))
    # rad1.append(string_list[13])
    # rad2.append(string_list[14])
    # rad3.append(string_list[15])
    # rad4.append(string_list[16])
    # rrp.append(string_list[17])
    # mrd.append((string_list[18]))
    # gusts.append((string_list[19]))
    # eye.append(string_list[20])
    # subregion.append((string_list[21]))
    # maxseas.append((string_list[22]))
    # initials.append(string_list[23])
    # direction.append(string_list[24])
    # speed.append(string_list[25])
    # stormname.append(string_list[26])
    # depth.append(string_list[27])
    # seascode.append((string_list[28]))
    # seas1.append((string_list[29]))
    #seas2.append(string_list[30])
    #seas3.append((string_list[31]))
    #seas4.append(string_list[32])
    
hour=[]
runhour=np.zeros(len(cy))

runhour=np.asarray(runhour, dtype=np.int)

for i in range(len(cy)):
    h=yyyymmddhh[i][-2:]
    float(h)
    hour.append(h)
    


hour=np.asarray(hour, dtype=np.int)

runhour[0]=0
for i in range(1,len(cy)):
    a = hour[i] - hour [i-1]
    if a == -18:
        runhour[i]= 6 + runhour[i-1]
    else:
        runhour[i] = a + runhour[i-1]
        

file = open('bal092008.dat','r')
count=0   

outF = open("fort22.txt", "w")
for line in file:
    a=str(runhour[count])
    b=('{:23s} ASYM,{:>4s},{:100s}'.format(line[0:23],a,line[34:192]))
    print(b)
    outF.write("\n")
    outF.write(b) #This close() is important
    count+=1
outF.close()
   