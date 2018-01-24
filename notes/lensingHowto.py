#
# lensdemo_script.py
#
# A script to allow simple explortation of gravitational lensing
# of extended objects (i.e., galaxies) by the gravity of a singular
# isothermal ellipsoid (SIE) potential.
#
# This script is meant to be used as a cut-and-paste guide to an interactive
# python2.5 command-line session, and is not necessarily to be run in
# unmodified form from end to end.
#
# Requires numpy and matplotlib, as well as the suporting file "lensdemo_funcs.py"
#
# Copyright 2009 by Adam S. Bolton
# Creative Commons Attribution-Noncommercial-ShareAlike 3.0 license applies:
# http://creativecommons.org/licenses/by-nc-sa/3.0/
# All redistributions, modified or otherwise, must include this
# original copyright notice, licensing statement, and disclaimer.
# DISCLAIMER: ABSOLUTELY NO WARRANTY EXPRESS OR IMPLIED.
# AUTHOR ASSUMES NO LIABILITY IN CONNECTION WITH THIS COMPUTER CODE.
#

# Import the necessary packages
import numpy as np
import matplotlib as m
# The following 2 lines are necessary to make the
# GUI work right, at least for me. YMMV!
m.use('TkAgg')
m.interactive(True)
from matplotlib import pyplot as plt
from matplotlib import cm
import lensdemo_funcs as ldf

# Package some image display preferences in a dictionary object, for use below:
myargs = {'interpolation': 'nearest', 'origin': 'lower', 'cmap': cm.spectral}
#myargs = {'interpolation': 'nearest', 'origin': 'lower', 'cmap': cm.gray}

# Make some x and y coordinate images:
nx = 501
ny = 501
xhilo = [-2.5, 2.5]
yhilo = [-2.5, 2.5]
x = (xhilo[1] - xhilo[0]) * np.outer(np.ones(ny), np.arange(nx)) / float(nx-1) + xhilo[0]
y = (yhilo[1] - yhilo[0]) * np.outer(np.arange(ny), np.ones(nx)) / float(ny-1) + yhilo[0]

# Set some Gaussian blob image parameters and pack them into an array:
g_amp = 1.0   # peak brightness value
g_sig = 0.05  # Gaussian "sigma" (i.e., size)
g_xcen = 0.0  # x position of center
g_ycen = 0.0  # y position of center
g_axrat = 1.0 # minor-to-major axis ratio
g_pa = 0.0    # major-axis position angle (degrees) c.c.w. from x axis
gpar = np.asarray([g_amp, g_sig, g_xcen, g_ycen, g_axrat, g_pa])

# Have a look at the un-lensed Gaussian image:
g_image = ldf.gauss_2d(x, y, gpar)
f = plt.imshow(g_image, **myargs)
# IMPORTANT: Kill these imshow GUIs before redisplaying, or you will get bad memory leaks!
# You can kill it with the "red button", or with the following command:
plt.close(f.get_figure().number)
# Alternatively, if you do the following you will probably be OK redisplaying
# without killing the GUI:
# f.axes.hold(False)

# Set some SIE lens-model parameters and pack them into an array:
l_amp = 1.5   # Einstein radius
l_xcen = 0.0  # x position of center
l_ycen = 0.0  # y position of center
l_axrat = 1.0 # minor-to-major axis ratio
l_pa = 0.0    # major-axis position angle (degrees) c.c.w. from x axis
lpar = np.asarray([l_amp, l_xcen, l_ycen, l_axrat, l_pa])

# Compute the lensing potential gradients:
(xg, yg) = ldf.sie_grad(x, y, lpar)

# Evaluate lensed Gaussian image:
g_lensimage = ldf.gauss_2d(x-xg, y-yg, gpar)

# Have a look:
f = plt.imshow(g_lensimage, **myargs)

# If you can recall what the parameter place values mean,
# the following lines are most efficient for exploration:
gpar = np.asarray([1.0, 0.05, 0.0, 0.0, 1.0, 0.0])
lpar = np.asarray([1.5, 0.0, 0.0, 1.0, 0.0])
(xg, yg) = ldf.sie_grad(x, y, lpar)
g_lensimage = ldf.gauss_2d(x-xg, y-yg, gpar)
f = plt.imshow(g_lensimage, **myargs)
# f.axes.hold(False)

# The following lines will plot the un-lensed and lensed images side by side:
gpar = np.asarray([1.0, 0.05, 0.0, 0.0, 1.0, 0.0])
lpar = np.asarray([1.0, 0.0, 0.0, 1.0, 0.0])
g_image = ldf.gauss_2d(x, y, gpar)
(xg, yg) = ldf.sie_grad(x, y, lpar)
g_lensimage = ldf.gauss_2d(x-xg, y-yg, gpar)
f = plt.imshow(np.hstack((g_image, g_lensimage)), **myargs)


# The following lines can be used to verify that the SIE potential gradient
# function actually computes what is is supposed to compute!
# Feel free to disregard...

# Pick some arbitrary lens parameters:
lpar = np.asarray([1.11, -0.23, 0.59, 0.72, 33.3])
# Compute the gradients:
(xg, yg) = ldf.sie_grad(x, y, lpar)
# Compute convergence as half the Laplacian of the potential from the gradients:
kappa_g = 0.5 * ( (xg[1:-1,2:] - xg[1:-1,0:-2]) / (x[1:-1,2:] - x[1:-1,0:-2]) +
                  (yg[2:,1:-1] - yg[0:-2,1:-1]) / (y[2:,1:-1] - y[0:-2,1:-1]))
# Compute the expected analytic convergence for these lens parameters:
(xn, yn) = ldf.xy_rotate(x, y, lpar[1], lpar[2], lpar[4])
kappa_a = 0.5 * lpar[0] / np.sqrt(lpar[3]*xn[1:-1,1:-1]**2 + yn[1:-1,1:-1]**2 / lpar[3])

f = plt.imshow(np.hstack((np.log(kappa_g), np.log(kappa_a), np.log(kappa_g) - np.log(kappa_a))),
             vmax=np.log(kappa_g).max(), vmin=np.log(kappa_g).min(), **myargs)
# OK, looks good!  Some disagreement in the center, which is to be expected.

plt.show(block=True)
