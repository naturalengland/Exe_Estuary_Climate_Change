import numpy as np
import pandas as pd
import geopandas
from shapely.geometry import box
import matplotlib
import matplotlib.pyplot as plt
from convertbng.util import convert_bng, convert_lonlat

plt.ion()

# Select RCP scenario
#myrcp = 'rcp45'
myrcp = 'rcp85'

# Make a dataframe for the output. This will have return levels as columns and years as rows
# The dataframe is initialised with zero values
rlev = ['t1', 't2', 't5', 't10', 't20', 't25', 't50', 't75', 't100', \
        't150', 't200', 't250', 't300', 't500', 't1000', 't10000']
df = pd.DataFrame(index = 2020+10*np.arange(9), columns = rlev, data = 0.0)

# Exe estuary area coordinates (W,S,E,N)
exe_lonlat = [-3.524754, 50.549227, -3.254053, 50.745831]
exe_bng = [convert_bng(exe_lonlat[0], exe_lonlat[1])[0][0], \
           convert_bng(exe_lonlat[0], exe_lonlat[1])[1][0], \
           convert_bng(exe_lonlat[2], exe_lonlat[3])[0][0], \
           convert_bng(exe_lonlat[2], exe_lonlat[3])[1][0]]

# Extreme sea level data
indir = 'C:\\Users\\m1013956D\\OneDrive - Defra\\Python\\test_exe_estuary\\data\\'
infile = []
for idec in 2020+10*np.arange(9):
    infile.append(indir + 'esl_shp_' + myrcp + '_future_'+str(idec) + \
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
esl_exe2020 = esl2020[esl2020.intersects(box(*exe_bng))].copy()
esl_exe2030 = esl2030[esl2030.intersects(box(*exe_bng))].copy()
esl_exe2040 = esl2040[esl2040.intersects(box(*exe_bng))].copy()
esl_exe2050 = esl2050[esl2050.intersects(box(*exe_bng))].copy()
esl_exe2060 = esl2060[esl2060.intersects(box(*exe_bng))].copy()
esl_exe2070 = esl2070[esl2070.intersects(box(*exe_bng))].copy()
esl_exe2080 = esl2080[esl2080.intersects(box(*exe_bng))].copy()
esl_exe2090 = esl2090[esl2090.intersects(box(*exe_bng))].copy()
esl_exe2100 = esl2100[esl2100.intersects(box(*exe_bng))].copy()

# Add lon-lat as new columns
lonlat = convert_lonlat(list(esl_exe2020.x_bng.values), list(esl_exe2020.y_bng.values))
esl_exe2020['lon'] = lonlat[0]; esl_exe2020['lat'] = lonlat[1]
esl_exe2030['lon'] = lonlat[0]; esl_exe2030['lat'] = lonlat[1]
esl_exe2040['lon'] = lonlat[0]; esl_exe2040['lat'] = lonlat[1]
esl_exe2050['lon'] = lonlat[0]; esl_exe2050['lat'] = lonlat[1]
esl_exe2060['lon'] = lonlat[0]; esl_exe2060['lat'] = lonlat[1]
esl_exe2070['lon'] = lonlat[0]; esl_exe2070['lat'] = lonlat[1]
esl_exe2080['lon'] = lonlat[0]; esl_exe2080['lat'] = lonlat[1]
esl_exe2090['lon'] = lonlat[0]; esl_exe2090['lat'] = lonlat[1]
esl_exe2100['lon'] = lonlat[0]; esl_exe2100['lat'] = lonlat[1]

# Select 3 points with smallest distance to a reference point
refpoint = [-3.425468, 50.596961]
refdist =(np.array(lonlat[0])-refpoint[0])**2 + (np.array(lonlat[1])-refpoint[1])**2
iselect = refdist.argsort()[:3]
esl_exe2020 =  esl_exe2020.iloc[iselect].copy()
esl_exe2030 =  esl_exe2030.iloc[iselect].copy()
esl_exe2040 =  esl_exe2040.iloc[iselect].copy()
esl_exe2050 =  esl_exe2050.iloc[iselect].copy()
esl_exe2060 =  esl_exe2060.iloc[iselect].copy()
esl_exe2070 =  esl_exe2070.iloc[iselect].copy()
esl_exe2080 =  esl_exe2080.iloc[iselect].copy()
esl_exe2090 =  esl_exe2090.iloc[iselect].copy()
esl_exe2100 =  esl_exe2100.iloc[iselect].copy()

# List with all the data
gdf = [esl_exe2020, esl_exe2030, esl_exe2040, \
       esl_exe2050, esl_exe2060, esl_exe2070, \
       esl_exe2080, esl_exe2090, esl_exe2100]

# Get the mean return levels for all years
for icol in rlev:
    for irow in range(df.shape[0]):
        df.loc[df.index[irow], icol] = gdf[irow][icol].mean()

# Plotting
ax = plt.figure().add_subplot(111)
mylevels = ['t10', 't50', 't100', 't200', 't500']
mycolors = ['deepskyblue', 'royalblue', 'orange', 'red', 'darkred']

for ilev in range(len(mylevels)):
    ax.plot(df.index, df[mylevels[ilev]], color=mycolors[ilev])

ax.set_title('Exe Estuary Extreme Sea Levels / ' + myrcp.upper())
ax.set_xlabel('Year'); ax.set_ylabel('Sea Level (m)')

for ilev in range(len(mylevels)):
    ax.text(2020, 4.1-0.1*ilev, '1-in-'+mylevels[ilev][1:]+' Years', color=mycolors[ilev])

plt.savefig('plot_extreme_wave_tseries_'+myrcp+'.png')
