# -*- coding: utf-8 -*-


# import the necessary packages
from PIL import Image
import imagehash
import argparse
import shelve

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required=True, help="path to dataset of images")
ap.add_argument("-s", "--shelve", required=True, help="output shelve database")
ap.add_argument("-q", "--query", required=True, help="path to the query image")
args = vars(ap.parse_args())

# open the shelve database
db = shelve.open(args["shelve"])

# load the query image, compute the difference image hash, and
# and grab the images from the database that have the same hash
# value
query = Image.open(args["query"])
h = str(imagehash.dhash(query))
filenames = db[h]
print("Found %d images" % (len(filenames)))

# loop over the images
for filename in filenames:
    print filename
    # image = Image.open(filename)
    # print(image)  # 为了便于观察，这里打印出来
    # image.show()

# close the shelve database
db.close()
