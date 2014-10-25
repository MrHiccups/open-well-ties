#!/usr/bin/env python

import numpy as np
import matplotlib as mpl
mpl.use('pdf')
import matplotlib.pyplot as plt
import synth 

from las import LASReader




#QC plots 
start_z = 2300
end_z = 2600

start_t = 1.4
end_t = 2.5

# In [15] (shoudl go into a function)
#plot_logs('density', z, RHOB, rho, start_z, end_z, title='de-spiked density')

# Plot sonic
#plot_logs('sonic', z, DT, dt, start_z, end_z, title='de-spiked sonic')

#plot_logs('ai_depth', z, Z, Z, start_z, end_z, title='Acoustic Impedance')

#plot_logs('ai_time', t, Z_t_nn, Z_t_nn, start_t, end_t, title='impedence in time')


r, RC_t = synth.generate_reflectivity()

tw, w = synth.ricker (f=25, length = 0.512, dt = 0.004)
synthetic = np.convolve(w, RC_t, mode='same')

synthetic = np.resize(synthetic, t.size )
plot_logs('synthetic', t, synthetic, synthetic, start_t, end_t, title='synthetic')


RC_t.savetxt("reflectivity.txt")



