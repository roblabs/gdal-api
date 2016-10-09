#!/usr/bin/env python2.7
###############################################################################
#
# Python example of GDAL + NumPy
#
###############################################################################

# MIT License
#
# Copyright (c) 2016 ePi Rational, Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


from osgeo import gdal
import numpy
import argparse
import sys
import json

description = '''
Use NumPy to compute the sum of Floating point values in a GeoTIFF

'''
usage = '''
Example,
  gdal_compute_sum.py -h

  # JSON, single file
  gdal_compute_sum.py -j -t 0.5 -f ../tiff/MY1DMM_CHLORA_2002-07_rgb_720x360.FLOAT.tif

  # JSON, multiple files
  gdal_compute_sum.py -j -t 0.5 -f ../tiff/*.FLOAT.tif

  # CSV, multiple threshold, multiple files
  gdal_compute_sum.py -c -t 0.2 0.5 1.0 99999.0 -f ../tiff/*.FLOAT.tif


'''

parser = argparse.ArgumentParser(description=description, epilog = usage, formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('-v', '--verbose', action='store_true', help='print extra information', required=False)
parser.add_argument('-t', '--threshold', nargs='+', type=float, help='Sum data only less than threshold', required=False)
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-c', '--csv', action='store_true', help='output as CSV', required=False)
group.add_argument('-j', '--json', action='store_true', help='output as json', required=False)

parser.add_argument('-f', '--files', nargs='+')
args = parser.parse_args()

NO_DATA = 99999.0

def computeCountConcentration( dataNumpyArray):
  # Read a single Gray scale band Floating Point TIFF into a NumPy Array

  array = dataNumpyArray [ dataNumpyArray != NO_DATA]
  return array.shape[0]

def computeCountNoData( dataNumpyArray):
  # Read a single Gray scale band Floating Point TIFF into a NumPy Array

  array = dataNumpyArray [ dataNumpyArray == NO_DATA]
  return array.shape[0]


def computeSumWithThreshold( dataNumpyArray, threshold):

  # convert to a mesh grid
  grid = numpy.meshgrid(dataNumpyArray)

  # Logical comparison
  #  1)  compute a boolean array of values less than the threshold
  compareThreshold = numpy.less (grid , threshold)

  #  2) compare and extract # TODO Not elegant, but works.  found this at http://stackoverflow.com/a/26511354
  boolThreshold = numpy.logical_and(compareThreshold , grid)

  # Create new array
  lowPlank = numpy.extract(boolThreshold, grid)
  return numpy.sum(lowPlank)


if __name__ == '__main__':

  jsonData = { 'data' : []}

  if( args.csv):
    # print header
    header = "file,concentration count, No Data count"

    for threshold in args.threshold:
      header += ",< "
      header += str(threshold)

    print header


  # if args.threshold is None:
  #   threshold = THRESHOLD
  # else:
  #   threshold = args.threshold

  for f in args.files:
      # split the file name, and retrieve the last item
      filePath = f.split('/')
      fileName = filePath[ len(filePath) - 1]

      datasetname = gdal.Open( f )
      if datasetname is None:
          print('Could not open %s' % args.datasetname)
          sys.exit( 1 )

      floatData = numpy.array(datasetname.GetRasterBand(1).ReadAsArray())

      row = fileName

      countConcentration = computeCountConcentration( floatData)
      countNoData = computeCountNoData( floatData)
      # append data to row
      if( args.csv):
        row += ","
        row += str(countConcentration)
        row += ","
        row += str(countNoData)


      for threshold in args.threshold:

        data = computeSumWithThreshold(floatData, threshold)

        # append data to row
        if( args.csv):
          # print row of data

          row += ","
          row += str(data)

      # once out of the Threshold loop, then print the row
      if( args.csv):
        print row

      jsonData['data'].append({ '%s' % fileName : data})

  if( args.json):
    print json.dumps(jsonData, separators=(',', ': '))
