#!/usr/bin/env python

import numpy as np
import matplotlib as mpl
mpl.use('pdf')
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

#def plot_logs(fig_name, depth, log1, log2, start, end, title=''):
#    plt.figure(figsize=(4,18))
#    plt.plot(log1[start:end], depth[start:end],'k')
#    plt.plot( log2[start:end], depth[start:end],'r')
#    #plt.set_ylim([start,end])
#    plt.title(title)
#    plt.savefig(fig_name+'.pdf')

def plot_logs(fig_name, depth, log1, log2, start, end, title=''): 
    fig = plt.figure(figsize=(4,18))
    ax = fig.add_subplot(1,1,1)    
    ax.plot(log1, depth,'k')
    ax.plot( log2, depth ,'r')
    ax.set_ylim([start,end])
    ax.set_title(title) 
    fig.savefig(fig_name+'.pdf') 


# [27] output a ricker wavelet 
def ricker(f, length, dt):
    t = np.linspace(-length / 2, (length-dt) / 2, length / dt)
    y = (1. - 2.*(np.pi**2)*(f**2)*(t**2))*np.exp(-(np.pi**2)*(f**2)*(t**2))
    return t, y

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

#start_z = 13000
#end_z = 14500
start_z = 2300
end_z = 2600

# In [15] (shoudl go into a function)
plot_logs('density', z, RHOB, rho, start_z, end_z, title='de-spiked density')

# [16] filter sonic
dt = despike(DT)

# Plot sonic
plot_logs('sonic', z, DT, dt, start_z, end_z, title='de-spiked sonic')
 
# [18] Computing the time-to-depth relationship
# The time-to-depth relationship is obtained by scaling the sonic log by the sample interval (6" or 0.1524 m) and by calling np.cumsum() on it.
# two-way-time to depth relationship
scaled_dt = 0.1524 * np.nan_to_num(dt) / 1e6

tcum = 2 * np.cumsum(scaled_dt)
tdr = tcum + log_start_time

# [19] Compute acoustic impedance
Z = (1e6/dt) * rho

plot_logs('ai_depth', z, Z, Z, start_z, end_z, title='Acoustic Impedance')

# [20] Compute reflection coefficient series
RC = (Z[1:] - Z[:-1]) / (Z[1:] + Z[:-1])

z_size = z.size
rc_size = RC.size 
print " RC.size = "+str(rc_size)
print "z.size = "+str(z_size)
RC = np.resize(RC, z.size )
plot_logs('well_reflectivity', z, RC, RC, start_z, end_z, title='well reflectivity')

#### I'm ignoring the side by side QC plots for now as they are not necessary. #### 

# [26] Converting logs to two-way-travel time

# RESAMPLING FUNCTION
dt = 0.004
maxt = 3.0 + dt

start_t = 1.4
end_t = 2.5 

print "min z = "+str(z.min()) +" max z = "+str(z.max() )


t = np.arange(0, maxt, dt) 

print "min t = "+str(t.min()) +" max t = "+str(t.max() )

print "min tdr = "+str(tdr.min()) +" max tdr = "+str(tdr.max() )


Z_t = np.interp(x = t, xp = tdr, fp = Z)

Z_t_nn = np.nan_to_num(Z_t)
print "min Z_t = "+str(Z_t_nn.min()) +" max Z_t = "+str(Z_t_nn.max() )

plot_logs('ai_time', t, Z_t_nn, Z_t_nn, start_t, end_t, title='impedence in time')

RC_t = (Z_t[1:] - Z_t[:-1]) / (Z_t[1:] + Z_t[:-1])

 
RC_t = np.nan_to_num(RC_t)
tw, w = ricker (f=25, length = 0.512, dt = 0.004)
synth = np.convolve(w, RC_t, mode='same')

synth = np.resize(synth, t.size )
plot_logs('synthetic', t, synth, synth, start_t, end_t, title='synthetic')







 
