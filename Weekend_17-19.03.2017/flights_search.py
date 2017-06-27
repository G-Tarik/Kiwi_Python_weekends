#!/usr/bin/python3

from datetime import datetime as dt
from datetime import timedelta
from pytz import timezone as tz
import pytz
from operator import itemgetter
from itertools import chain

class AirPort:
    def __init__(self, port_id, country_id,timezone):
        self.code = port_id
        self.country = country_id
        self.tzone = timezone
        self.dstntions = []
    def add_destination(self, *args):
        arr_port, dep_time, arr_time = args
        dep_zone = tz(self.tzone)
        arr_zone = tz(airports[arr_port].tzone)
        dep_time = dep_zone.localize(dt.strptime(dep_time, "%Y-%m-%d %H:%M:%S"))
        arr_time = arr_zone.localize(dt.strptime(arr_time, "%Y-%m-%d %H:%M:%S"))
        self.dstntions.append((arr_port,dep_time,arr_time))


####################################################      
airports = {}      
with open('iata_codes.csv','r') as iatafile:
    for line in iatafile:
        ia_country, ia_port, ia_timezone = line.rstrip().split(',')
        airports[ia_port]=AirPort(ia_port,ia_country,ia_timezone)
  
# parse input data   
with open('input_data.csv','r') as datafile:
    for line in datafile:
        dep_port, arr_port, dep_time, arr_time = line.rstrip().split(';')
        #cut off destination in the same country
        if airports[dep_port].country != airports[arr_port].country:
            airports[dep_port].add_destination(arr_port,dep_time,arr_time)
####################################################

def date_to_string(ptimes):
    t_fmt='%Y-%m-%dT%H:%M:%S'
    return [(t[0].strftime(t_fmt), t[1].strftime(t_fmt)) for t in ptimes]
 
def checktime(nxt,pathtime):
    if not pathtime or  (nxt[1]>pathtime[-1][1] and nxt[2]-pathtime[0][0]<path_maxlen):
        return True,nxt[1:]
    return False, None
    

def enumpaths(k,c,visitedcntrs=[],path=[],pathtime=[]):
    if len(pathlist)>40*c:
        raise ValueError('Limit of 40 paths is reached, choosing next start port..')
    palen = len(path)
    if not visitedcntrs: 
        visitedcntrs=[airports[k].country]
    if palen>9:
        pathlist.append(path)
        timelist.append(date_to_string(pathtime))
    else:
        for nxt in airports[k].dstntions:
            cun = airports[nxt[0]].country
            t_ok, t_tup = checktime(nxt,pathtime)
            if t_ok and ((palen==9 and cun==visitedcntrs[0]) or (palen<9 and cun not in visitedcntrs)):
                enumpaths(nxt[0],c,visitedcntrs+[cun],path+[(visitedcntrs[-1],k,nxt[0])],pathtime+[t_tup])

def formatresults():
    rez=[list(zip(pathlist[i],timelist[i])) for i in range(len(pathlist))]
    rez=[[str(i)]+list(chain.from_iterable(y)) for i,x in enumerate(rez) for y in x]
    return rez
    
def export_res(rez):
    with open('results_10.csv','a') as rzf:
        for line in rez:
            rzf.write(';'.join(line)+'\n')

            
pathlist, timelist = [], []
path_maxlen=timedelta(365) 
c=0
for port in airports: 
    c += 1
    try:
        enumpaths(port,c)
    except ValueError as e:
        print(port,e)
    if c>40:
        break

rez=formatresults()
export_res(rez)
