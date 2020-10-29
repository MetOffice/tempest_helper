# (C) British Crown Copyright 2020, Met Office.
# Please see LICENSE for license details.
import unittest

from tempest_helper.trajectory_manipulations import fill_trajectory_gaps


class TestFillTrajectoryGaps(unittest.TestCase):
    """Test tempest_helper.fill_trajectory_gaps()"""
    def test_fill_traj_gap_increasing(self):
        """Test TempestTracker.fill_traj_gap"""
        storm = {
            'length': 3,
            'step': [1, 2],
            'lat': ['0.0', '1.0'],
            'lon': ['0.0', '1.0'],
            'year': ['2000', '2000'],
            'month': ['1', '1'],
            'day': ['1', '1'],
            'hour': ['0', '6']
        }
        expected = {
            'length': 3,
            'step': [1, 2, 3, 4, 5],
            'lat': ['0.0', '1.0', '2.0', '3.0', '4.0'],
            'lon': ['0.0', '1.0', '2.0', '3.0', '4.0'],
            'year': ['2000', '2000', '2000', '2000', '2000'],
            'month': ['1', '1', '1', '1', '1'],
            'day': ['1', '1', '1', '1', '1'],
            'hour': ['0', '6', '18', '18', '18']
        }
        fill_trajectory_gaps(storm, 6, '5.0', '5.0', '2000', '1', '1', '18')
        self.assertEqual(expected, storm)

    def test_fill_traj_gap_decreasing(self):
        """Test TempestTracker.fill_traj_gap"""
        storm = {
            'length': 3,
            'step': [1, 2],
            'lat': ['1.0', '0.0'],
            'lon': ['1.0', '0.0'],
            'year': ['2000', '2000'],
            'month': ['1', '1'],
            'day': ['1', '1'],
            'hour': ['0', '6']
        }
        expected = {
            'length': 3,
            'step': [1, 2, 3, 4, 5],
            'lat': ['1.0', '0.0', '-1.0', '-2.0', '-3.0'],
            'lon': ['1.0', '0.0', '359.0', '358.0', '357.0'],
            'year': ['2000', '2000', '2000', '2000', '2000'],
            'month': ['1', '1', '1', '1', '1'],
            'day': ['1', '1', '1', '1', '1'],
            'hour': ['0', '6', '18', '18', '18']
        }
        fill_trajectory_gaps(storm, 6, '356.0', '-4.0', '2000', '1', '1', '18')
        self.assertEqual(expected, storm)

    def test_fill_traj_gap_different_directions(self):
        """Test TempestTracker.fill_traj_gap"""
        storm = {
            'length': 3,
            'step': [1, 2],
            'lat': ['0.0', '1.0'],
            'lon': ['1.0', '0.0'],
            'year': ['2000', '2000'],
            'month': ['1', '1'],
            'day': ['1', '1'],
            'hour': ['0', '6']
        }
        expected = {
            'length': 3,
            'step': [1, 2, 3, 4, 5],
            'lat': ['0.0', '1.0', '2.0', '3.0', '4.0'],
            'lon': ['1.0', '0.0', '359.0', '358.0', '357.0'],
            'year': ['2000', '2000', '2000', '2000', '2000'],
            'month': ['1', '1', '1', '1', '1'],
            'day': ['1', '1', '1', '1', '1'],
            'hour': ['0', '6', '18', '18', '18']
        }
        fill_trajectory_gaps(storm, 6, '356.0', '5.0', '2000', '1', '1', '18')
        self.assertEqual(expected, storm)

    def test_fill_traj_gap_non_integer(self):
        """Test TempestTracker.fill_traj_gap"""
        storm = {
            'length': 3,
            'step': [1, 2],
            'lat': ['0.0', '1.5'],
            'lon': ['1.0', '359.5'],
            'year': ['2000', '2000'],
            'month': ['1', '1'],
            'day': ['1', '1'],
            'hour': ['0', '6']
        }
        expected = {
            'length': 3,
            'step': [1, 2, 3, 4, 5],
            'lat': ['0.0', '1.5', '3.0', '4.5', '6.0'],
            'lon': ['1.0', '359.5', '358.0', '356.5', '355.0'],
            'year': ['2000', '2000', '2000', '2000', '2000'],
            'month': ['1', '1', '1', '1', '1'],
            'day': ['1', '1', '1', '1', '1'],
            'hour': ['0', '6', '18', '18', '18']
        }
        fill_trajectory_gaps(storm, 6, '353.5', '7.5', '2000', '1', '1', '18')
        self.assertEqual(expected, storm)
