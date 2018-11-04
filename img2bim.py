import cv2
import argparse
import beam
import column
import json

if __name__ == "__main__":
  # Construct the argument parse and parse the arguments.
  ap = argparse.ArgumentParser()
  ap.add_argument("-i", "--image", help = "path to the image file")
  args = vars(ap.parse_args())
  image = cv2.imread(args["image"])
  
  model = {
    "beam": beam.find_steel_beams(image),
    "column": column.find_columns(image),
    "grid": [],
    "wall": [],
  }

  print(json.dumps(model, sort_keys=True, indent=4, separators=(',', ': ')))

