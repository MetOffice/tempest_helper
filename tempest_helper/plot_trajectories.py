# (C) British Crown Copyright 2020, Met Office.
# Please see LICENSE for license details.
import logging
import os

import cartopy.crs as ccrs
import matplotlib
if not os.getenv('DISPLAY'):
    matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E402


def plot_trajectories_cartopy(storms, filename, title=''):
    """
    Use Cartopy to plot the loaded trajectories and save them in the specified
    file.

    :param list storms: The loaded trajectories.
    :param str filename: The full path to save the plot as.
    :param str title: An optional title to include on the plot.
    """
    fig = plt.figure(figsize=(9,6), dpi=100)
    ax = plt.axes(projection=ccrs.PlateCarree(central_longitude=-160))
    ax.set_global()

    for storm in storms:
        lon = [float(index) for index in storm['lon']]
        lat = [float(index) for index in storm['lat']]
        ax.plot(lon, lat, linewidth=1.2, transform=ccrs.Geodetic())

    fig.gca().coastlines()

    if title:
        plt.title(title)
    plt.savefig(filename)
    plt.show()
