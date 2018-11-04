import numpy as np
import cv2

def find_walls(img):
  pass

def remove_walls(img):
  rimg = cv2.bitwise_not(img)
  kernel = np.ones((5,5),np.uint8)
  lower = np.array([190, 190, 190])
  upper = np.array([195, 195, 195])
  initial_mask = cv2.inRange(img, lower, upper)
  erosion = cv2.erode(initial_mask,kernel,iterations = 1)
  
  dilation = cv2.dilate(erosion, kernel, iterations=2) 
  final_mask_walls = cv2.bitwise_not(dilation)

  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  image = cv2.bitwise_and(rimg, rimg, mask=final_mask_walls)
  return image
