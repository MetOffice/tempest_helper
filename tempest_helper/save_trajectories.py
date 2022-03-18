# (C) British Crown Copyright 2021, Met Office.
# Please see LICENSE for license details.
import os
import logging

from cftime import date2num, datetime
from netCDF4 import Dataset
import numpy as np

logger = logging.getLogger(__name__)

DEFAULT_VARIABLE_UNITS = {
    "slp": "Pa",
    "sfcWind": "m s-1",
    "zg": "m",
    "orog": "m",
    "wind925": "m s-1",
    "wind850": "m s-1",
    "rvT63": "s-1",
    "rvT63_1": "m s-1",
    "zg_1": "m",
}


def _define_netcdf_metadata(var, variable_units):
    """
    Define potential metadata for the netcdf variables

    :param str var: Variable name for which metadata is required
    :param variable_units: The units of the variables
    :return: strings for netcdf metadata for standard_name,
        long_name, description, units
    :rtype: Four strings
    """
    standard_name = "unknown"
    long_name = "unknown"
    description = "unknown"
    units = "1"

    if "slp" in var:
        standard_name = "air_pressure_at_mean_sea_level"
        long_name = "Sea Level Pressure"
        description = "Sea level pressure for tracked variable"
        units = variable_units["slp"]
    elif "sfcWind" in var:
        standard_name = "wind_speed"
        long_name = "Near-surface Wind Speed"
        description = "near-surface (usually 10 metres) wind speed"
        units = variable_units["sfcWind"]
    elif "orog" in var:
        standard_name = "surface_altitude"
        long_name = "Surface Altitude"
        description = "Surface altitude (height above sea level)"
        units = variable_units["orog"]
    elif "wind" in var:
        standard_name = "wind_speed"
        units = variable_units["sfcWind"]
    elif "rv" in var:
        standard_name = "relative_vorticity"
        units = "s-1"
    elif "zg" in var:
        standard_name = "geopotential_height"
        long_name = "Geopotential Height"
        description = "Geopotential height difference"
        units = "m"

    return standard_name, long_name, description, units


def save_trajectories_netcdf(
    directory,
    savefname,
    storms,
    calendar,
    time_units,
    variable_units,
    frequency,
    um_suiteid,
    resolution_code,
    cmd_detect,
    cmd_stitch,
    output_vars,
    startperiod="",
    endperiod="",
    title="Tempest TC tracks",
    institution_id="MOHC",
    algorithm="TempestExtremes_v2",
    algorithm_ref=(
        "Ullrich and Zarzycki 2017; Zarzycki and Ullrich 2017; " "Ullrich et al. 2020"
    ),
):
    """
    Create netCDF file for the tracks.

    :param str directory: Output directory
    :param str savefname: Output filename
    :param list storms: The loaded trajectories, each list component is a
        dictionary.
    :param str calendar: The calendar used by the model (360_day, gregorian etc)
    :param str time_units: The units for the calendar
    :param dict variable_units: The units of the variables as a dictionary
    :param str frequency: The frequency of the data for netCDF metadata
    :param str um_suiteid: The model suiteid for netCDF metadata
    :param str resolution_code: The resolution string (e.g. N216)
    :param str cmd_detect: The command string used in the detection
    :param str cmd_stitch: The command string used in the stitching
    :param list output_vars: The variables required in the netCDF file (lat and
        lon are always included and do not need to be specified here)
    :param str startperiod: The start of the time period for this file to include
        as a global attribute (format is user defined)
    :param str endperiod: The end of the time period for this file to include
        as a global attribute (format is user defined)
    :param str title: The title global attribute to include in the file
    :param str institution_id: The institution_id global attribute  to include
        in the file
    :param str algorithm: The algorithm global attribute to include in the file
    :param str algorithm_ref: The algorithm_ref global attribute to include
        in the file
    """
    logger.debug("making netCDF of outputs")

    nc = Dataset(os.path.join(directory, savefname), "w", format="NETCDF4")
    nc.title = title
    nc.directory = directory
    nc.tracked_data_frequency = frequency

    nc.mo_runid = um_suiteid
    nc.grid = resolution_code
    nc.start_date = startperiod
    nc.end_date = endperiod
    nc.institution_id = institution_id
    nc.algorithm = algorithm
    nc.algorithm_ref = algorithm_ref
    nc.detect_cmd = cmd_detect
    nc.stitch_cmd = cmd_stitch

    record_length = 0
    tracks = 0
    for storm in storms:
        tracks += 1
        storm_length = storm["length"]
        record_length += storm_length

    nc.createDimension("tracks", size=tracks)  # unlimited dimension
    nc.createDimension("record", size=record_length)

    nc.createVariable("FIRST_PT", np.int32, ("tracks",))
    nc.createVariable("NUM_PTS", np.int32, ("tracks",))
    nc.createVariable("TRACK_ID", np.int32, ("tracks",))
    nc.createVariable("index", np.int32, ("record",))
    nc.createVariable("time", "f8", ("record",))
    nc.createVariable("lon", "f4", ("record",))
    nc.createVariable("lat", "f4", ("record",))

    for var in output_vars:
        nc.createVariable(var, "f8", ("record",))

    nc.variables["FIRST_PT"].units = "ordinal"
    nc.variables["FIRST_PT"].long_name = "first_pt"
    nc.variables["FIRST_PT"].description = "Index to first point of this track number"

    nc.variables["NUM_PTS"].units = "ordinal"
    nc.variables["NUM_PTS"].long_name = "num_pts"
    nc.variables["NUM_PTS"].description = "Number of points for this track"

    nc.variables["TRACK_ID"].units = "ordinal"
    nc.variables["TRACK_ID"].long_name = "track_id"
    nc.variables["TRACK_ID"].description = "Tropical cyclone track number"

    nc.variables["index"].units = "ordinal"
    nc.variables["index"].long_name = "track_id"
    nc.variables["index"].description = "Track sequence number (0-length of track-1)"

    nc.variables["lat"].units = "degrees_north"
    nc.variables["lat"].standard_name = "latitude"
    nc.variables["lat"].long_name = "latitude"
    nc.variables["lat"].description = (
        "Latitude (degrees north) associated " + "with tracked variable"
    )

    nc.variables["lon"].units = "degrees_east"
    nc.variables["lon"].standard_name = "longitude"
    nc.variables["lon"].long_name = "longitude"
    nc.variables["lon"].description = (
        "Longitude (degrees east) associated " + "with tracked variable"
    )

    nc.variables["time"].units = time_units
    nc.variables["time"].calendar = calendar
    nc.variables["time"].standard_name = "time"
    nc.variables["time"].long_name = "time"

    if not variable_units:
        variable_units = DEFAULT_VARIABLE_UNITS

    for var in output_vars:
        standard_name, long_name, description, v_units = _define_netcdf_metadata(
            var, variable_units
        )

        logger.debug(f"var, units {var} {v_units} ")
        nc.variables[var].standard_name = standard_name
        nc.variables[var].long_name = long_name
        nc.variables[var].description = description
        nc.variables[var].units = str(v_units)

    # read the storms and write the values to the file
    # track: first_pt, num_pts, track_id
    # record: lat, lon, time, slp, index(0:tracklen-1)
    first_pt = []
    num_pts = []
    track_id = []
    lon = []
    lat = []
    time = []
    index = []

    variables_to_write = {}
    for var in output_vars:
        variables_to_write[var] = []

    first_pt_index = 0
    for ist, storm in enumerate(storms):
        first_pt.append(first_pt_index)
        num_pts.append(storm["length"])
        track_id.append(ist)
        first_pt_index += storm["length"]

        for ipt in range(storm["length"]):
            t1 = date2num(
                datetime(
                    storm["year"][ipt],
                    storm["month"][ipt],
                    storm["day"][ipt],
                    storm["hour"][ipt],
                ),
                time_units,
                calendar=calendar,
            )
            time.append(t1)
            index.append(ipt)
            lon.append(storm["lon"][ipt])
            lat.append(storm["lat"][ipt])
            for var in output_vars:
                variables_to_write[var].append(storm[var][ipt])

    logger.debug(f"first_pt {first_pt} ")
    logger.debug(f"tracks, record_length {tracks} {record_length} ")
    logger.debug(f"len(first_pt) {len(first_pt)} ")
    logger.debug(f"len(lon) {len(lon)} ")
    # now write variables to netcdf
    nc.variables["FIRST_PT"][:] = first_pt
    nc.variables["NUM_PTS"][:] = num_pts
    nc.variables["TRACK_ID"][:] = track_id
    nc.variables["index"][:] = index
    nc.variables["lon"][:] = lon
    nc.variables["lat"][:] = lat
    nc.variables["time"][:] = time
    for var in output_vars:
        logger.debug(f"var {var} ")
        nc.variables[var][:] = variables_to_write[var]

    nc.close()
