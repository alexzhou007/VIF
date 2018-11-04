import numpy as np
import cv2
import wall

SAME_LINE_THRESHOLD = 100
SAME_LEVEL_THRESHOLD = 8
SHORT_LINE_LENGTH = 10
BLEED_THRESHOLD = 10

def similar_line_already_found(line, found_lines):
  for fline in found_lines:
    x1, y1, x2, y2 = line
    fx1, fy1, fx2, fy2 = fline
    
    is_vertical_with_range = abs(x1 - x2) < SAME_LEVEL_THRESHOLD
    is_horizental_with_range = abs(y1 - y2) < SAME_LEVEL_THRESHOLD

    # Drop if short line.
    if ((is_horizental_with_range and abs(x1 - x2) < SHORT_LINE_LENGTH) or
       (is_vertical_with_range and abs(y1 - y2) < SHORT_LINE_LENGTH)):
      return True

    xdiff = abs(x1 - fx1) + abs(x2 - fx2)
    ydiff = abs(y1 - fy1) + abs(y2 - fy2)
    diff = xdiff + ydiff
    if diff <= SAME_LINE_THRESHOLD:
      if is_horizental_with_range:
        avg_y = int((y1 + y2 + fy1 + fy2) / 4)
        fline[1] = fline[3] = avg_y
      elif is_vertical_with_range:
        avg_x = int((x1 + x2 + fx1 + fx2) / 4)
        fline[0] = fline[2] = avg_x
      return True

    if is_horizental_with_range and (
      (x1 > fx1 - BLEED_THRESHOLD and x2 < fx2 + BLEED_THRESHOLD) or
      (x1 > fx2 - BLEED_THRESHOLD and x2 < fx1 + BLEED_THRESHOLD)
    ) and abs(ydiff < SAME_LINE_THRESHOLD/2):
      avg_y = int((y1 + y2 + fy1 + fy2) / 4)
      fline[1] = fline[3] = avg_y
      return True
    elif is_vertical_with_range and (
      (y1 > fy1 - BLEED_THRESHOLD and y2 < fy2 + BLEED_THRESHOLD) or
      (y1 > fy2 - BLEED_THRESHOLD and y2 < fy1 + BLEED_THRESHOLD)
    ) and abs(xdiff < SAME_LINE_THRESHOLD/2):
      avg_x = int((x1 + x2 + fx1 + fx2) / 4)
      fline[0] = fline[2] = avg_x
      return True

  return False

def normalize_lines(lines):
  norm_dict = {}
  normalized_lines = []
  for line in lines:
    existing_line = similar_line_already_found(line[0].tolist(), normalized_lines)
    if not existing_line:
      normalized_lines.append(line[0].tolist())

  return normalized_lines


def find_steel_beams(img, debug=False):
  image = wall.remove_walls(img)
  if debug:
    cv2.imshow("Walls/Columns Removed", image)
    cv2.waitKey(0)
  thresh = 50
  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  im_bw = cv2.threshold(gray, thresh, 255, cv2.THRESH_BINARY)[1]
  if debug:
    cv2.imshow("Black And White", im_bw)
    cv2.waitKey(0)

  kernel = np.ones((2,2),np.uint8)
  erosion = cv2.erode(im_bw, kernel, iterations=3)
  if debug:
    cv2.imshow("Erode", erosion)
    cv2.waitKey(0)

  dilation = cv2.dilate(erosion, kernel, iterations=3)
  if debug:
    cv2.imshow("Dilate", dilation)
    cv2.waitKey(0)
  minLineLength = 100
  maxLineGap = 0
  lines = cv2.HoughLinesP(dilation, rho=0.02, theta=np.pi/500, threshold=10, minLineLength=minLineLength, maxLineGap=maxLineGap)
  print("Found %d lines" % len(lines))
  lines = normalize_lines(lines)
  print("Normalized to %d lines" % len(lines))
  for line in lines:
    x1, y1, x2, y2 = line
    cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)

  if debug:
    cv2.imshow("Beam", img)
    cv2.waitKey(0)

  return lines