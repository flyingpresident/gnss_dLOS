import geomtools
import numpy as np
import pandas as pd

print("year, station code1(static), station code2")

year, static, station = input().split()

sfile = "./{}.{}.pos".format(static, year[2:])
file = "./{}.{}.pos".format(station, year[2:])
EPSG = 32655

xy_s = []
xy = []
date = []
height_s= []
height = []

flen = sum([1 for _ in open(sfile)]) # 383

with open(sfile) as f:
    ll = []
    for i, l in enumerate(f):
        # if year == "2018":
        #     max = 364
        # else:
        #     max = 361

        if i >= 20 and i < flen-2:
            date.append("".join(l.rstrip().split()[:3]))
            lat = float(l.rstrip().split()[7])
            lon = float(l.rstrip().split()[8])
            height_s.append(float(l.rstrip().split()[9]))
            ll.append((lon, lat))
    xy_s = geomtools.ll2UTM(ll, EPSG)
# station
with open(file) as f:
    ll = []
    for i, l in enumerate(f):
        if i >= 20 and i < flen-2:
            lat = float(l.rstrip().split()[7])
            lon = float(l.rstrip().split()[8])
            height.append(float(l.rstrip().split()[9]))
            ll.append((lon, lat))
    xy = geomtools.ll2UTM(ll, EPSG)

# relative
rxy = (xy-xy_s).tolist()
rheight = [str(h - h_s) for (h, h_s) in zip(height, height_s)]

with open("./{}_{}.{}.csv".format(static, station, year[2:]), mode='w') as f:
    f.write("date,x[km],y[km],z[m]\n")
    for t, xy_, h in zip(date, rxy, rheight):
        xx = str(xy_[0])
        yy = str(xy_[1])
        f.writelines([",".join([t, xx, yy, h]), "\n"])

print("Completed")
