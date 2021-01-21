# (C) British Crown Copyright 2020, Met Office.
# Please see LICENSE for license details.


def make_loaded_trajectories():
    """
    Make sn example structure of trajectories as returned by
    `tempest_helper.get_trajectories()`.

    :returns: A simulated list of trajectories.
    :rtype: list
    """
    storms = []
    # Northern hemisphere
    storm = {}
    storm["length"] = 2  # 2 time points
    storm["lon"] = [1.0, 2.0]
    storm["lat"] = [10.0, 11.0]
    storm["year"] = [2014, 2014]
    storm["month"] = [12, 12]
    storm["day"] = [21, 21]
    storm["hour"] = [0, 6]
    storm["step"] = [1, 2]
    storm["slp"] = [100000.3, 99999.3]
    storm["sfcWind"] = [5.6, 8.5]
    storm["zg"] = [5090.2, 5125.3]
    storm["orog"] = [10.2, 0.0]
    storms.append(storm)
    # Southern hemisphere
    storm = {}
    storm["length"] = 2  # 2 time points
    storm["lon"] = [1.0, 2.0]
    storm["lat"] = [-1.0, 0.0]
    storm["year"] = [2014, 2014]
    storm["month"] = [12, 12]
    storm["day"] = [21, 21]
    storm["hour"] = [0, 6]
    storm["step"] = [1, 2]
    storm["slp"] = [100000.3, 99999.3]
    storm["sfcWind"] = [5.6, 8.5]
    storm["zg"] = [5090.2, 5125.3]
    storm["orog"] = [10.2, 0.0]
    storms.append(storm)
    # Northern hemisphere
    storm = {}
    storm["length"] = 2  # 2 time points in file
    storm["lon"] = [1.0, 1.5, 2.0]
    storm["lat"] = [0.0, 0.5, 1.0]
    storm["year"] = [2014, 2014, 2014]
    storm["month"] = [12, 12, 12]
    storm["day"] = [21, 21, 21]
    storm["hour"] = [0, 6, 12]
    storm["step"] = [1, 2, 3]
    storm["slp"] = [100000.3, 99999.3, 99995.1]
    storm["sfcWind"] = [5.6, 8.5, 10.2]
    storm["zg"] = [5090.2, 5125.3, 5100.4]
    storm["orog"] = [10.2, 0.0, 0.0]
    storms.append(storm)
    return storms
