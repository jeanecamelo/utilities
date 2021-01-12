#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 13:43:52 2021

@author: camelo
"""
import netCDF4
import numpy as np
import math
import geopy.distance
from ismember import ismember
import math

##note for the coords, the lat goes first
def area_heron(A,B,C):
    coords_1 = A
    coords_2 = B
    coords_3 = C

    s1 = (geopy.distance.geodesic(coords_1, coords_2).m)
    s2 = (geopy.distance.geodesic(coords_2, coords_3).m)
    s3 = (geopy.distance.geodesic(coords_1, coords_3).m)

    s_tot = 0.5*(s1+s2+s3)
    area = math.sqrt((s_tot*(s_tot-s1)*(s_tot-s2)*(s_tot-s3)))
    return(area)

maxele = netCDF4.Dataset("/Users/camelo/Documents/Dissertation/scripts/Ike_CTRL_maxele.63.nc","r")

# get variables from maxele.63 file
x  = maxele.variables["x"][:]
y = maxele. variables["y"][:]
zeta_max = maxele.variables["zeta_max"][:]
depth = maxele.variables["depth"][:]
element = maxele.variables["element"][:] -1# how nodes are connected as elements 3xnum(element)
element = np.array(element)
lon = np.array(x)
lat = np.array(y)
height = np.array(zeta_max)

##  find nodes that are in land
land_node=[]
for i in range(len(depth)):
    if depth[i]<0:
        land = i
        land_node.append(land)

land_element=[]

i=[]
[i,dx]=ismember(element[:,0],land_node) 
[j,dy]=ismember(element[:,1],land_node)
[k,dz]= ismember(element[:,2],land_node)

l = np.zeros((len(element),3))
l[:,0]=i
l[:,1]=j
l[:,2]=k

water_element=[]

for i in range(len(element)):
    if l[i,0] and l[i,1] and l[i,2] ==1:
        land = i
        land_element.append(land)
    else:
        water=i
        water_element.append(water)
A=[]
B=[]
C=[]
# Saves the corresponding node number of each element
A = np.take(element[:,0],land_element[:])
B = np.take(element[:,1],land_element[:])
C = np.take(element[:,2],land_element[:])

# also need to change the index to correspond to python indexing that starts at 0.
for i in range(0,len(A)):
    A[i]=A[i]-1
    B[i]=B[i]-1
    C[i]=C[i]-1
    
area_ele=[]
ele_height =[]

# pass to function
for i in range(len(land_element)):
    area = area_heron((lat[A[i]],lon[A[i]]),(lat[B[i]],lon[B[i]]),(lat[C[i]],lon[C[i]]))
    area_ele.append(area)
    ele_h= (depth[A[i]]+depth[B[i]]+depth[C[i]])/3
    ele_height.append(ele_h)
    
totalArea = sum(area_ele)
totalTopo = sum(ele_height)

#need to run the following for each storm
#initially assume everything is wet, then subtract off dry elements in loop below
wetArea = totalArea
wetTopo = totalTopo
print(totalArea*0.000001, "m^2")
height = np.where(height==-99999.0, 0, height) #replace dry nodes with 0s, this assumes maxele.63 gives water elevation above topography

dry_ele_height = []
vol_ele =[]
wet_ele_height=[]
wet_count=[]
dry_count=[]
for i in range(len(land_element)):
    height_0  = height[A[i]]
    height_1  = height[B[i]]
    height_2  = height[C[i]]

    if height_0 < 0.001 and height_1 < 0.001 and height_2 < 0.001: #if all three nodes are dry
        vol = 0 #set volume to 0
        vol_ele.append(vol)
        wetArea = wetArea - area_ele[i]#subtract off area of this element from wetArea calculation
        dry_ele_height.append(ele_height[i])
        dry_count.append(i)  # count how many elements were not part of the sum

       
    else:
        vol = (1/3)*(area_ele[i])*(height_0+height_1+height_2)
        vol_ele.append(vol)
        wet_ele_height.append(ele_height[i])
        wet_count.append(i)

totalVol = sum(vol_ele)
total_wet_depth = sum(wet_ele_height)
print("Sum of all wet depth:", total_wet_depth,"m")
print(total_wet_depth/len(wet_count),"m")
print("Highest Topo:", min(wet_ele_height),"m")
print(wetArea*0.000001,"km^2")
print(totalVol*.000000001,"km^3")
print("Total wet elements:",len(wet_count))
print("Total dry elements:",len(dry_count))
print(len(wet_count)+len(dry_count))
print(len(area_ele))
        