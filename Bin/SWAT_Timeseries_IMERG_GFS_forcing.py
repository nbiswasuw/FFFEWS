'''
Created on Apr 2, 2018

@author: nishan
'''
def forcing(processdate):
    import os
    import datetime
    from scipy import misc
    start= '20140401'
    end = processdate   
    os.makedirs('./SWAT_Timeseries/' + end)
    for i in xrange(30):
            lat = 25.75 - i*0.1
            for j in range(47):
                lon = 89.65 + j*0.1
                forcingfile = './SWAT_Timeseries/' + end + '/p' + "{0:.3f}".format(lat) + '_' + "{0:.3f}".format(lon) + '.txt'
                forcingline = "20140401"
                with open(forcingfile, 'w') as txt:
                    txt.write(forcingline + '\n')

    startdate = datetime.datetime.strptime(start, '%Y%m%d')
    print(startdate)
    enddate = datetime.datetime.strptime(end, '%Y%m%d')
    print(enddate)
    timedelta = datetime.timedelta(days=1)

    while startdate<=enddate:
        print(startdate)
        preciptime = datetime.datetime.strftime(startdate, '%Y%m%d') #PRCP_1981.01.01.tif
        precippath = '/home/nishan/GBMHydro/IMERG/CropData/' + preciptime + '.tif'
        precip = misc.imread(precippath)
        for i in xrange(30):
            lat = 25.75 - i*0.1
            for j in range(47):
                lon = 89.65 + j*0.1
                forcingfile = './SWAT_Timeseries/' + end + '/p' + "{0:.3f}".format(lat) + '_' + "{0:.3f}".format(lon) + '.txt'
		if precip[i][j] != 65535.0:
	            forcingline = "{0:.2f}".format(precip[i][j])
		else:
		    forcingline = "0.00"
                with open(forcingfile, 'a') as txt:
                    txt.write(forcingline + '\n')
        
        startdate = startdate + timedelta
    frsttime = datetime.datetime.strftime(enddate, '%Y%m%d') #PRCP_1981.01.01.tif
    for frst in xrange(1, 11):
        frstpath = '/home/nishan/FlashFloodForecast/UCAR_Historical/ForecastData/'+ frsttime + '.L' + str(frst) + '.prcp.tif'
        precip = misc.imread(frstpath)
        for i in xrange(30):
            lat = 25.75 - i*0.1
            for j in range(47):
                lon = 89.65 + j*0.1
                forcingfile = './SWAT_Timeseries/' + end + '/p' + "{0:.3f}".format(lat) + '_' + "{0:.3f}".format(lon) + '.txt'
		if precip[i][j] != 65535.0:
	            forcingline = "{0:.2f}".format(precip[i][j])
		else:
		    forcingline = "0.00"
                with open(forcingfile, 'a') as txt:
                    txt.write(forcingline + '\n')

    print 'Done with this part.'

if __name__ == '__main__':
    import datetime
    start = '20180301'
    days=92
    startdate = datetime.datetime.strptime(start, '%Y%m%d')
    for i in xrange(days): 
	timedelta = datetime.timedelta(days=i)
	xdate = startdate + timedelta
	processdate = datetime.datetime.strftime(xdate, '%Y%m%d')
	forcing(processdate)
