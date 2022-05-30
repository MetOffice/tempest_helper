# (C) British Crown Copyright 2022, Met Office.
# Please see LICENSE for license details.
import cartopy.crs as ccrs
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402


def plot_trajectories_cartopy(storms, filename, title=""):
    """
    Use Cartopy to plot the loaded trajectories and save them in the specified
    file.

    :param list storms: The loaded trajectories.
    :param str filename: The full path to save the plot as.
    :param str title: An optional title to include on the plot.
    """
    fig = plt.figure(figsize=(9, 6), dpi=100)
    ax = plt.axes(projection=ccrs.PlateCarree(central_longitude=-160))
    ax.set_global()

    for storm in storms:
        ax.plot(storm["lon"], storm["lat"], linewidth=1.2, transform=ccrs.Geodetic())

    fig.gca().coastlines()

    if title:
        plt.title(title)
    plt.savefig(filename)
    # plt.show()
    plt.close(fig)
