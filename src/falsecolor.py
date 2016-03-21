import numpy as np
import os
import re
import sys
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, RadioButtons

fname = sys.argv[1]

def search_spp(fname):
    found = re.search('_S([0-9]+)', fname)
    if found == None:
        return 1
    else:
        return found.group(1)

def load_data(fname, dtype=np.int64, spp=1):
    return np.loadtxt(fname, dtype=dtype, delimiter=' ', ndmin = 2) / float(spp)
    
def show_data(D, cmap='jet'):
    return plt.imshow(D, cmap=cmap)

fig, ax = plt.subplots()
plt.subplots_adjust(left=0.25)
ax_color = 'lightgoldenrodyellow'

title = os.path.basename(fname)
fig.canvas.set_window_title(title)
fig.suptitle(title)

# -- DATA --
D = load_data(fname, spp=search_spp(fname))
imgplt = show_data(D, cmap='jet')
plt.colorbar()

# -- LOG SELECTION --
ax_log = plt.axes([0.25, 0.1, 0.4, 0.03], axisbg=ax_color)
slider = Slider(ax_log, 'Log', 1.0, 2.0, valinit=1.0)
def update(val):
    if (val == 1.0):
        imgplt.set_data(D)
    else:
        imgplt.set_data(np.log(D.copy()) / np.log(val))
    fig.canvas.draw_idle()
slider.on_changed(update)

# -- COLOR MAP SELECTION --
ax_cmap = plt.axes([0.025, 0.5, 0.15, 0.15], axisbg=ax_color)
radio = RadioButtons(ax_cmap, ('jet', 'Greys', 'hot', 'seismic', 'spectral'), active=0, activecolor='blue')
def change_cmap(label):
    imgplt.set_cmap(label)
    fig.canvas.draw_idle()
radio.on_clicked(change_cmap)

plt.show()