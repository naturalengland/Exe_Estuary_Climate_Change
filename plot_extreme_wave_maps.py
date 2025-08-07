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

import numpy as np
#import pandas as pd
import geopandas
from shapely.geometry import box
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from convertbng.util import convert_bng

plt.ion()

# Select RCP scenario
#myrcp = 'rcp45'
myrcp = 'rcp85'

# Select return level (e.g. t100 denotes 1-in-100 years extremes)
#rlev = 't1'
#rlev = 't2'
#rlev = 't5'
#rlev = 't10'
#rlev = 't20'
#rlev = 't25'
#rlev = 't50'
#rlev = 't75'
rlev = 't100'
#rlev = 't150'
#rlev = 't200'
#rlev = 't250'
#rlev = 't300'
#rlev = 't500'
#rlev = 't1000'
#rlev = 't10000'

# Exe estuary area coordinates (W,S,E,N)
exe_lonlat = [-3.524754, 50.549227, -3.254053, 50.745831]
exe_bng = [convert_bng(exe_lonlat[0], exe_lonlat[1])[0][0], \
           convert_bng(exe_lonlat[0], exe_lonlat[1])[1][0], \
           convert_bng(exe_lonlat[2], exe_lonlat[3])[0][0], \
           convert_bng(exe_lonlat[2], exe_lonlat[3])[1][0]]

# Read Exe Estuary map for plotting
inmapfile = 'C://Users//m1013956D//OneDrive - Defra//Python//read_SSSI_GeoJSON_Oct2023//Regions_in_England.geojson'
exemap = geopandas.read_file(inmapfile)

# Extreme sea level data
indir = 'C:\\Users\\m1013956D\\OneDrive - Defra\\Python\\test_exe_estuary\\data\\'
infile = []
for idec in 2020+10*np.arange(9):
    infile.append(indir + 'esl_shp_'+myrcp+'_future_'+str(idec) + \
    '\\extremeSeaLevel_marine-sim_return-periods-shp_' + myrcp + \
    '_future_' + str(idec) + '.shp')

# Read extreme sea level data for each decade
esl2020 = geopandas.read_file(infile[0])
esl2030 = geopandas.read_file(infile[1])
esl2040 = geopandas.read_file(infile[2])
esl2050 = geopandas.read_file(infile[3])
esl2060 = geopandas.read_file(infile[4])
esl2070 = geopandas.read_file(infile[5])
esl2080 = geopandas.read_file(infile[6])
esl2090 = geopandas.read_file(infile[7])
esl2100 = geopandas.read_file(infile[8])

# Extract Exe estuary area
esl_exe2020 = esl2020[esl2020.intersects(box(*exe_bng))]
esl_exe2030 = esl2030[esl2030.intersects(box(*exe_bng))]
esl_exe2040 = esl2040[esl2040.intersects(box(*exe_bng))]
esl_exe2050 = esl2050[esl2050.intersects(box(*exe_bng))]
esl_exe2060 = esl2060[esl2060.intersects(box(*exe_bng))]
esl_exe2070 = esl2070[esl2070.intersects(box(*exe_bng))]
esl_exe2080 = esl2080[esl2080.intersects(box(*exe_bng))]
esl_exe2090 = esl2090[esl2090.intersects(box(*exe_bng))]
esl_exe2100 = esl2100[esl2100.intersects(box(*exe_bng))]

# List with all the data
exedata = [esl_exe2020, esl_exe2030, esl_exe2040, \
           esl_exe2050, esl_exe2060, esl_exe2070, \
           esl_exe2080, esl_exe2090, esl_exe2100]

###################
# PLOT EXE ESTUARY
###################

fig = plt.figure(figsize=[1.0*6.4, 1.6*4.8])
plt.subplots_adjust(bottom=0.065, top=0.92, left=0.05, right=0.95, wspace=0.2, hspace=0.3)
mycmap = makecmap_bluered(50,50)
mynorm=mcolors.Normalize(vmin=esl_exe2020[rlev].min(), vmax=esl_exe2100[rlev].max())

# Loop over decades and plot the map for each decade (3x3 panels)
for ix in range(3):
    for iy in range(3):
        ax = plt.subplot2grid((3,3), (ix,iy))
        idecade = ix*3+iy                    
        # Plot map
        exedata[idecade].plot(ax = ax, column=rlev, norm=mynorm, cmap = mycmap, legend=False)
        ax.set_xticks([]); ax.set_xticklabels([])
        ax.set_yticks([]); ax.set_yticklabels([])
        #ax.set_axis_off()
        ax.set_xlim([exe_bng[0], exe_bng[2]])
        ax.set_ylim([exe_bng[1], exe_bng[3]])
        # Add a colorbar
        sm = plt.cm.ScalarMappable(cmap = mycmap, norm = mynorm)
        plt.colorbar(sm, ax=ax, label='Extreme Sea Level (m)', orientation='horizontal', fraction=0.042, pad=0.05)
        # Add UK map
        exemap.boundary.plot(ax=ax, aspect=1, linewidth=0.5, color='black')
        exemap.plot(ax=ax, aspect=1,  color='gainsboro')
        ax.text(0.7, 0.85, str(2020+10*idecade), transform=ax.transAxes)

mytitle = 'Exe Estuary 1-in-' + rlev[1:] + ' yr Sea Levels / ' +  myrcp.upper()
plt.text(-2.35, 4.0, mytitle, transform=ax.transAxes, fontsize=15)


plt.savefig('plot_extreme_wave_maps_'+myrcp+'.png')
