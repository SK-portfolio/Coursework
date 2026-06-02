import pandas as pd
import numpy as np
# GHCNM-V4 doc: (https://www.ncei.noaa.gov/pub/data/ghcn/v4/readme.txt)
#------------------------[read inventory metadata]------------------------
##create empty dataframe for .inv file (use 1-based positions ['-' = 'to'])
#ID (1–11), LAT (13–20), LON (22–30), ELEV (32–37), NAME (39–68)

inv_colspecs = [
    (0, 11),   # station id
    (12, 20),  # latitude
    (21, 30),  # longitude
    (31, 37),  # elevation
    (38, 68)   # name
]

#set column names
inv_names = ["station", "lat", "lon", "elev", "name"]

#fill empty dataframe with fixed-width file data
df_inv = pd.read_fwf(
    "ghcnm.tavg.v4.0.1.20251123.qcf.inv",
    colspecs=inv_colspecs,
    names=inv_names,
    dtype={"station": str}
)

#------------------------[read temperature metadata]------------------------
#create empty dataframe for .dat file (uses 1-based positions ['-' = 'to'])
#ID (1–11), YEAR (12–15), ELEMENT (16–19)
                                     #^^ =[N]
dat_colspecs = [
    (0, 11),   # station
    (11, 15),  # year
    (15, 19),  # element
]

#loop for 12 months per year: (value, dm, qc, ds)
'''
VALUE_i ([N]-[N+5]),
DMFLAG_i ([N+5]-[N+6]),
QCFLAG_i ([N+6]-[N+7]),
DSFLAG_i ([N+7]-[N+8])
                 ^^^^ = [N]<new>
'''    

start = 19
for i in range(12):
    dat_colspecs.append((start, start + 5))      # month temp val
    dat_colspecs.append((start + 5, start + 6))  # data measurement flag
    dat_colspecs.append((start + 6, start + 7))  # quality ctrl flag
    dat_colspecs.append((start + 7, start + 8))  # data source flag
    start += 8

#set column names
dat_cols = ["station", "year", "element"]
for i in range(1, 13):
    dat_cols += [f"v{i}", f"dm{i}", f"qc{i}", f"ds{i}"]

#fill empty dataframe with fixed-width file data
df_temp = pd.read_fwf(
    "ghcnm.tavg.v4.0.1.20251123.qcf.dat",
    colspecs=dat_colspecs,
    names=dat_cols,
    dtype={"station": str}
)

#keep only TAVG (mean temperature)
df_temp = df_temp[df_temp["element"] == "TAVG"]

#------------------------[clean + convert tmp vals]------------------------
#in doc: monthly Val = integer hundredths °C, missing Val = -9999
#function to convert raw temp value
def convert_val(x):
    try:
        x = int(x)    #ensure it's an integer conversion
    except:
        return np.nan
    if x == -9999:    #missing value
        return np.nan
    return x / 100.0  #convert hundredths of °C → °C

#apply conversion to all monthly value columns
vcols = [f"v{i}" for i in range(1, 13)]

for c in vcols:
    df_temp[c] = df_temp[c].apply(convert_val)

#------------------------[filter europe & years 1924–2024]------------------------
#limit to europe based on lat/lon bounds [approximations based on (https://boundingbox.klokantech.com/)]
#lat: S, N | lon: W, E
df_inv_eur = df_inv[
    df_inv.lat.between(35, 71) &
    df_inv.lon.between(-25, 41)
]
#filter to years 1924–2024
df_temp_100yr = df_temp[df_temp.year.between(1924, 2024)]
#keep only stations in europe
df_temp_eur = df_temp_100yr[
    df_temp_100yr.station.isin(df_inv_eur.station)
]

#------------------------[merge .inv & .dat metadata]------------------------

df_final = df_temp_eur.merge(df_inv_eur, on="station", how="left")

#------------------------[compute annual mean temp]------------------------

df_final["annual_mean"] = df_final[vcols].mean(axis=1)

#------------------------[save as .csv]------------------------

df_final.to_csv("ghcnm_europe_1924_2024.csv", index=False)
print("Saved as CSV:", df_final.shape)
