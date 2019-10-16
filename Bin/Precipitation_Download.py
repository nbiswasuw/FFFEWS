#!"C:\Users\nbiswas\Anaconda2\python.exe"
'''
Created on Jan 15, 2019

@author: nbiswas
'''
import datetime
import urllib
import urllib2
import subprocess
import requests
import h5py
# import pandas as pd
import os
import shutil
# import numpy as np
# import rasterio
import csv
import sqlite3
import paramiko
from scp import SCPClient


class FFFEWSSystem():
    def __init__(self):
        self.todaydate = datetime.date.today()
        self.noforedays = 5
        self.swatstartdate = datetime.datetime.combine(datetime.date(2016,1,1), datetime.time(0,0))
        self.forestartdate =  datetime.datetime.combine(self.todaydate, datetime.time(0,0)) + datetime.timedelta(days=0)
        self.imergprcpdate = datetime.datetime.combine(self.todaydate, datetime.time(0,0)) + datetime.timedelta(days=-1)
        self.rasstartdate = self.forestartdate + datetime.timedelta(days=-8)
        self.visstartdate = self.forestartdate + datetime.timedelta(days=-21)
        self.foreenddate = datetime.datetime.combine(self.todaydate, datetime.time(0,0)) + datetime.timedelta(days=self.noforedays)
        self.conn = sqlite3.connect('Insituwaterlevel.db')
        print self.todaydate, self.forestartdate, self.foreenddate
        
        
    def imergprecip(self):
        strdate = self.imergprcpdate.strftime("%Y%m%d")
        todayyr = self.imergprcpdate.strftime("%Y")
        todaymonth = self.imergprcpdate.strftime("%m")
        path = r'ftp://saswe@uw.edu:saswe@uw.edu@jsimpson.pps.eosdis.nasa.gov/NRTPUB/imerg/gis/early/' + todayyr + '/' + todaymonth + '/3B-HHR-E.MS.MRG.3IMERG.' + strdate + '-S233000-E235959.1410.V06B.1day.tif'
        print todayyr, todaymonth, strdate, path
        fpath = r'../Precipitation/IMERG/precip.imerg.' + strdate + '.tif'
        urllib.urlretrieve(path, fpath)
        os.system('C:\OSGeo4W64\OSGeo4W.bat gdalwarp -of GTiff -tr 0.1 0.1 -te 89.60 22.8 94.25 25.80 -overwrite ' + fpath + ' ../Precipitation/IMERG/meghna.precip.imerg.' + strdate + '.tif')
        os.system('C:\OSGeo4W64\OSGeo4W.bat gdal_translate -of AAIGrid ../Precipitation/IMERG/meghna.precip.imerg.' + strdate + '.tif ../Precipitation/IMERG/meghna.precip.imerg.' + strdate + '.asc')
        os.system('precip_unit_modification.py ../Precipitation/IMERG/meghna.precip.imerg.' + strdate + '.asc')
#         with open(r'IMERG_translate_unit.bat', 'w') as txt:
#             txt.write('gdalwarp -of GTiff -tr 0.1 0.1 -te 89.60 22.8 94.25 25.80 -overwrite ' + fpath + ' ../Precipitation/IMERG/meghna.precip.imerg1.' + strdate + '.tif\n"C:\OSGeo4W64\OSGeo4W.bat" gdal_calc -A ../Precipitation/IMERG/meghna.precip.imerg1.' + strdate + '.tif --outfile=../Precipitation/IMERG/meghna.precip.imerg.' + strdate + '.tif --calc="A/10"')
#         urllib.urlcleanup()
#         os.system("C:\OSGeo4W64\OSGeo4W.bat IMERG_translate_unit.BAT")
        print "IMERG Precipitation data processed successfully."

        
    def gsmapprecip(self):
        print "GSMaP download facility is under development"
        os.system("C:\OSGeo4W64\OSGeo4W.bat Resample_Aggregate_GFS_Precip.BAT")



    def gfsforecastprecip(self):
        batfile = 'GFS_Resample_Aggregate_Precip.BAT'
        with open(batfile, 'w') as txt:
            txt.write("")
    #     user, password = 'nbiswas@uw.edu', 'ArindamMou_07'
        strdate = self.forestartdate.strftime("%Y%m%d")
        todayyr = self.forestartdate.strftime("%Y")
        todaymonth = self.forestartdate.strftime("%m")
#         todayday = self.forestartdate.strftime("%d")
    
        time = '00'
        print todayyr, todaymonth, strdate
        for forecasthr in range(24, (self.noforedays+1)*24+1, 24):
            ## Data from NCEP NOaa
            path = r'https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl?file=gfs.t' + time + 'z.pgrb2.0p25.f' + str(forecasthr).zfill(3) + '&var_APCP=on&subregion=&leftlon=60&rightlon=100&toplat=40&bottomlat=10&dir=%2Fgfs.' + strdate+ '%2F' + time
            print strdate, forecasthr, path
            fpath = r'../Precipitation/GFS/precip.gfs.' + strdate + time + str(forecasthr).zfill(3) + '.tif'
            urllib.urlretrieve(path, fpath)
            urllib.urlcleanup()
            os.system('C:\OSGeo4W64\OSGeo4W.bat gdalwarp -of GTiff -tr 0.1 0.1 -te 89.60 22.8 94.25 25.80 ' + fpath + ' ../Precipitation/GFS/meghna.precip.gfs.' + strdate + '.f' + str(forecasthr).zfill(3) + '.tif')
            os.system('C:\OSGeo4W64\OSGeo4W.bat gdal_translate -of AAIGrid -a_nodata -9999 ../Precipitation/GFS/meghna.precip.gfs.' + strdate + '.f' + str(forecasthr).zfill(3) + '.tif -b 1 ../Precipitation/GFS/meghna.precip.gfs.'  + strdate + '.f' + str(forecasthr).zfill(3) + '.asc')
        
            ## Forecast from NCAR UCAR Server
    #         hrs = int(time) + forecasthr
    #         foredate = (datetime.datetime(int(todayyr), int(todaymonth), int(todayday),0,0,0) + datetime.timedelta(hours = hrs)).strftime("%Y-%m-%dT%H")
    #         print foredate
    #         path =  "https://rda.ucar.edu/thredds/ncss/grid/files/g/ds084.1/" + todayyr + "/" + todaydate + "/gfs.0p25." + todaydate + time + ".f" + str(forecasthr).zfill(3) + ".grib2?var=Total_precipitation_surface_6_Hour_Accumulation&north=40&west=60&east=100&south=10&horizStride=1&time_start=" + foredate + "%3A00%3A00Z&time_end=" + foredate + "%3A00%3A00Z&timeStride=1&vertCoord=&accept=netcdf"
    #         resp = requests.get(path, auth=(user, password))
    #         if resp.status_code == 200:
    #             with open("../Precipitation/GFS/precip.gfs." + todaydate + ".f" + str(forecasthr).zfill(3) + '.nc', 'wb') as f:
    #                 f.write(resp.content)
        print "Done"
    def ecmwfforecastprecip(self):
        today = self.forestartdate
        xllcorner = 89.65
        yllcorner = 25.75
        gridsize = 0.1
        ncols = 47
        nrows = 30
        prcpvals = []
        for y in xrange(nrows):
            nodey = "{0:0.2f}".format(yllcorner - y*gridsize)
            for x in xrange(ncols):
                nodex = "{0:0.2f}".format(xllcorner + x*gridsize)
                print  nodey + r"/" + nodex
#                 print "https://node.windy.com/forecast/v4/ecmwf/" + nodey + r"/" + nodex
                incontent = urllib2.urlopen("https://node.windy.com/forecast/v4/ecmwf/" + nodey + r"/" + nodex).read()
                dd = incontent.split('{')[16]
#                 print dd
                datestr = dd.split(']')[0].split('[')[1].replace('"', '').split(',')
                hrstr = dd.split(']')[1].split('[')[1].split(',')
                strmm = ''
                for t in dd.split(']'):
                    if 'mm' in t:
                        strmm = t
                mmstr = strmm.split('[')[1].split(',')
                outdate = []
                outprcp = []
                
                for i in xrange(len(datestr)):
                    indate = datetime.datetime.strptime(datestr[i], "%Y-%m-%d")
                    hrs = int(hrstr[i])
                    outdate.append(indate + datetime.timedelta(hours = hrs))
                    outprcp.append(float(mmstr[i]))

                prcpvals.append(outprcp)
        print len(prcpvals), len(prcpvals[0])

        for lead in range(1, len(outdate)):
            try:
                if int(outdate[lead].strftime("%H"))%6 == 0.0:
                    leadhours = (outdate[lead]-today).total_seconds()/3600.0
                    print lead, leadhours, outdate[lead].strftime("%Y-%m-%d %H%M%S")
                    stroutput = "ncols        47\nnrows        30\nxllcorner    89.60\nyllcorner    22.80\ncellsize     0.100000\nNODATA_value  -9999.00"
                    for row in xrange(nrows):
                        stroutput = stroutput + "\n "
                        for col in xrange(ncols):
                            stroutput = stroutput + "{0:.2f}".format(prcpvals[row*ncols+col][lead] + prcpvals[row*ncols+col][lead-1]) + " "
                    with open(r'../Precipitation/ECMWF/meghna.precip.ecmwf.' + today.strftime("%Y%m%d") + '.f' + str(int(leadhours)).zfill(3) + '.asc', 'w') as txt:
                        txt.write(stroutput)
            except:
                continue        
    def ffwcobsdata(self):
        stationids = [1,2,4,6,10,12,13,14,17,18,19,20,21,22,23,24,25,27,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,86,87,89,91,93,95,96,97,98,99,100,101,103,105,108]
        for station in stationids:
            incontent = urllib2.urlopen("http://www.ffwc.gov.bd/ffwc_charts/index.php?stid=" +str(station)).readlines()
            stationarray = incontent[23].split()
            stationname = stationarray[stationarray.index('at')+1]
            if stationname == 'B.':
                stationname = 'B. Baria'
            elif stationname == 'Sherpur-Sylhet':
                stationname = 'Sherpur'
            elif stationname == 'Lourergorh':
                stationname = 'Lourergarh'
            
            print stationname, incontent[67].replace('                data: ', '')          
            dd = incontent[67].replace('                data: ', '')
            if dd!='[]\n':
                indates = []
                inwls = []
                x = dd.replace('Date.UTC(', '').replace(')', '').replace(' ', '').replace('[[', '').replace(']]', '').replace('],[', ';')
                for t in x.split(';'):
                    incont = t.split(',')
                    obsdate = datetime.datetime.combine(datetime.date(int(incont[0]), int(incont[1])+1, int(incont[2])), datetime.time(int(incont[3]), int(incont[4])))
                    obswl = float(incont[5])
                    indates.append(obsdate)
                    inwls.append(obswl)
                print stationname, indates, inwls
                
                for index in xrange(len(indates)):
                    self.conn.text_factory = str
                    c = self.conn.cursor()
                    indate = indates[index]
                    inwl = inwls[index]
                    c.execute("REPLACE into Waterlevel(Station,Date,WL) VALUES(?,?,?)", (stationname,indate,inwl))
        self.conn.commit()
                
                        
    
    def dailyprcpcalc(self, ftype='GFS'):
        nrows = 30
        ncols = 47
        preciptime = self.forestartdate.strftime('%Y%m%d') #meghna.precip.imerg.20160101.tif
        if ftype =='GFS':
            missftype = 'ECMWF'
        else:
            missftype = 'GFS'
        for leadday in xrange(self.noforedays+1):
            prcpvals = [0]*nrows*ncols
            print len(prcpvals)
            for hrindex in range(4):
                forecasthr = leadday*24+hrindex*6 + 6
                precippath = '../Precipitation/' + ftype + r'/meghna.precip.' + ftype.lower() + '.' + preciptime + '.f' + str(forecasthr).zfill(3) + '.asc'
                if os.path.exists(precippath) == False:
                    precippath = '../Precipitation/' + missftype + r'/meghna.precip.' + missftype.lower() + '.' + preciptime + '.f' + str(forecasthr).zfill(3) + '.asc'
                if os.path.exists(precippath) == True:
                    strcontent = open(precippath, 'r')
                    lines = strcontent.readlines()
                    for i in xrange(nrows):
                        elements = lines[i+6].split(' ')
                        for j in range(ncols):
                            prcpvals[i*ncols+j] = prcpvals[i*ncols+j] + float(elements[j+1])
                        
            stroutput = "ncols        47\nnrows        30\nxllcorner    89.60\nyllcorner    22.80\ncellsize     0.100000\nNODATA_value  -9999.00"
            for row in xrange(nrows):
                stroutput = stroutput + "\n "
                for col in xrange(ncols):
                    stroutput = stroutput + "{0:.2f}".format(prcpvals[row*ncols+col]) + " "
            with open(r'../Precipitation/' + ftype + r'/meghna.precip.' + ftype.lower() + '.' + preciptime + '.L' + str(leadday) + '.asc', 'w') as txt:
                txt.write(stroutput)

    def swatforcing(self, hindcast="IMERG"):
        enddate = self.forestartdate 
                
        preciptime = (enddate + datetime.timedelta(days=-1)).strftime('%Y%m%d') #meghna.precip.imerg.20160101.tif
        precippath = '../Precipitation/' + hindcast + r'/meghna.precip.imerg.' + preciptime + '.asc'
        strcontent = open(precippath, 'r')
        lines = strcontent.readlines()
        for i in xrange(30):
            lat = 25.75 - i*0.1
            elements = lines[i+6].split(' ')
            for j in range(47):
                lon = 89.65 + j*0.1
                forcingfile = '../SWATInput/IMERG/p' + "{0:.3f}".format(lat) + '_' + "{0:.3f}".format(lon) + '.txt'
                forcingline = "{0:.2f}".format(float(elements[j+1]))
                with open(forcingfile, 'a') as txt:
                    txt.write(forcingline + '\n')
        for ftype in ['GFS', 'ECMWF']:
            if os.path.exists(r'../SWATInput/' + ftype + r'/' + enddate.strftime("%Y%m%d")) == False:
                os.makedirs(r'../SWATInput/' + ftype + r'/' + enddate.strftime("%Y%m%d"))

            for i in xrange(30):
                    lat = 25.75 - i*0.1
                    for j in range(47):
                        lon = 89.65 + j*0.1
                        forcingfile = r'../SWATInput/IMERG/p' + "{0:.3f}".format(lat) + '_' + "{0:.3f}".format(lon) + '.txt'
                        outfile = r'../SWATInput/' + ftype + r'/' + enddate.strftime("%Y%m%d") + '/p' + "{0:.3f}".format(lat) + '_' + "{0:.3f}".format(lon) + '.txt'
                        shutil.copy(forcingfile, outfile)
    
    
    #      
            for frst in xrange(self.noforedays+1):
                frsttime = datetime.timedelta(days=frst)
                print (enddate + frsttime).strftime("%Y%m%d")
                frstpath = '../Precipitation/' + ftype + r'/meghna.precip.' + ftype.lower() + '.' + enddate.strftime("%Y%m%d") + '.L' + str(frst) + '.asc' ##meghna.precip.gfs.20190127.tif
                strcontent = open(frstpath, 'r')
                lines = strcontent.readlines()
                for i in xrange(30):
                    elements = lines[i+6].split(' ')
    #                 print elements
                    lat = 25.75 - i*0.1
                    for j in range(47):
                        lon = 89.65 + j*0.1
                        forcingfile = '../SWATInput/' + ftype + r'/' + enddate.strftime("%Y%m%d") + '/p' + "{0:.3f}".format(lat) + '_' + "{0:.3f}".format(lon) + '.txt'
                        forcingline = "{0:.2f}".format(float(elements[j+1]))
                        with open(forcingfile, 'a') as txt:
                            txt.write(forcingline + '\n')
    
        print 'Done with this part.'
    def updateimerg(self):
        startdate = self.swatstartdate
        enddate = self.forestartdate 
        for i in xrange(30):
            lat = 25.75 - i*0.1
            for j in range(47):
                lon = 89.65 + j*0.1
                forcingfile = '../SWATInput/IMERG/p' + "{0:.3f}".format(lat) + '_' + "{0:.3f}".format(lon) + '.txt'
                forcingline = startdate.strftime('%Y%m%d')
                with open(forcingfile, 'w') as txt:
                    txt.write(forcingline + '\n')
        
        while startdate<enddate:
            preciptime = startdate.strftime('%Y%m%d') #meghna.precip.imerg.20160101.tif
            print preciptime
            precippath = '../Precipitation/IMERG/meghna.precip.imerg.' + preciptime + '.asc'
            strcontent = open(precippath, 'r')
            lines = strcontent.readlines()
            for i in xrange(30):
                lat = 25.75 - i*0.1
                elements = lines[i+6].split(' ')
                for j in range(47):
                    lon = 89.65 + j*0.1
                    forcingfile = '../SWATInput/IMERG/p' + "{0:.3f}".format(lat) + '_' + "{0:.3f}".format(lon) + '.txt'
                    forcingline = "{0:.2f}".format(float(elements[j+1]))
                    with open(forcingfile, 'a') as txt:
                        txt.write(forcingline + '\n')
            startdate = startdate + datetime.timedelta(days=1)
        
            
    def swatprecipprep(self, ftype='GFS'):
        templatepath=r"pcpSample.pcp"
        precippath = r"../SWATModel_" + ftype + "/pcp1.pcp"
        startdate = self.swatstartdate
        forecastdate = self.forestartdate
        enddate = self.foreenddate
        ffile = open(templatepath, 'r')
        lines = ffile.readlines()
        stations=lines[0].replace('Station  ','').replace(',\n','').split(',')
        days = (enddate - startdate).days + 1
        print(days)
        pcp=[]
        for i in xrange(days):
            x=datetime.timedelta(days=i)
            pcp.append(datetime.datetime.strftime(startdate+x, "%Y%j"))
            
        print pcp[0]
        print pcp[len(pcp)-1]
        print len(pcp)
        for station in stations:
            p = open(r'../SWATInput/' + ftype + r'/' + forecastdate.strftime("%Y%m%d") + '/' + station + '.txt', 'r')
            plines=p.readlines()
            for j in range(1,len(pcp)+1):
                pcp[j-1]=pcp[j-1]+ '{0:.1f}'.format(float(plines[j].rstrip())).zfill(5)
        print pcp[0]
        strcontent = lines[0] + lines[1] + lines[2] + lines[3] + "\n".join(pcp)
    
        with open(precippath,'w') as txt:
            txt.write(strcontent)
        print "Scuccessful"
        
    def swatsimulation(self, ftype='GFS'):
        configpath=r"../SWATModel_" + ftype + "/file.cio"
        startdate = self.swatstartdate
        startyear = int(startdate.strftime("%Y"))
        enddate= self.foreenddate
        
        year=int(datetime.datetime.strftime(enddate, "%Y"))
        julianday=datetime.datetime.strftime(enddate, "%j")
    
        simyr=year-startyear+1
        ffile = open(configpath, 'r')
        lines = ffile.readlines()
    
        line7 = list(lines[7])
        line7[15] = str(simyr)
        lines[7] = ''.join(line7)
    
        line10 = list(lines[10])
        if len(julianday)==1:
            line10[13]=' '
            line10[14]=' '
            line10[15]=julianday
        elif len(julianday)==2:
            line10[13]=' '
            line10[14]=julianday[0]
            line10[15]=julianday[1]
        else:
            line10[13]=julianday[0]
            line10[14]=julianday[1]
            line10[15]=julianday[2]
    
        lines[10] = ''.join(line10)
    
        ffile=open(configpath,'w')
        ffile.write("".join(lines))
        
        
        os.chdir("../SWATModel_" + ftype + r'/')
        p = subprocess.Popen("./swat2012.exe")
        p.wait()
        os.chdir("../Bin")
        shutil.copy('../SWATModel_' + ftype + '/output.rch', '../SWATOutput/Results_SWAT_' + ftype + '_' + self.forestartdate.strftime("%Y%m%d") + '.rch')
    
    def swatoutputprocessor(self, ftype='GFS'):
            stations = {'Ballah':217,'BhairabBazar': 196,'Haziganj':76,'Amalshid':110,'Karimganj':119,'Lubachara':58,'Lalakhal':38,'Tamabil':30,'Patrokhola':206,'Sharifpur':187,'Fultola':148,'Nakuagaon':47,'Malijhi':26,'Chelakhali':25,'Bijoypur':66,'Nitai':68,'Sunamganj':39,'Jadukata':49,'DoyarBazar':41,'Bichanakandi':34,'Lourergarh':57}
            reach=[26, 47, 68, 25, 57, 39, 49, 41, 66, 30, 38, 58,76, 110, 119, 148, 187, 206, 217, 34, 196]
            print len(stations), len(reach)

            
            start = self.forestartdate.strftime("%Y%m%d")
            if os.path.exists(r'../SWATOutput/' + ftype + r'/' + start) == False:
                os.makedirs(r'../SWATOutput/' + ftype + r'/' + start)
            for reac in xrange(len(reach)):
                print reach[reac]
                fname = '../SWATOutput/' + ftype + r'/' + start  + '/' + str(reach[reac]) + '.txt'
                with open(fname, 'w') as txt:
                    txt.write('')
                      
                infile = '../SWATOutput/Results_SWAT_' + ftype + '_' + start + '.rch'
                filep = open(infile, 'r')
                reader = filep.readlines()
                for i in range(10, len(reader)):
                    lines=reader[i].split()
                    if int(lines[1].strip())==reach[reac]:
                        with open(fname, 'a') as txt:
                            if reach[reac] == 196:
                                txt.write(str(-1.0*float(lines[6]))+'\n')
                            else:
                                txt.write(str(float(lines[6]))+'\n')
                        
            startdate = self.swatstartdate + datetime.timedelta(days=366);
            if os.path.exists(r'../FinalOutputs/Inflow/' + ftype + r'/' + start) == False:
                os.makedirs(r'../FinalOutputs/Inflow/' + ftype + r'/' + start)
                
            for station in stations:
                startdate = self.swatstartdate + datetime.timedelta(days=366);
                strcontent = "Date,Streamflow(cumecs)\n"
                infile = open('../SWATOutput/' + ftype + r'/' + start  + '/' + str(stations[station]) + '.txt', 'r')
                outfile = r'../FinalOutputs/Inflow/' + ftype + r'/' + start + r'/' + station.lower() + '.txt'
                fcontent = infile.readlines()
                for line in fcontent:
                    startdate = startdate+ datetime.timedelta(days=1)
                    if startdate>=self.visstartdate:
                        if startdate<self.forestartdate:
                            strcontent = strcontent + startdate.strftime("%Y-%m-%d") + ',' + "{0:0.1f}".format(float(line.rstrip())) + ',,' + '\n'
                        elif startdate == self.forestartdate:
                            strcontent = strcontent + startdate.strftime("%Y-%m-%d") + ',' + "{0:0.1f}".format(float(line.rstrip())) + ',' + "{0:0.1f}".format(float(line.rstrip())) + '\n'
                        else:
                            strcontent = strcontent + startdate.strftime("%Y-%m-%d") + ',,' + "{0:0.1f}".format(float(line.rstrip())) + '\n'
                with open(outfile, 'w') as txt:
                    txt.write(strcontent)
                
                   
                            
    def rasbndgen(self, ftype='GFS'):
        forecastdate = self.forestartdate.strftime("%Y%m%d")
        todaydate = self.forestartdate
        rsttime = datetime.timedelta(days = -9)
        rstdate = datetime.datetime.strftime(todaydate + rsttime, "%d%b%Y").upper()
        print rstdate
        
        unsteadyfname = '../HecrasModel_' + ftype + '/unsteady2D.u01'
        strcontent = "Flow Title=IMERG_" + ftype + "_Forecast_" + forecastdate + "\nProgram Version=5.05\nUse Restart=-1\nRestart Filename=Unsteady2D.p01." + rstdate + r" 2400.rst" + "\n"
        dates = (self.foreenddate-self.swatstartdate).days + 1
        print dates
        ## 2D flow area precipitation data
        precipGridf = open('Precip_Grids.txt', 'r')
        precipgrids = precipGridf.readlines()
        gridprcp = [0] * dates
        count = len(precipgrids)
        for grid in precipgrids:
            #print grid
            prcpfile= open(r'../SWATInput/' + ftype + r'/' + forecastdate + '/' + grid.rstrip() + '.txt', 'r')
            #"D:\SWATInputs\20160301\p24.150_90.950.txt"
            prcpdata = prcpfile.readlines()
            for k in range(1, len(gridprcp)+1):
                gridprcp[k-1] = gridprcp[k-1] + float(prcpdata[k])
        for j in xrange(len(gridprcp)):
            gridprcp[j] = gridprcp[j]/count
    
        # Upstream FLow Data
        flowstations = [26, 25, 47, 68, 66, 57, 39, 49, 41, 34, 30, 38, 58, 76, 110, 119, 148, 187, 206, 217, 196]
        for station in flowstations:
            strcontent = strcontent + 'Boundary Location=                ,                ,        ,        ,                ,NERegion        ,                ,' + str(station) + '                              \nInterval=1DAY\n'
            stationfname = open('../SWATOutput/' +ftype + r'/' + forecastdate +'/' + str(station) + '.txt', 'r')
            stationdata = stationfname.readlines()
            strcontent = strcontent + 'Flow Hydrograph= ' + str(len(stationdata))
            for i in xrange(len(stationdata)/10+1):
                strcontent = strcontent + "\n"
                for j in xrange(10):
                    if i*10+j<len(stationdata):
                        flowval = float(stationdata[i*10+j].rstrip())
                        flowdata = "{0:.0f}".format(flowval)
                        flowdata = flowdata.rjust(8)
                        strcontent = strcontent + flowdata
            strcontent = strcontent + '\nStage Hydrograph TW Check=0\nFlow Hydrograph Slope= 0.05 \nDSS Path=\nUse DSS=False\nUse Fixed Start Time=True\n'
            strcontent = strcontent + 'Fixed Start Date/Time=02Jan2017,00:00\nIs Critical Boundary=False\nCritical Boundary Flow=\n'
        # Downstream Boundary WL data
#         bhairabBazarfile = open('BhairabBazar_WL.bnd', 'r')
#         wl = bhairabBazarfile.read()
#         strcontent = strcontent + wl + '\n'
    
        # Writing calculated precipitation data
    
        strcontent = strcontent + 'Boundary Location=                ,                ,        ,        ,                ,NERegion        ,                ,                                \n'
        strcontent= strcontent + 'Interval=1DAY\n'
        strcontent = strcontent + 'Precipitation Hydrograph= ' + str(len(gridprcp))
    
        for i in xrange(len(gridprcp)/10+1):
            strcontent = strcontent + "\n"
            for j in xrange(10):
                if i*10+j<len(gridprcp):
                    flowdata = "{0:.1f}".format(gridprcp[i*10+j])
                    flowdata = flowdata.rjust(8)
                    strcontent = strcontent + flowdata
        strcontent = strcontent + '\nStage Hydrograph TW Check=0\nFlow Hydrograph Slope= 0.05 \nDSS Path=\nUse DSS=False\nUse Fixed Start Time=True\n'
        strcontent = strcontent + 'Fixed Start Date/Time=02Jan2016,00:00\nIs Critical Boundary=False\nCritical Boundary Flow=\n'
    
        # Writing unsteady boundary data
        with open(unsteadyfname, 'w') as txt:
            txt.write(strcontent)


    def rasplangen(self, ftype='GFS'):
        forecastdate = self.forestartdate
        startdeltime = datetime.timedelta(days=-10)
        rstdeltime = datetime.timedelta(days=-7)

        rstdate = datetime.datetime.strftime(forecastdate+rstdeltime, '%d%b%Y')
        startdate = datetime.datetime.strftime(forecastdate+startdeltime, '%d%b%Y')
        enddate = datetime.datetime.strftime(self.foreenddate+datetime.timedelta(days=1), '%d%b%Y')
        
        plantemplate = 'unsteady2D.pSample'
        fcontent = open(plantemplate, 'r')
        lines = fcontent.readlines()
    #     print lines[0].rstrip()
        lines[0] = 'Plan Title=Plan_' + forecastdate.strftime("%Y%m%d") + '\n'
        print lines[0]
    #     print lines[2].rstrip()
        lines[2] = 'Short Identifier=' + forecastdate.strftime("%Y%m%d") + '\n'
    #     print lines[2]
    #     print lines[3].rstrip()
        lines[3] = 'Simulation Date=' + startdate + ',00:00,' + enddate + ',00:00' + '\n'
    #     print lines[3]
    #     print lines[5]
        lines[5] = 'Flow File=u01' + '\n' 
    #     print lines[5]
    
        lines[88] = 'IC Time=,' + rstdate + ',00:00' + '\n' 
    #     print lines[5]
    
        # Writing unsteady boundary data
        planfname = '../HecrasModel_' + ftype + '/unsteady2D.p01'
        with open(planfname, 'w') as txt:
            txt.write(''.join(lines))
        
    def rassimulation(self, ftype = 'GFS'):
        modelpath = r'D:/FFFEWS_Operational'
        simstartdate = self.forestartdate
        dates = []
        for i in xrange(61):
            dates.append(self.rasstartdate+datetime.timedelta(hours=6*i))
        
        strcontent = '\t<Layer Name="' + simstartdate.strftime("%Y%m%d") + '" Type="RASResults" Checked="True" Filename=".\Unsteady2D.p01.hdf">\n\t  <Layer Type="RASGeometry" Filename=".\Unsteady2D.p01.hdf" />'
        for findex in xrange(len(dates)):
            reqdate = dates[findex]
            if reqdate>=simstartdate:
                strcontent = strcontent + '\n' + '\t  <Layer Name="depth" Type="RASResultsMap" Filename=".\\' + simstartdate.strftime("%Y%m%d") + r'\Depth (' + reqdate.strftime("%d%b%Y %H").upper() + ' 00 00).vrt">\n\t\t<LabelFeatures Checked="True" rows="1" cols="1" r0c0="FID" Position="5" Color="-16777216" />\n\t\t<MapParameters MapType="depth" LayerName="Depth" OutputMode="Stored Current Terrain" StoredFilename=".\\' + simstartdate.strftime("%Y%m%d") + '\Depth (' + reqdate.strftime("%d%b%Y %H").upper() + ' 00 00).vrt" Terrain="Terrain" ProfileIndex="' + str(findex) + '" ProfileName="' + reqdate.strftime("%d%b%Y %H").upper() + ':00:00" ArrivalDepth="0" />\n\t  </Layer>'
        strcontent = strcontent + '\n' + '      <Layer Name="velocity" Type="RASResultsMap">\n        <MapParameters MapType="velocity" ProfileIndex="2147483647" ProfileName="Max" />\n      </Layer>\n      <Layer Name="elevation" Type="RASResultsMap" Checked="True">\n        <MapParameters MapType="elevation" ProfileIndex="2147483647" ProfileName="Max" />\n      </Layer>\n    </Layer>\n'
        samplefile = open("Unsteady2D.rasmapSample", 'r')
        samplecontent = samplefile.readlines()
        samplecontent[46] = strcontent
        with open(r'../HecrasModel_' + ftype + r'/Unsteady2D.rasmap', 'w') as txt:
            txt.write(''.join(samplecontent))
            
            
            
        import win32com.client
        hec = win32com.client.Dispatch("RAS505.HECRASController")
#         hec.showRas()
        rasproject = os.path.join(modelpath +  r"/HecrasModel_" + ftype + "/Unsteady2D.prj")
        hec.Project_Open(rasproject)
        NMsg,TabMsg,block = None,None,True
        hec.Compute_CurrentPlan(NMsg,TabMsg,block)
        hec.QuitRas()
        del hec
        
    def rasresults(self, ftype='GFS'):
        todaytime = datetime.datetime.combine(self.todaydate, datetime.time(0,0))
        locationfile = open('Station_Grids.txt', 'r')
        self.stationcells = {}
        lines = csv.DictReader(locationfile, delimiter = '\t')
        for row in lines:
            print row['Station']
            self.stationcells[row['Station']] = int(row['250m'])
        if os.path.exists(r'../HecrasOutput/WaterLevel/' + ftype + r'/' + self.forestartdate.strftime("%Y%m%d")) == False:
            os.makedirs(r'../HecrasOutput/WaterLevel/' + ftype + r'/' + self.forestartdate.strftime("%Y%m%d"))
        if os.path.exists(r'../FinalOutputs/WaterLevel/' + ftype + r'/' + self.forestartdate.strftime("%Y%m%d")) == False:
            os.makedirs(r'../FinalOutputs/WaterLevel/' + ftype + r'/' + self.forestartdate.strftime("%Y%m%d"))
    
        datefile = open(r"../HecrasModel_" + ftype + "/Unsteady2D.p01.blf", 'r')
        datesx = datefile.readlines()[0].split(' ')[4:-11]
        print datesx
        dates = []
        for i in xrange(len(datesx)):
            if len(datesx[i])>9:
                indate = datetime.datetime.strptime(datesx[i],"%H%M%d%b%Y")
                hrs = datesx[i][:2]
                if hrs == '18':
                    indate = indate + datetime.timedelta(days=-1)
                dates.append(indate)
            else:
                indate = datetime.datetime.strptime(datesx[i],"%d%b%Y") 
                dates.append(indate)
       
        x = h5py.File(r"../HecrasModel_" + ftype + r"/Unsteady2D.p01.hdf", 'r')
        ppp = x['Results']['Unsteady']['Output']['Output Blocks']['Base Output']['Unsteady Time Series']['2D Flow Areas']['NERegion']['Water Surface']
#         print dates
        xxx = zip(*ppp)
        for station in self.stationcells:
            index = self.stationcells[station]
            xdata = xxx[index]
            print station, index, len(dates), len(xdata)
            
            with open(r'../HecrasOutput/WaterLevel/' + ftype + r'/' + self.forestartdate.strftime("%Y%m%d") + r"/" + station.lower() +'.txt', 'w') as txt:
                for j in xrange(len(xdata)):
                    if dates[j]>=self.visstartdate:
                        if dates[j]+datetime.timedelta(hours=6)<todaytime:
                            txt.write((dates[j]+datetime.timedelta(hours=6)).strftime("%Y-%m-%dT%H:%M:%S") + ',' + "{0:.2f}".format(xdata[j]) + ",," + '\n')
                        elif dates[j]+datetime.timedelta(hours=6)==todaytime:
                            txt.write((dates[j]+datetime.timedelta(hours=6)).strftime("%Y-%m-%dT%H:%M:%S") + ',' + "{0:.2f}".format(xdata[j]) + "," + "{0:.2f}".format(xdata[j]) + '\n')
                        else:
                            txt.write((dates[j]+datetime.timedelta(hours=6)).strftime("%Y-%m-%dT%H:%M:%S") + ',,' + "{0:.2f}".format(xdata[j]) + '\n')
    
            
            
            
            # Correction using in-situ WL
            
            bias = 0.0
            insitudates = []
            insituwls = []
            self.conn.text_factory = str
            c = self.conn.cursor()
            try:
                c.execute("Select Date, WL from Waterlevel WHERE Station = ? and Date>=? ORDER by Date DESC", (station,self.visstartdate))
                print(len(c.fetchall()))
                if len(c.fetchall()) == 0:
                    insitudates.append(self.forestartdate)
                    insituwls.append(100.0)
                else:
                    for row in c.fetchall():
                        insitudates.append(datetime.datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S"))
                        insituwls.append(float(row[1]))
            except:
                insitudates.append(self.forestartdate)
                insituwls.append(100.0)
            print len(insitudates), len(insituwls)
            for x in xrange(len(dates)):
                if dates[x] == insitudates[0]:
                        if insituwls[0]!=100.0:
                            bias = xdata[x] - insituwls[0]
                        else:
                            bias = 0.0
                        print bias, dates[x]
                else:
                    bias = 0.0
                    
            
            with open(r'../FinalOutputs/WaterLevel/' + ftype + r'/' + self.forestartdate.strftime("%Y%m%d") + r"/" + station.lower() +'.txt', 'w') as txt:
                for j in xrange(len(xdata)):
                    if dates[j]>=self.visstartdate:
                        if dates[j]+datetime.timedelta(hours=6)<todaytime:
                            txt.write((dates[j]+datetime.timedelta(hours=6)).strftime("%Y-%m-%dT%H:%M:%S") + ',' + "{0:.2f}".format(xdata[j]-bias) + ",," + '\n')
                        elif dates[j]+datetime.timedelta(hours=6)==todaytime:
                            txt.write((dates[j]+datetime.timedelta(hours=6)).strftime("%Y-%m-%dT%H:%M:%S") + ',' + "{0:.2f}".format(xdata[j]-bias) + "," + "{0:.2f}".format(xdata[j]-bias) + '\n')
                        else:
                            txt.write((dates[j]+datetime.timedelta(hours=6)).strftime("%Y-%m-%dT%H:%M:%S") + ',,' + "{0:.2f}".format(xdata[j]-bias) + '\n')
    
    def pullobsdata(self):
        locationfile = open('Station_Grids.txt', 'r')
        self.stationcells = {}
        mindate = self.visstartdate
        lines = csv.DictReader(locationfile, delimiter = '\t')
        for row in lines:
            self.stationcells[row['Station']] = int(row['250m'])
            
        for station in self.stationcells:
            dates = []
            wls = []
            print station
            self.conn.text_factory = str
            c = self.conn.cursor()
            c.execute("Select Date, WL from Waterlevel WHERE Station = ? and Date>=? ORDER by Date DESC", (station,mindate))
            for row in c.fetchall():
                print row[0]
                dates.append(datetime.datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S"))
                wls.append(float(row[1]))

            if dates[0] >= self.forestartdate:
                print "sth"
    
    def mappreparation(self):
        strdate = self.forestartdate.strftime("%Y%m%d")
#         todayyr = self.forestartdate.strftime("%Y")
#         todaymonth = self.forestartdate.strftime("%m")
#         todayday = self.forestartdate.strftime("%d")
    
#         time = '00'

        if os.path.exists(r'../FinalOutputs/ECMWFPrecipitation/' + strdate) == False:
            os.makedirs(r'../FinalOutputs/ECMWFPrecipitation/' + strdate)
        if os.path.exists(r'../FinalOutputs/GFSPrecipitation/' + strdate) == False:
            os.makedirs(r'../FinalOutputs/GFSPrecipitation/' + strdate)
        if os.path.exists(r'../FinalOutputs/FloodDepth/GFS/' + strdate) == False:
            os.makedirs(r'../FinalOutputs/FloodDepth/GFS/' + strdate)
        if os.path.exists(r'../FinalOutputs/FloodDepth/ECMWF/' + strdate) == False:
            os.makedirs(r'../FinalOutputs/FloodDepth/ECMWF/' + strdate)

        if os.path.exists(r'../HecrasOutput/WaterSurface/GFS/' + self.forestartdate.strftime("%Y%m%d")) == False:
            os.makedirs(r'../HecrasOutput/WaterSurface/GFS/' + self.forestartdate.strftime("%Y%m%d"))
        if os.path.exists(r'../HecrasOutput/WaterSurface/ECMWF/' + self.forestartdate.strftime("%Y%m%d")) == False:
            os.makedirs(r'../HecrasOutput/WaterSurface/ECMWF/' + self.forestartdate.strftime("%Y%m%d"))
    
        # ECMWFMap Preparation
        for forecasthr in range(6, (self.noforedays+1)*24+1, 6):
            os.system('C:\OSGeo4W64\OSGeo4W.bat gdal_translate -of GTiff ../Precipitation/ECMWF/meghna.precip.ecmwf.' + strdate + '.f' + str(forecasthr).zfill(3) + '.asc ../FinalOutputs/ECMWFPrecipitation/meghna.precip.ecmwf.' + strdate + '.f' + str(forecasthr).zfill(3) + '.tif')
            os.system('C:\OSGeo4W64\OSGeo4W.bat gdalwarp -overwrite -s_srs EPSG:4326 -t_srs EPSG:3857 ../FinalOutputs/ECMWFPrecipitation/meghna.precip.ecmwf.' + strdate + '.f'+ str(forecasthr).zfill(3) +'.tif ../FinalOutputs/ECMWFPrecipitation/W' + strdate + '.f' + str(forecasthr).zfill(3) + '.tif')
            os.system('C:\OSGeo4W64\OSGeo4W.bat gdaldem color-relief ../FinalOutputs/ECMWFPrecipitation/W' + strdate + '.f' + str(forecasthr).zfill(3) + '.tif precipitation.txt -alpha ../FinalOutputs/ECMWFPrecipitation/C' + strdate + '.f' + str(forecasthr).zfill(3) + '.tif')
            os.system('C:\OSGeo4W64\OSGeo4W.bat gdal_translate -of PNG ../FinalOutputs/ECMWFPrecipitation/C' + strdate + '.f' + str(forecasthr).zfill(3) + '.tif ../FinalOutputs/ECMWFPrecipitation/' + strdate + r'/f' + str(forecasthr).zfill(3) + '.PNG')
        
        # GFSMap Preparation
        for forecasthr in range(6, (self.noforedays+1)*24+1, 6):
            os.system('C:\OSGeo4W64\OSGeo4W.bat gdalwarp -overwrite -s_srs EPSG:4326 -t_srs EPSG:3857 ../Precipitation/GFS/meghna.precip.gfs.' + strdate + '.f'+ str(forecasthr).zfill(3) +'.tif ../FinalOutputs/GFSPrecipitation/W' + strdate + '.f' + str(forecasthr).zfill(3) + '.tif')
            os.system('C:\OSGeo4W64\OSGeo4W.bat gdaldem color-relief ../FinalOutputs/GFSPrecipitation/W' + strdate + '.f' + str(forecasthr).zfill(3) + '.tif precipitation.txt -alpha ../FinalOutputs/GFSPrecipitation/C' + strdate + '.f' + str(forecasthr).zfill(3) + '.tif')
            os.system('C:\OSGeo4W64\OSGeo4W.bat gdal_translate -of PNG ../FinalOutputs/GFSPrecipitation/C' + strdate + '.f' + str(forecasthr).zfill(3) + '.tif ../FinalOutputs/GFSPrecipitation/' + strdate + r'/f' + str(forecasthr).zfill(3) + '.PNG')
        
        # HECRAS Results copy
        for ftype in ['GFS', 'ECMWF']:
            for fn in os.listdir('../HecrasModel_'+ ftype +r'/' + strdate + r'/'):
                if '.tif' in fn:
                    print fn[7:25]
                    filedate = datetime.datetime.strptime(fn[7:25], "%d%b%Y %H %M %S")
                    shutil.copy('../HecrasModel_'+ ftype +r'/' + strdate + r'/' + fn, r'../HecrasOutput/WaterSurface/' + ftype + r'/' + strdate + r'/' + filedate.strftime("%Y%m%d%H") + '.tif')
        
        # HecRAS Flodo Map preparation
        for ftype in ['GFS', 'ECMWF']:
            for forecasthr in range(6, (self.noforedays+1)*24+1, 6):
                reqdate = self.forestartdate + datetime.timedelta(hours = forecasthr)
                os.system('C:\OSGeo4W64\OSGeo4W.bat gdalwarp -overwrite -te 184115.0 2641392.0 449746.0 2802020.0 -tr 30.0 30.0 ' + '../HecrasOutput/WaterSurface/'+ ftype + r'/' + strdate + r'/' + reqdate.strftime("%Y%m%d%H") + '.tif' +  r' ../FinalOutputs/FloodDepth/' + ftype + r'/' + 'f' + str(forecasthr).zfill(3) + '.tif')
                os.system('C:\OSGeo4W64\OSGeo4W.bat gdalwarp -overwrite -s_srs EPSG:32646 -t_srs EPSG:3857 ../FinalOutputs/FloodDepth/' + ftype + r'/' + r'f' + str(forecasthr).zfill(3) + '.tif ../FinalOutputs/FloodDepth/' + ftype + r'/W' + 'f' + str(forecasthr).zfill(3) + '.tif')
                os.system('C:\OSGeo4W64\OSGeo4W.bat gdaldem color-relief ../FinalOutputs/FloodDepth/' + ftype + r'/W' + 'f' + str(forecasthr).zfill(3) + '.tif waterlevel.txt -alpha ../FinalOutputs/FloodDepth/' + ftype + r'/C' + 'f' + str(forecasthr).zfill(3) + '.tif')
                os.system('C:\OSGeo4W64\OSGeo4W.bat gdal_translate -of PNG ../FinalOutputs/FloodDepth/' + ftype + r'/C' + 'f' + str(forecasthr).zfill(3) + '.tif ../FinalOutputs/FloodDepth/' + ftype + r'/' + strdate + r'/f' + str(forecasthr).zfill(3) + '.PNG')
                        
    def pushresults(self):
        strdate = self.forestartdate.strftime("%Y%m%d")
#        ssh = paramiko.SSHClient()
#        ssh.load_system_host_keys()
#        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#        ssh.connect(hostname='ovid.u.washington.edu',port='22',username='saswe',password='Bangla_Power21Feb')

        ssh = self.createSSHClient('ovid.u.washington.edu', 22, 'saswe', 'Bangla_Power21Feb')
        scp = SCPClient(ssh.get_transport(),  socket_timeout=15.0)
                
        for ftype in ['GFS', 'ECMWF']:
            for forecasthr in range(6, (self.noforedays+1)*24+1, 6):
                # Flood Maps
                filepath = '../FinalOutputs/FloodDepth/' + ftype + r'/' + strdate + r'/f' + str(forecasthr).zfill(3) + '.PNG'
                serverpath = 'public_html/flashflood/data/floodmap/' + ftype.lower() + r'/f' + str(forecasthr).zfill(3) + '.PNG'
                try:
                    scp.put(filepath, serverpath)
                    print  "Success in uplodaing file: " + filepath
                    scp.close()
                except:
                    print  "Error in uplodaing file: " + filepath
                    continue

                # Precipitation Maps
                filepath = '../FinalOutputs/' + ftype + r'Precipitation/' + strdate + r'/f' + str(forecasthr).zfill(3) + '.PNG'
                serverpath = 'public_html/flashflood/data/' + ftype.lower() + r'precipitation/f' + str(forecasthr).zfill(3) + '.PNG'
                try:
                    scp.put(filepath, serverpath)
                    print  "Success in uplodaing file: " + filepath
                except:
                    print  "Error in uplodaing file: " + filepath
                    continue


                # Forecasted Boundary Inflow
                for fn in os.listdir('../FinalOutputs/Inflow/' + ftype + r'/' + strdate + r'/'):
                    filepath = '../FinalOutputs/Inflow/' + ftype + r'/' + strdate + r'/' + fn
                    serverpath = 'public_html/flashflood/data/inflow/' + ftype.lower() + r'/' + fn
                    try:    
                        scp.put(filepath, serverpath)
                        print  "Success in uplodaing file: " + filepath
    
                    except:
                        print  "Error in uplodaing file: " + filepath
                        continue

                # Forecasted WL Timeseries
            for fn in os.listdir('../FinalOutputs/WaterLevel/' + ftype + r'/' + strdate + r'/'):
                filepath = '../FinalOutputs/WaterLevel/' + ftype + r'/' + strdate + r'/' + fn
                serverpath = 'public_html/flashflood/data/station/' + ftype.lower() + r'/' + fn
                try:
                    scp.put(filepath, serverpath)
                    print  "Success in uplodaing file: " + filepath
                except:
                    print  "Error in uplodaing file: " + filepath
                    continue
  
    def createSSHClient(self, server, port, user, password):
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(server, port, user, password)
        return client

      
        
if __name__ == '__main__':
    forecast = FFFEWSSystem()
    forecast.ffwcobsdata()
    forecast.imergprecip()
 ##    forecast.updateimerg()
    forecast.gfsforecastprecip()
    forecast.ecmwfforecastprecip()
    for ftype in ['GFS', 'ECMWF']:
        forecast.dailyprcpcalc(ftype)
    forecast.swatforcing('IMERG')
    for ftype in ['GFS','ECMWF']:
        forecast.swatprecipprep(ftype)
        forecast.swatsimulation(ftype)
        forecast.swatoutputprocessor(ftype)
        forecast.rasbndgen(ftype)
        forecast.rasplangen(ftype)
        forecast.rassimulation(ftype)
        forecast.rasresults(ftype)
    forecast.mappreparation()
    forecast.pushresults()
