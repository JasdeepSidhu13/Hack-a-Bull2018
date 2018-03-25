# -*- coding: utf-8 -*-
"""
Created on Sun Mar 25 10:14:50 2018

@author: Jasdeep
"""

#!/usr/bin/env python

import urllib.request as request
import json
import io
import csv
from datetime import datetime

#Modify these values to change the min/max magnitudes for search.
MINMAG = 4.5
MAXMAG = 5.5
#Modify these values to change start/end dates for search.
STARTDATE = '2018-01-01'
ENDDATE = '2018-03-25'
#The API for this URL query is described here:
#http://earthquake.usgs.gov/fdsnws/event/1/
#More parameters are available there, including lat/lon bounds.

if __name__ == '__main__':
    url = 'http://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=[START]&endtime=[END]&minmag=[MIN]&maxmag=[MAX]&producttype=dyfi&orderby=time-asc'
    url = url.replace('[START]',STARTDATE)
    url = url.replace('[END]',ENDDATE)
    url = url.replace('[MIN]',str(MINMAG))
    url = url.replace('[MAX]',str(MAXMAG))
    print(url)
    fh = request.urlopen(url)
    data = fh.read().decode('utf8')
    fh.close()
    jdict = json.loads(data)
    f = open('cdi_results.csv','wt')
    f.write('Event ID, Time, Lat,Lon,Depth,Magnitude,Max CDI, Max CDI Distance\n')
    for event in jdict['features']:
        eid = event['id']
        lon,lat,depth = event['geometry']['coordinates']
        mag = event['properties']['mag']
        etime = datetime.utcfromtimestamp(event['properties']['time']/1000)
        durl = event['properties']['detail']
        fh = request.urlopen(durl)
        data = fh.read().decode('utf8')
        fh.close()
        jdict2 = json.loads(data)
        if 'cdi_geo.txt' not in jdict2['properties']['products']['dyfi'][0]['contents']:
            continue
        txturl = jdict2['properties']['products']['dyfi'][0]['contents']['cdi_geo.txt']['url']
        fh = request.urlopen(txturl)
        data = fh.read().decode('utf8')
        fh.close()
        f = io.StringIO(data)
        reader = csv.reader(f)
        headers = next(reader)
        cdi = []
        dist = []
        for line in reader:
            cdi.append(float(line[1]))
            dist.append(float(line[3]))
        if not len(cdi):
            continue
        maxcdi = max(cdi)
        imax = cdi.index(maxcdi)
        maxdist = dist[imax]
        tstr = etime.strftime('%Y-%m-%d %H:%M:%S')
        print(tstr,mag,maxcdi,maxdist)
        tpl = (eid,tstr,lat,lon,depth,mag,maxcdi,maxdist)
        f.write('%s,%s,%.4f,%.4f,%.2f,%.1f,%.1f,%.1f\n' % tpl)
