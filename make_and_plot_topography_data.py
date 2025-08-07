##########################################
# Function to create a blue-red color map
##########################################

def makecmap_bluered(nneg, npos):
    import numpy as np
    from matplotlib import colormaps
    from matplotlib.colors import ListedColormap
    cblue=colormaps['Blues']
    cred=colormaps['Reds']
    #newcolours=np.vstack((cblue(np.linspace(1,0,nneg)),cred(np.linspace(0,1,npos))))
    newcolours=np.vstack((cblue(np.linspace(0.8,0.2,nneg)),cred(np.linspace(0.1,0.8,npos))))
    my_bluered=ListedColormap(newcolours)
    return my_bluered


###############
# MAIN PROGRAM
###############

import os
import numpy as np
#import pandas as pd
import xarray as xr
import rioxarray as rxr
import geopandas
from shapely.geometry import box
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from convertbng.util import convert_bng
import cartopy.crs as ccrs


plt.ion()

# Read UK map for plotting and change map coordinates to lon-lat (so you can overplot on topography)
inmapfile = 'C://Users//m1013956D//OneDrive - Defra//Python//read_SSSI_GeoJSON_Oct2023//ukmap_ukcp18.geojson'
ukmap = geopandas.read_file(inmapfile)
ukmap = ukmap.set_crs("EPSG:27700", allow_override=True)
ukmap = ukmap.to_crs("EPSG:4326")

'''
# Input topography data files
indatadir = 'C://Users//m1013956D//OneDrive - Defra//Python//test_exe_estuary//data//lidar_topography//'
infiles = os.listdir(indatadir)

# Read input data files
indata = [rxr.open_rasterio(indatadir+ifile, masked=True) for ifile in infiles]
fld = xr.combine_by_coords(indata, combine_attrs="override")

# Convert coordinates to lon-lat degrees
fld = fld.rio.reproject("EPSG:4326")

# Save topography data in netcdf file
fld.to_netcdf(indatadir[:-18] + "topography.nc")
'''

# Read from saved netcdf
indatadir = 'C://Users//m1013956D//OneDrive - Defra//Python//test_exe_estuary//data//'
fld = xr.open_dataset(indatadir + "topography.nc")

# Give an intuitive name to the data
fld = fld.rename({"__xarray_dataarray_variable__": "elevation"})

# Clip UK map to include only the Exe estuary area
bbox = box(fld.x.min(), fld.y.min(), fld.x.max(), fld.y.max())
ukmap = ukmap.clip(bbox)

# Plotting
mycmap = makecmap_bluered(20, 260)

fig = plt.figure()
ax = plt.subplot2grid((1,1), (0,0), projection=ccrs.PlateCarree())
#ax.set_axis_off()
plt.pcolormesh(fld.x, fld.y, fld.elevation[0],  vmin = -20, vmax = 260, cmap=mycmap)

ukmap.boundary.plot(ax=ax, aspect=1, facecolor='none', edgecolor='black', linewidth=0.5)

ax.set_title('Exe Estuary Topography')
plt.colorbar(orientation='vertical', fraction=0.05)

#plt.savefig('plot_topography_exe.png')

