# (C) British Crown Copyright 2022, Met Office.
# Please see LICENSE for license details.
import logging

import iris

from .trajectory_manipulations import (
    convert_date_to_step,
    fill_trajectory_gaps,
)

logger = logging.getLogger(__name__)


def get_trajectories(tracked_file, nc_file, time_period, column_names):
    """
    Load the trajectories from the file output by TempestExtremes.

    :param str tracked_file: The path to the file produced by TempestExtremes.
    :param nc_file: The path to a netCDF file that the tracking was run on.
    :param int time_period: The time period in hours between time points in the
        data.
    :param dict column_names: the names of the column variables within the
        tracked_file, to be used as storm[] keys
    :returns: The loaded trajectories.
    :rtype: list
    """
    logger.debug(f"Running get_trajectories on {tracked_file}")

    # The text at the start of a header element in the TempestExtremes output
    header_delim = "start"

    coords_position = {
        "grid_x": 0,
        "grid_y": 1,
        "lon": 2,
        "lat": 3,
        "year": -4,
        "month": -3,
        "day": -2,
        "hour": -1,
    }
    # derive a dictionary with only the variables (needed later)
    coords_all = column_names
    coords_variable = list(column_names.keys()).copy()
    for pos in coords_position:
        coords_variable.remove(pos)

    # Initialize storms and line counter
    storms = []
    new_var = {}
    line_of_traj = None

    cube = iris.load_cube(nc_file)

    with open(tracked_file) as file_handle:
        for line in file_handle:
            line_array = line.split()
            if header_delim in line:  # check if header string is satisfied
                line_of_traj = 0  # reset trajectory line to zero
                track_length = int(line_array[1])
                storm = {}
                storms.append(storm)
                storm["length"] = track_length
                for coord in coords_all:
                    storm[coord] = []
                storm["step"] = []
            else:
                if line_of_traj <= track_length:
                    grid_x = int(line_array[coords_all["grid_x"]])
                    grid_y = int(line_array[coords_all["grid_y"]])
                    lon = float(line_array[coords_all["lon"]])
                    lat = float(line_array[coords_all["lat"]])
                    year = int(line_array[coords_all["year"]])
                    month = int(line_array[coords_all["month"]])
                    day = int(line_array[coords_all["day"]])
                    hour = int(line_array[coords_all["hour"]])
                    step = convert_date_to_step(
                        cube,
                        year,
                        month,
                        day,
                        hour,
                        time_period,
                    )
                    for var in coords_variable:
                        if line_array[coords_all[var]][0] == '"':
                            results = (
                                line_array[coords_all[var]].strip('"[]"').split(",")
                            )
                            results = [float(i) for i in results]
                            new_var[var] = results
                        else:
                            new_var[var] = float(line_array[coords_all[var]])
                    # now check if there is a gap in the traj, if so fill it in
                    if line_of_traj > 0:
                        if (step - storm["step"][-1]) > 1:
                            # add extra points before the next one
                            fill_trajectory_gaps(
                                storm,
                                step,
                                lon,
                                lat,
                                grid_x,
                                grid_y,
                                cube,
                                time_period,
                                new_var,
                            )
                    for coord in coords_position:
                        storm[coord].append(eval(coord))
                    for coord in coords_variable:
                        storm[coord].append(new_var[coord])
                    storm["step"].append(step)
                line_of_traj += 1  # increment line

    return storms
