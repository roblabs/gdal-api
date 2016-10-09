import numpy as numpy
data = numpy.genfromtxt('../tiff/MY1DMM_CHLORA_2002-07.CSV', delimiter=',')
data.shape


print "0.2, %s" % sum( data [ data < 0.2 ])
print "0.5, %s" % sum( data [ data < 0.5 ])
print "1.0, %s" % sum( data [ data < 1.0 ])
print "2.0, %s" % sum( data [ data < 2.0 ])
print "all, %s" % sum( data [ data < 99999.0 ])

concentrationValues = data [ data != 99999.0]
noDataValues        = data [ data == 99999.0]
total = data.shape[0] * data.shape[1]

totalConcentrationValues = concentrationValues.shape[0]
totalNoDataValues = noDataValues.shape[0]

print "Total count of pixels in image, count of concentration values, count of No Data values"
print "%s, %s, %s" % (total, totalConcentrationValues, totalNoDataValues)
print "Total count == concentraion count + No Data count %s = " % (total == (totalConcentrationValues + totalNoDataValues) )


# compare data to
'''
###
gdal_compute_sum.py --csv -t 0.2 0.5 1.0 2.0 99999.0 -f ../tiff/MY1DMM_CHLORA_2002-07.FLOAT.TIFF

file,concentration count, No Data count,< 0.2,< 0.5,< 1.0,< 2.0,< 99999.0
MY1DMM_CHLORA_2002-07.FLOAT.TIFF,2434211,4045789,173463.460798,306416.076544,435435.518854,524163.342494,1002490.80658

gdalinfo -hist MY1DMM_CHLORA_2002-07.FLOAT.TIFF
Count of NO_DATA = 4045789
  256 buckets   256 buckets from -196.058 to 100195:
  2434211
    0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
  4045789
'''
