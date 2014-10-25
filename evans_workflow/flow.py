#!/usr/bin/env python


import numpy as np
from las import LASReader
L30 = LASReader('L-30.las', null_subs=np.nan)

print L30.curves.names

print L30.curves.DEPTH.units


