# PULLING IMAGE DOWN FROM APOD WEBSITE
from bs4 import BeautifulSoup
import requests
import re
import urllib2
import os
import cookielib
import json
import sys
import urllib

arguments = sys.argv
DIR = "./pictures"
number_of_images = int(arguments[1])

for i in range(number_of_images):
    print 'running download and lens script on image #', i

    url = arguments[i + 2]
    ImageToBeSaved = os.path.join(DIR, "Image" + str(i) + ".jpg")
    LensedImageToBeSaved = os.path.join(DIR, "Image" + str(i) + "_Lensed.jpg")

    # delete only if file exists
    if os.path.exists(ImageToBeSaved):
        os.remove(ImageToBeSaved)
        print "The old %s file was deleted." % ImageToBeSaved
    else:
        print "The %s file did not exist." % ImageToBeSaved

    if not os.path.exists(DIR):
        os.mkdir(DIR)

    img = url

    try:
        urllib.urlretrieve(img, ImageToBeSaved)
        foundImage = 1

    except Exception as e:
        print "could not load : " + img
        print e
        foundImage = 0

    # GRAVITATIONAL LENSING
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy import misc
    import astropy.units as u
    import random

    def SourceCoord_vals(x, y):
        # Position x,y on lensed image

        # radius from x,y to deflector x_def,y_def
        r = ((x - x_def)**2 + (y - y_def)**2)**0.5 * plate_scale_val

        # theta, angle from x,y to deflector
        theta = np.arctan(r / d_s_val)

        # beta, angle from x,y to source
        beta = theta - theta_E_val**2 / theta

        # radius from source to deflector
        r_sou = np.copysign(np.tan(beta) * d_s_val /
                            plate_scale_val, np.tan(beta))

        # source x and y positions
        x_sou = x_def + r_sou * plate_scale_val * (x - x_def) / r
        y_sou = y_def + r_sou * plate_scale_val * (y - y_def) / r

        # magnification
        mu = 1 / (1 - (theta_E_val / theta)**4)

        # returns source x and y positions
        if (x == x_def) & (y == y_def):
            return x_def, y_def
        else:
            return int(x_sou), int(y_sou)

    if foundImage:
        image1 = misc.imread(ImageToBeSaved)

        n_x_pix = len(image1)
        n_y_pix = len(image1[0])

        G = 6.67408 * 10**-11 * u.m**3 / (u.kg * u.s**2)
        c = 3 * 10**8 * u.m / u.s
        M = random.randint(10**15, 10**16) * u.kg

        x_def = random.randint(n_x_pix * 1 / 4, n_x_pix * 3 / 4)
        y_def = random.randint(n_y_pix * 1 / 4, n_y_pix * 3 / 4)

        d_d = 3.5 * 10**40 * u.lyr
        d_ds = 3.5 * 10**30 * u.lyr
        d_s = d_d + d_ds

        plate_scale = (.25 * u.pc).to(u.lyr)

        theta_E = (np.sqrt(4 * G * M * d_ds / (d_d * d_s * c**2))
                   * u.rad).decompose()

        d_s_val = d_s.value  # Light Years
        plate_scale_val = plate_scale.value  # lyr/pixel
        theta_E_val = theta_E.value

        print 'Einstein Radius:', (theta_E_val * d_s_val / (plate_scale_val)), 'pixels'

        image2 = np.zeros([n_x_pix, n_y_pix, 3])
        for i in range(n_x_pix):
            for j in range(n_y_pix):
                x_sou, y_sou = SourceCoord_vals(i, j)
                if (x_sou < n_x_pix) & (x_sou > 0) & (y_sou < n_y_pix) & (y_sou > 0) == True:
                    image2[i][j] = image1[x_sou][y_sou]

        misc.imsave(LensedImageToBeSaved, image2)
