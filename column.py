import numpy as np
import cv2


MAX_COLUMN_WIDTH = 100
MAX_COLUMN_HEIGHT = 100

def find_columns(img, debug=False):
  rimg = cv2.bitwise_not(img)
  kernel = np.ones((5,5),np.uint8)
  lower = np.array([190, 190, 190])
  upper = np.array([195, 195, 195])
  initial_mask = cv2.inRange(img, lower, upper)
  if debug:
    cv2.imshow("initial_mask", initial_mask)
    cv2.waitKey(0)
  erosion = cv2.erode(initial_mask,kernel,iterations = 1)
  if debug:
    cv2.imshow("erosion", erosion)
    cv2.waitKey(0)

  dilation = cv2.dilate(erosion, kernel, iterations=2) 
  if debug:
    cv2.imshow("dilation", dilation)
    cv2.waitKey(0)

  final_mask_walls = cv2.bitwise_not(dilation)
  if debug:
    cv2.imshow("final_mask_walls", final_mask_walls)
    cv2.waitKey(0)

  _, contours, h = cv2.findContours(final_mask_walls,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
  print("Found %d areas" % len(contours))
  contours_bound = []
  for contour in contours:
    (x,y,w,h) = cv2.boundingRect(contour)
    if w < MAX_COLUMN_WIDTH and h < MAX_COLUMN_HEIGHT:
      cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
      contours_bound.append((x,y,w,h))

  print("Normalized to %d columns" % len(contours_bound))

  if debug:
    cv2.imshow("Columns", img)
    cv2.waitKey(0)

  return contours_bound
