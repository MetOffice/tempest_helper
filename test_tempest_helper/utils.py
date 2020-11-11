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
    storm['length'] = 2  # 2 time points
    storm['lon'] = ['1.0', '2.0']
    storm['lat'] = ['10.0', '11.0']
    storm['year'] = ['2014', '2014']
    storm['month'] = ['12', '12']
    storm['day'] = ['21', '21']
    storm['hour'] = ['0', '6']
    storm['step'] = [1, 2]
    storms.append(storm)
    # Southern hemisphere
    storm = {}
    storm['length'] = 2  # 2 time points
    storm['lon'] = ['1.0', '2.0']
    storm['lat'] = ['-1.0', '0.0']
    storm['year'] = ['2014', '2014']
    storm['month'] = ['12', '12']
    storm['day'] = ['21', '21']
    storm['hour'] = ['0', '6']
    storm['step'] = [1, 2]
    storms.append(storm)
    # Northern hemisphere
    storm = {}
    storm['length'] = 2  # 2 time points in file
    storm['lon'] = ['1.0', '1.5', '2.0']
    storm['lat'] = ['0.0', '0.5', '1.0']
    storm['year'] = ['2014', '2014', '2014']
    storm['month'] = ['12', '12', '12']
    storm['day'] = ['21', '21', '21']
    storm['hour'] = ['0', '6', '12']
    storm['step'] = [1, 2, 3]
    storms.append(storm)
    return storms
