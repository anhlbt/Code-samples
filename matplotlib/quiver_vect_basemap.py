""" Quiver plot demo with basemap. Extracted from http://matplotlib.github.com/basemap/users/examples.html

"""
import numpy as np
import matplotlib.pyplot as plt
import datetime
from mpl_toolkits.basemap import Basemap, shiftgrid, addcyclic
from netCDF4 import Dataset, date2index

# specify date to plot.
date = datetime.datetime(1993,3,14,0)
# set OpenDAP server URL.
URL="http://nomad1.ncep.noaa.gov:9090/dods/reanalyses/reanalysis-2/6hr/pgb/pgb"
data = Dataset(URL)
# read lats,lons,times.
latitudes = data.variables['lat'][:]
longitudes = data.variables['lon'][:].tolist()
times = data.variables['time']
# get time index for desired date.
ntime = date2index(date,times,calendar='standard')
# get sea level pressure and 10-m wind data.
slpdata = data.variables['presmsl']
udata = data.variables['ugrdprs']
vdata = data.variables['vgrdprs']
# mult slp by 0.01 to put in units of hPa.
slpin = 0.01*slpdata[ntime,:,:]
uin = udata[ntime,0,:,:] 
vin = vdata[ntime,0,:,:] 

# add cyclic points manually (could use addcyclic function)
slp = np.zeros((slpin.shape[0],slpin.shape[1]+1),np.float)
slp[:,0:-1] = slpin; slp[:,-1] = slpin[:,0]
u = np.zeros((uin.shape[0],uin.shape[1]+1),np.float64)
u[:,0:-1] = uin; u[:,-1] = uin[:,0]
v = np.zeros((vin.shape[0],vin.shape[1]+1),np.float64)
v[:,0:-1] = vin; v[:,-1] = vin[:,0]
longitudes.append(360.); longitudes = np.array(longitudes)

# make 2-d grid of lons, lats
lons, lats = np.meshgrid(longitudes,latitudes)
# make orthographic basemap.
m = Basemap(resolution='c',projection='ortho',lat_0=60.,lon_0=-60.)
# create figure, add axes
fig1 = plt.figure(figsize=(8,10))
ax = fig1.add_axes([0.1,0.1,0.8,0.8])
# set desired contour levels.
clevs = np.arange(960,1061,5)
# compute native x,y coordinates of grid.
x, y = m(lons, lats)
# define parallels and meridians to draw.
parallels = np.arange(-80.,90,20.)
meridians = np.arange(0.,360.,20.)
# plot SLP contours.
CS1 = m.contour(x,y,slp,clevs,linewidths=0.5,colors='k',animated=True)
CS2 = m.contourf(x,y,slp,clevs,cmap=plt.cm.RdBu_r,animated=True)
# plot wind vectors on projection grid.
# first, shift grid so it goes from -180 to 180 (instead of 0 to 360
# in longitude).  Otherwise, interpolation is messed up.
ugrid,newlons = shiftgrid(180.,u,longitudes,start=False)
vgrid,newlons = shiftgrid(180.,v,longitudes,start=False)
# transform vectors to projection grid.
uproj,vproj,xx,yy = \
m.transform_vector(ugrid,vgrid,newlons,latitudes,31,31,returnxy=True,masked=True)
# now plot.
Q = m.quiver(xx,yy,uproj,vproj,scale=700)
# make quiver key.
qk = plt.quiverkey(Q, 0.1, 0.1, 20, '20 m/s', labelpos='W')
# draw coastlines, parallels, meridians.
m.drawcoastlines(linewidth=1.5)
m.drawparallels(parallels)
m.drawmeridians(meridians)
# add colorbar
cb = m.colorbar(CS2,"bottom", size="5%", pad="2%")
cb.set_label('hPa')
# set plot title
ax.set_title('SLP and Wind Vectors '+str(date))

plt.show()