# (C) British Crown Copyright 2022, Met Office.
# Please see LICENSE for license details.


def count_hemispheric_trajectories(storms):
    """
    From a loaded trajectory count the number of storms whose first point is
    in the southern hemisphere (latitude < 0.0) and those in the northern
    hemisphere (latitude >= 0.0).

    :param list storms: The storm trajectories loaded from TempestExtremes.
    :returns: Integer numbers of the trajectories in the southern and then
        northern hemispheres.
    :rtype: tuple
    """
    northern_found = 0
    southern_found = 0
    for storm in storms:
        lat = storm["lat"][0]
        if lat < 0.0:
            southern_found += 1
        else:
            northern_found += 1

    return southern_found, northern_found


def count_trajectories(storms):
    """
    From a loaded trajectory count the number of storms.

    :param list storms: The storm trajectories loaded from TempestExtremes.
    :returns: The number of trajectories.
    :rtype: int
    """
    return len(storms)
