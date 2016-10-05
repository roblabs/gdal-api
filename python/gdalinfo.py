#!/usr/bin/env python2.7
###############################################################################
#
# Python example of gdalinfo
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
import argparse
import sys

description = '''
lists information about a raster dataset

'''
usage = '''
This Python wrapper is not intended to replace the command option
It is intended to help you learn how Python bindings work with GDAL

See this link if you need more than this Python wrapper
  http://www.gdal.org/gdalinfo.html

Example,
  gdalinfo.py ../tiff/MY1DMM_CHLORA_2002-07.TIFF

'''

parser = argparse.ArgumentParser(description=description, epilog = usage, formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('datasetname')
args = parser.parse_args()


if __name__ == '__main__':

  datasetname = gdal.Open( args.datasetname )
  if datasetname is None:
      print('Could not open %s' % args.datasetname)
      sys.exit( 1 )

  print "Driver: %s/%s" % (datasetname.GetDriver().ShortName, datasetname.GetDriver().LongName)
  print "Size is %d, %d" %(datasetname.RasterXSize, datasetname.RasterYSize)
  print "Bands = %d" % datasetname.RasterCount
  print "Coordinate System is:", datasetname.GetProjectionRef ()
  print "GetGeoTransform() = ", datasetname.GetGeoTransform ()
  print "GetMetadata() = ", datasetname.GetMetadata ()
