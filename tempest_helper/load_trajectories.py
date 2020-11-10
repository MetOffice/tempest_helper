# (C) British Crown Copyright 2020, Met Office.
# Please see LICENSE for license details.
import logging

import iris

from .trajectory_manipulations import convert_date_to_step, fill_trajectory_gaps

logger = logging.getLogger(__name__)


def get_trajectories(tracked_file, num_vars_stitch, nc_file):
    """
    Load the trajectories from the file output by TempestExtremes.

    :param str tracked_file: The path to the file produced by TempestExtremes.
    :param num_vars_stitch: The number of variables in the output file.
    :param nc_file: The path to a netCDF file that the tracking was run on.
    :returns: The loaded trajectories.
    :rtype: list
    """
    logger.debug(f'Running getTrajectories on {tracked_file}')

    # The text at the start of a header element in the TempestExtremes output
    header_delim = 'start'

    # TODO why - 2 + 1?
    num_vars_offset = num_vars_stitch - 2 + 1

    coords = {
        'lon': 2,
        'lat': 3,
        'year': 3 + num_vars_offset,
        'month': 3 + num_vars_offset + 1,
        'day': 3 + num_vars_offset + 2,
        'hour': 3 + num_vars_offset + 3
    }

    # Initialize storms and line counter
    storms = []
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
                storm['length'] = track_length
                for coord in coords:
                    storm[coord] = []
                storm['step'] = []
            else:
                if line_of_traj <= track_length:
                    lon = line_array[coords['lon']]
                    lat = line_array[coords['lat']]
                    year = line_array[coords['year']]
                    month = line_array[coords['month']]
                    day = line_array[coords['day']]
                    hour = line_array[coords['hour']]
                    step = convert_date_to_step(
                        cube,
                        int(year),
                        int(month),
                        int(day),
                        int(hour)
                    )
                    # now check if there is a gap in the traj, if so fill it in
                    if line_of_traj > 0:
                        if (step - storm['step'][-1]) > 1:
                            # add extra points before the next one
                            fill_trajectory_gaps(storm, step, lon, lat,
                                                 year, month, day, hour)
                    for coord in coords:
                        storm[coord].append(line_array[coords[coord]])
                    storm['step'].append(step)
                line_of_traj += 1  # increment line

    #TODO document in data_format.rst the structure of storms
    return storms
