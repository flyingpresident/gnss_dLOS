import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

i = 36.12 # incident angle
a = 190.24 # azimth angle

static, station = input().split()

# static = "93037"
# station = "02P107"

df = pd.read_csv('./pos_csv/{}_{}.csv'.format(static, station))
df[df.keys()[1]] = pd.to_datetime(df[df.keys()[1]], format='%Y%m%d')
x = df[df.keys()[2]]*1000 # m
y = df[df.keys()[3]]*1000 # m
h = df[df.keys()[4]] # m
df["dlos[m]"] = (np.cos(a)*np.sin(i)*x - np.sin(a)*np.sin(i)*y - np.cos(i)*h) # m
df.to_csv("./LOS_{}_{}.csv".format(static, station), index=False)
cr = df["dlos[m]"][0]
fig = plt.figure(figsize=(8,3))
ax = fig.add_subplot(1, 1, 1)

# cr = -7668.9438580 #m
ax.text(-0.05, 1.05, "cm    {}→{} LOS displacement".format(static, station), ha='left', transform=ax.transAxes)
ax.text(1.0, 1.05, "standard value: {}m".format(round(cr, 3)), ha='right', transform=ax.transAxes)
plt.ylim(-5., 5.)
plt.plot(df[df.keys()[1]], (df["dlos[m]"]-cr)*100, marker='.', ls='') # cm
plt.grid(True)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%m/%d"))
plt.gcf().autofmt_xdate()
fig.savefig("./LOS_{}_{}.png".format(static, station))
