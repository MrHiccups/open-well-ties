#!/usr/bin/env python

import sys
import numpy as np
import matplotlib as mpl
mpl.use('pdf')
import matplotlib.pyplot as plt

sys.path.append('./synth')
import synth  
#from synth.synth import generate_reflectivity 
#from synth.synth import ricker
#from synth.synth import plot_logs
#from synth.synth import plot_spectrum
from synth.synth import *


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


t, RC_t = generate_reflectivity()

tw, w = ricker (f=25, length = 0.512, dt = 0.004)
synthetic = np.convolve(w, RC_t, mode='same')

synthetic = np.resize(synthetic, t.size )
plot_logs('./outputs/synthetic.pdf', 'pdf', t, synthetic, synthetic, start_t, end_t, title='Synthetic')

plot_spectrum('./outputs/well_RC_spectrum.pdf', 'pdf', RC_t)

np.savetxt("./outputs/reflectivity.txt", (RC_t))
np.savetxt("./outputs/time.txt", (t))

real_trace = get_data_trace( './data/PenobXL_1155.txt', 314)

plot_logs('./outputs/real_trace.pdf', 'pdf', t, real_trace, real_trace, start_t, end_t, title='Real Trace')
np.savetxt("./outputs/real_trace.txt", (real_trace))

plot_spectrum('./outputs/trace_spectrum.pdf', 'pdf', real_trace)

# Generate gabor filter and apply to logs
gab = gabor_filt()
synth2 = np.convolve(gab, RC_t, mode='same') 
synth2 = np.resize(synth2, t.size)

plot_spectrum('./outputs/well_synth2_spectrum.pdf', 'pdf', synth2)

plot_logs('./outputs/real_trace2.pdf', 'pdf', t, real_trace, synth2, start_t, end_t, title='Real Trace')



