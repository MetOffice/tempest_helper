# (C) British Crown Copyright 2020, Met Office.
# Please see LICENSE for license details.
import unittest

import cf_units
from iris.tests.stock import realistic_3d

from tempest_helper.trajectory_manipulations import (
    _calculate_gap_time,
    convert_date_to_step,
    fill_trajectory_gaps,
)


class TestConvertDateToStep(unittest.TestCase):
    """Test tempest_helper.trajectory_manipulations.convert_date_to_step"""

    def test_conversion(self):
        """Test standard conversion"""
        cube = realistic_3d()
        # realistic_3d()'s first time point is 2014-12-21 00:00:00
        actual = convert_date_to_step(cube, 2014, 12, 21, 0, 6)
        expected = 1
        self.assertEqual(expected, actual)

    def test_different_calendar(self):
        """Test a different calendar"""
        cube = realistic_3d()
        cal_360day = cf_units.Unit(
            "hours since 1970-01-01 00:00:00", calendar=cf_units.CALENDAR_360_DAY,
        )
        # realistic_3d() in 360_day starts at 2015-08-16 00:00:00
        cube.coord("time").units = cal_360day
        actual = convert_date_to_step(cube, 2015, 8, 16, 6, 6)
        expected = 2
        self.assertEqual(expected, actual)

    def test_different_period(self):
        """Test standard conversion"""
        cube = realistic_3d()
        # realistic_3d()'s first time point is 2014-12-21 00:00:00
        actual = convert_date_to_step(cube, 2014, 12, 22, 0, 12)
        expected = 3
        self.assertEqual(expected, actual)


class TestFillTrajectoryGaps(unittest.TestCase):
    """Test tempest_helper.trajectory_manipulations.fill_trajectory_gaps()"""

    def test_fill_traj_gap_increasing(self):
        """Test increasing latitude and longitude"""
        storm = {
            "length": 3,
            "step": [1, 2],
            "lat": ["0.0", "1.0"],
            "lon": ["0.0", "1.0"],
            "year": ["2000", "2000"],
            "month": ["1", "1"],
            "day": ["1", "1"],
            "hour": ["0", "6"],
        }
        expected = {
            "length": 3,
            "step": [1, 2, 3, 4, 5],
            "lat": ["0.0", "1.0", "2.0", "3.0", "4.0"],
            "lon": ["0.0", "1.0", "2.0", "3.0", "4.0"],
            "year": ["2000", "2000", "2000", "2000", "2000"],
            "month": ["1", "1", "1", "1", "1"],
            "day": ["1", "1", "1", "1", "2"],
            "hour": ["0", "6", "12", "18", "0"],
        }
        cube = realistic_3d()
        fill_trajectory_gaps(storm, 6, "5.0", "5.0", cube, 6)
        self.assertEqual(expected, storm)

    def test_fill_traj_gap_decreasing(self):
        """Test decreasing latitude and longitude"""
        storm = {
            "length": 3,
            "step": [1, 2],
            "lat": ["1.0", "0.0"],
            "lon": ["1.0", "0.0"],
            "year": ["2000", "2000"],
            "month": ["1", "1"],
            "day": ["1", "1"],
            "hour": ["0", "6"],
        }
        expected = {
            "length": 3,
            "step": [1, 2, 3, 4, 5],
            "lat": ["1.0", "0.0", "-1.0", "-2.0", "-3.0"],
            "lon": ["1.0", "0.0", "359.0", "358.0", "357.0"],
            "year": ["2000", "2000", "2000", "2000", "2000"],
            "month": ["1", "1", "1", "1", "1"],
            "day": ["1", "1", "1", "1", "2"],
            "hour": ["0", "6", "12", "18", "0"],
        }
        cube = realistic_3d()
        fill_trajectory_gaps(storm, 6, "356.0", "-4.0", cube, 6)
        self.assertEqual(expected, storm)

    def test_fill_traj_gap_different_directions(self):
        """Test increasing latitude and decreasing longitude"""
        storm = {
            "length": 3,
            "step": [1, 2],
            "lat": ["0.0", "1.0"],
            "lon": ["1.0", "0.0"],
            "year": ["2000", "2000"],
            "month": ["1", "1"],
            "day": ["1", "1"],
            "hour": ["0", "6"],
        }
        expected = {
            "length": 3,
            "step": [1, 2, 3, 4, 5],
            "lat": ["0.0", "1.0", "2.0", "3.0", "4.0"],
            "lon": ["1.0", "0.0", "359.0", "358.0", "357.0"],
            "year": ["2000", "2000", "2000", "2000", "2000"],
            "month": ["1", "1", "1", "1", "1"],
            "day": ["1", "1", "1", "1", "2"],
            "hour": ["0", "6", "12", "18", "0"],
        }
        cube = realistic_3d()
        fill_trajectory_gaps(storm, 6, "356.0", "5.0", cube, 6)
        self.assertEqual(expected, storm)

    def test_fill_traj_gap_non_integer(self):
        """
        Test increasing latitude and decreasing longitude with non-integer
        delta.
        """
        storm = {
            "length": 3,
            "step": [1, 2],
            "lat": ["0.0", "1.5"],
            "lon": ["1.0", "359.5"],
            "year": ["2000", "2000"],
            "month": ["1", "1"],
            "day": ["1", "1"],
            "hour": ["0", "6"],
        }
        expected = {
            "length": 3,
            "step": [1, 2, 3, 4, 5],
            "lat": ["0.0", "1.5", "3.0", "4.5", "6.0"],
            "lon": ["1.0", "359.5", "358.0", "356.5", "355.0"],
            "year": ["2000", "2000", "2000", "2000", "2000"],
            "month": ["1", "1", "1", "1", "1"],
            "day": ["1", "1", "1", "1", "2"],
            "hour": ["0", "6", "12", "18", "0"],
        }
        cube = realistic_3d()
        fill_trajectory_gaps(storm, 6, "353.5", "7.5", cube, 6)
        self.assertEqual(expected, storm)


class TestCalculateGapTime(unittest.TestCase):
    """Test tempest_helper.trajectory_manipulations._calculate_gap_time()"""

    def test_simple(self):
        """Basic test"""
        cube = realistic_3d()
        actual = _calculate_gap_time(cube, 1978, 7, 19, 6, 6)
        expected = ("1978", "7", "19", "12")
        self.assertEqual(expected, actual)

    def test_gregorian_over_leap_year(self):
        """Basic test"""
        cube = realistic_3d()
        actual = _calculate_gap_time(cube, 1978, 12, 31, 21, 4)
        expected = ("1979", "1", "1", "1")
        self.assertEqual(expected, actual)

    def test_360day_calendar(self):
        """Test a different calendar"""
        cube = realistic_3d()
        cal_360day = cf_units.Unit(
            "hours since 1970-01-01 00:00:00", calendar=cf_units.CALENDAR_360_DAY,
        )
        cube.coord("time").units = cal_360day
        actual = _calculate_gap_time(cube, 1978, 2, 29, 21, 12)
        expected = ("1978", "2", "30", "9")
        self.assertEqual(expected, actual)
