# (C) British Crown Copyright 2020, Met Office.
# Please see LICENSE for license details.
import datetime

import cftime

# cftime v1.0.0 doesn't allow a keyword to the datetime method to specify,
# but this introduced in v1.2.0 and so will have to use the code below to
# specify the type of datetime object to create
DATETIME_TYPES = {
    "noleap": cftime.DatetimeNoLeap,
    "all_leap": cftime.DatetimeAllLeap,
    "360_day": cftime.Datetime360Day,
    "julian": cftime.DatetimeJulian,
    "gregorian": cftime.DatetimeGregorian,
    "standard": cftime.DatetimeGregorian,
    "proleptic_gregorian": cftime.DatetimeProlepticGregorian,
}


def convert_date_to_step(cube, year, month, day, hour, time_period):
    """
    Calculate the step number, with the first time in a file have a step number
    of one. All calendars are handled.

    :param iris.Cube.cube cube: A cube loaded from a data file from the
        current period.
    :param int year: The current year.
    :param int month: The current month.
    :param int day: The current day of month.
    :param int hour: The current hour.
    :param int time_period: The time period in hours between time points in the
        data.
    :returns: The time index at the specified time point.
    :rtype: int
    """

    calendar = cube.coord("time").units.calendar

    current_datetime = DATETIME_TYPES[calendar](year, month, day, hour)
    first_point = cube.coord("time").units.num2date(cube.coord("time").points[0])
    time_delta = current_datetime - first_point
    seconds_in_hour = 60 ** 2
    return round(time_delta.total_seconds() / (time_period * seconds_in_hour)) + 1


def fill_trajectory_gaps(storm, step, lon, lat, cube, time_period, new_var):
    """
    Fill the gap by linearly interpolating the last latitude, longitude,
    time and other values from the last of these values up to step. The 
    trajectory is passed in to the `storm` attribute and is a standard 
    `tempest_helper` dictionary. Longitudes and their interpolation may wrap 
    around the 0/360 degree numerical discontinuity. The longitudes output 
    are between 0 and 359 degrees.

    :param dict storm: Details of the current storm.
    :param int step: The integer number of time points of the current
        point since the start of the file.
    :param float lon: The longitude of the current point in the storm in
        degrees.
    :param float lat: The latitude of the current point in the storm in
        degrees.
    :param dict new_var: The other variables contained in the storm at the current point
    :param iris.cube.Cube cube: A cube loaded from a data file from the
        current period.
    :param int time_period: The time period in hours between time points in the
        data.

    """

    gap_length = step - storm["step"][-1]
    # Using technique at https://stackoverflow.com/a/14498790 to handle
    # longitudes wrapping around 0/360
    dlon = (((lon - storm["lon"][-1]) + 180) % 360 - 180) / gap_length
    dlat = (lat - storm["lat"][-1]) / gap_length
    for gap_index in range(1, gap_length):
        lon1 = (storm["lon"][-1] + dlon) % 360
        lat1 = storm["lat"][-1] + dlat
        storm["lon"].append(lon1)
        storm["lat"].append(lat1)
        storm["step"].append(storm["step"][-1] + 1)
        # interpolate the time too
        step_time_components = _calculate_gap_time(
            cube,
            storm["year"][-1],
            storm["month"][-1],
            storm["day"][-1],
            storm["hour"][-1],
            time_period,
        )
        storm["year"].append(step_time_components[0])
        storm["month"].append(step_time_components[1])
        storm["day"].append(step_time_components[2])
        storm["hour"].append(step_time_components[3])

    for var in new_var:
        dvar = (new_var[var] - storm[var][-1]) / gap_length
        for gap_index in range(1, gap_length):
            var1 = storm[var][-1] + dvar
            storm[var].append(var1)


def _calculate_gap_time(cube, year, month, day, hour, time_period):
    """
    Calculate the date and time for the next interpolated time point.

    :param iris.cube.Cube cube: A cube loaded from a data file from the
        current period.
    :param int year: The year of the last time point.
    :param int month: The month of the last time point.
    :param int day: The day of the month of the last time point.
    :param int hour: The hour of the last time point.
    :param int time_period: The time period in hours between time points in the
        data.
    :returns: The year, month, day and hour of the interpolated time point.
    :rtype: tuple
    """

    calendar = cube.coord("time").units.calendar

    last_datetime = DATETIME_TYPES[calendar](year, month, day, hour)
    time_delta = datetime.timedelta(hours=time_period)
    this_datetime = last_datetime + time_delta
    this_datetime_tuple = (
        this_datetime.year,
        this_datetime.month,
        this_datetime.day,
        this_datetime.hour,
    )
    return this_datetime_tuple
