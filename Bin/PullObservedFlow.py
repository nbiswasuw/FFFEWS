from bs4 import BeautifulSoup
import urllib2
import datetime

now = datetime.datetime.now()
fdate=now-datetime.timedelta(days=1)

#Ganges
htmlG = urllib2.urlopen('http://www.ffwc.gov.bd/ffwc_charts/index.php?stid=43').read()  #Ganges
for x in htmlG.split('{'):
    if "name: 'Observed Water Level'" in x:
        observddata = x.replace('[Date.UTC(', '').replace(')', '').replace("\n                name: 'Observed Water Level',\n                data: [",'').replace('\n            }, ', '').replace(' ', '')
        for y in observddata.split(']'):
            print y
    elif "name: 'Forecast Water Level'" in x:
        print x.replace('[Date.UTC(', '').replace(')', '').replace(']', '').replace("\n                name: 'Forecast Water Level',\n                data: [",'').replace('\n            }, ', '').replace(' ', '')
