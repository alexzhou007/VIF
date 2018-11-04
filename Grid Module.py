#Grid Module

#Import Module

import cv2
import numpy as np
import matplotlib.pyplot as plt

#Import Photo and Template-----------------
img_res_f = cv2.imread('floor.jpg',1)
img_res = cv2.imread('floor.jpg',0)


#Grid Lookup-----------------
threshold=0.2
#Import bubble template
img_f=cv2.imread('bubble2.jpg', 0)
w, h=img_f.shape[::-1]
res = cv2.matchTemplate(img_res,img_f,cv2.TM_CCOEFF_NORMED)
loc = np.where(res>=threshold)

#Tolerance to get rid of repeating pixal
tolerance=3
allfind=[]
new=[]
for pt in zip(*loc[::-1]):
        allfind.append(pt)
        cv2.rectangle(img_res_f, pt,(pt[0]+w,pt[1]+h),(0,50,255),3)

allfind.sort()
print(allfind)
new.append(allfind[0])
n=0
for n in range(1,len(allfind)):
        if abs(allfind[n-1][0]-allfind[n][0]) or abs(allfind[n-1][1]-allfind[n][1])>=tolerance:
                new.append(allfind[n])
                
#Centroid of found object
n=0
centroid=[]
print(len(new))
for n in range(0,len(new)):
          centroid.append([new[n][0]+int(w/2), new[n][1]+int(h/2)])
          cv2.circle(img_res_f,(new[n][0]+int(w/2),new[n][1]+int(h/2)), 10, (0,255,0), -1)
          font = cv2.FONT_HERSHEY_SIMPLEX
          cv2.putText(img_res_f,'C'+str(new[n][0]+int(w/2))+','+str(new[n][1]+int(h/2)),(new[n][0]+int(w/2),new[n][1]+int(h/2)), font, 1, (155,155,155), 5, cv2.LINE_AA)
print(centroid)


#Classify NS or EW grid
xmax=max([l[0] for l in centroid])
xmin=min([l[0] for l in centroid])
ymax=max([l[1] for l in centroid])
ymin=min([l[1] for l in centroid])
NSgrid=[]
EWgrid=[]
for n in range(0,len(centroid)):
               if (abs(centroid[n][0]-xmax)<=3 or abs(centroid[n][0]-xmin) <=3):
                       if abs(centroid[n][1]-ymax)>=3 and abs(centroid[n][1]-ymin)>=3:
                               EWgrid.append(centroid[n])
                       else: NSgrid.append(centroid[n])        
               else:        
                       NSgrid.append(centroid[n])
               
print('EW',EWgrid)
print('NS',NSgrid)
print(xmax,xmin)
print(ymax,ymin)
plt.imshow(img_res_f, cmap = 'gray')
plt.show()



