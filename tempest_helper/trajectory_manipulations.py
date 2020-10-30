# (C) British Crown Copyright 2020, Met Office.
# Please see LICENSE for license details.
import cftime


def convert_date_to_step(cube, year, month, day, hour, time_period=6):
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
    calendar = cube.coord('time').units.calendar

    # cftime v1.0.0 doesn't allow a keyword to the datetime method to specify,
    # but this introduced in v1.2.0 and so will have to use the code below to
    # specify the type of datetime object to create
    datetime_types = {
        'noleap': cftime.DatetimeNoLeap,
        'all_leap': cftime.DatetimeAllLeap,
        '360_day': cftime.Datetime360Day,
        'julian': cftime.DatetimeJulian,
        'gregorian': cftime.DatetimeGregorian,
        'standard': cftime.DatetimeGregorian,
        'proleptic_gregorian': cftime.DatetimeProlepticGregorian
    }

    current_datetime = datetime_types[calendar](year, month, day, hour)
    first_point = cube.coord('time').units.num2date(
        cube.coord('time').points[0]
    )
    time_delta = current_datetime - first_point
    seconds_in_hour = 60**2
    return round(time_delta.total_seconds() /
                 (time_period * seconds_in_hour)) + 1


def fill_trajectory_gaps(storm, step, lon, lat, year, month, day, hour):
    """
    Fill the gap by linearly interpolating the latitude, longitude and adding
    steps. The trajectory is passed in to the `storm` attribute and is a
    standard `tempest_helper` dictionary. The date and time is not interpolated
    and the end time is inserted for the interpolated steps. Longitudes and
    their interpolation may wrap around the 0/360 degree numerical
    discontinuity. The longitudes output are between 0 and 359 degrees.

    :param dict storm: Details of the current storm.
    :param int step: The integer number of time points of the current
        point since the time unit's epoch.
    :param str lon: The longitude of the current point in the storm in
        degrees.
    :param str lat: The latitude of the current point in the storm in
        degrees.
    :param str year: Year of the current time point.
    :param str month: Month of the current time point.
    :param str day: Day of the current time point.
    :param str hour: Hour of the current time point.
    """
    gap_length = step - storm['step'][-1]
    # Using technique at https://stackoverflow.com/a/14498790 to handle
    # longitudes wrapping around 0/360
    dlon = ((((float(lon) - float(storm['lon'][-1])) + 180) % 360 - 180) /
            gap_length)
    dlat = (float(lat) - float(storm['lat'][-1])) / gap_length
    for gap_index in range(1, gap_length):
        lon1 = (float(storm['lon'][-1]) + dlon) % 360
        lat1 = float(storm['lat'][-1]) + dlat
        storm['lon'].append(str(lon1))
        storm['lat'].append(str(lat1))
        storm['step'].append(storm['step'][-1] + 1)
        storm['year'].append(year)
        storm['month'].append(month)
        storm['day'].append(day)
        storm['hour'].append(hour)
