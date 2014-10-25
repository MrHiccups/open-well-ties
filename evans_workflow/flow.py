#!/usr/bin/env python

### #!/opt/local/bin/python2.7
## #!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
from las import LASReader

def f2m(thing):
    "converts feet to meters"
    if type(thing) == str:
        # if the input is a string
        converted = float(thing) * 0.3048 # Changed from evans to remove rounding error 
    elif type(thing) == float or int:
        # if the input is numeric
        converted = thing * 0.3048  # Changed from evans to remove rounding error 
    return converted

def tvdss(md):
    "assumes a vertical well"
    return md - f2m(L30.well.KB.data)


# [10]
# Used for allpying median filter to the logs 
def rolling_window(a, window):
        shape = a.shape[:-1] + (a.shape[-1] - window + 1, window)
        strides = a.strides + (a.strides[-1],)
        rolled = np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)
        return rolled

# [11] 
# Median filter 
def median_filter(input_array, window=13):
  # the length of filter is 13 samples or ~ 2 metres
  out_array = np.median(rolling_window(input_array,window), -1)
  out_array = np.pad(out_array, window/2, mode='edge')
  return out_array 

# [13]
# Despike filter
def despike(curve, window=13, max_clip=100): 
    curve_sm = median_filter(curve, window)
    spikes = np.where(curve - curve_sm > max_clip)[0]
    spukes = np.where(curve_sm - curve > max_clip)[0]
    out = np.copy(curve)
    out[spikes] = curve_sm[spikes] + max_clip  # Clip at the max allowed diff
    out[spukes] = curve_sm[spukes] - max_clip  # Clip at the min allowed diff
    return out

L30 = LASReader('L-30.las', null_subs=np.nan)

print L30.curves.names

print L30.curves.DEPTH.units

# [7]
z = f2m(L30.data['DEPTH'])      # convert feet to metres
GR = L30.data['GRS']
IL8 = L30.data['LL8']
ILM = L30.data['ILM']
ILD = L30.data['ILD']
NPHISS = L30.data['NPHISS']
NPHILS = L30.data['NPHILS']
ILD = L30.data['ILD']
DT = L30.data['DT']*3.28084     # convert usec/ft to usec/m
RHOB = L30.data['RHOB']*1000    # convert to SI units

# Deal with absence of logs in the shallow section 
#[8]
print "KB elevation [m]: ", f2m(L30.well.KB.data) # Kelly Bushing (ft)
print "Seafloor elevation [m]: ", f2m(L30.well.GL.data) # Depth to Sea Floor (ft)
print "Top of sonic log [m]: ", f2m(L30.start)  # top of log (ft) (actually 1150 ft)

repl_int = f2m(L30.start) - f2m(L30.well.KB.data) + f2m(L30.well.GL.data)
water_vel = 1480
print "replacement interval [m]: ", repl_int

repl_vel = 1600 # m/s
repl_time = 2 * repl_int / repl_vel
print "two-way-replacement time: ", repl_time

water_time = 2 * np.abs(f2m(L30.well.GL.data)) / water_vel
print "seafloor bottom :", water_time

log_start_time = water_time + repl_time
print 'log_start_time:', log_start_time

top_log_TVDss = f2m(L30.well.KB.data) - f2m(L30.well.GL.data) 

# Fix and edit the logs
# [11] (now in median_filter)
rho_sm = median_filter(RHOB)

# In [14]:
rho = despike(RHOB)

start = 13000
end = 14500


# In [15] (shoudl go into a function)
plt.figure(figsize=(18,4))
plt.plot(z[start:end], RHOB[start:end],'k')
plt.plot(z[start:end], rho_sm[start:end],'b')
plt.plot(z[start:end], rho[start:end],'r')
plt.title('de-spiked density')
plt.show()

 
