# (C) British Crown Copyright 2022, Met Office.
# Please see LICENSE for license details.
import os
import tempfile

import cf_units
from iris.tests.stock import realistic_3d


from .utils import make_column_names, TempestHelperTestCase
from tempest_helper.trajectory_manipulations import (
    _calculate_gap_time,
    convert_date_to_step,
    fill_trajectory_gaps,
    storms_overlap_in_time,
    storms_overlap_in_space,
    write_track_line,
    rewrite_track_file,
)


class TestConvertDateToStep(TempestHelperTestCase):
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
            "hours since 1970-01-01 00:00:00",
            calendar=cf_units.CALENDAR_360_DAY,
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


class TestFillTrajectoryGaps(TempestHelperTestCase):
    """Test tempest_helper.trajectory_manipulations.fill_trajectory_gaps()"""

    def test_fill_traj_gap_increasing(self):
        """Test increasing latitude and longitude"""
        storm = {
            "length": 3,
            "step": [1, 2],
            "grid_y": [0, 2],
            "grid_x": [0, 2],
            "lat": [0.0, 1.0],
            "lon": [0.0, 1.0],
            "year": [2000, 2000],
            "month": [1, 1],
            "day": [1, 1],
            "hour": [0, 6],
            "slp_min": [100000.0, 99999.0],
            "sfcWind_max": [5.5, 5.7],
            "zg_avg_250": [5090.0, 5091.0],
            "orog_max": [10.0, 8.0],
        }
        expected = {
            "length": 3,
            "step": [1, 2, 3, 4, 5],
            "grid_y": [0, 2, 4, 6, 8],
            "grid_x": [0, 2, 4, 6, 8],
            "lat": [0.0, 1.0, 2.0, 3.0, 4.0],
            "lon": [0.0, 1.0, 2.0, 3.0, 4.0],
            "year": [2000, 2000, 2000, 2000, 2000],
            "month": [1, 1, 1, 1, 1],
            "day": [1, 1, 1, 1, 2],
            "hour": [0, 6, 12, 18, 0],
            "slp_min": [100000.0, 99999.0, 99998.0, 99997.0, 99996.0],
            "sfcWind_max": [5.5, 5.7, 5.9, 6.1, 6.3],
            "zg_avg_250": [5090.0, 5091.0, 5092.0, 5093.0, 5094.0],
            "orog_max": [10.0, 8.0, 6.0, 4.0, 2.0],
        }
        cube = realistic_3d()
        new_var = {
            "slp_min": 99995.0,
            "sfcWind_max": 6.5,
            "zg_avg_250": 5095.0,
            "orog_max": 0.0,
        }
        fill_trajectory_gaps(storm, 6, 5.0, 5.0, 10, 10, cube, 6, new_var)
        self.assertTempestDictEqual(expected, storm)

    def test_fill_traj_gap_decreasing(self):
        """Test decreasing latitude and longitude"""
        storm = {
            "length": 3,
            "step": [1, 2],
            "grid_y": [5, 4],
            "grid_x": [6, 5],
            "lat": [1.0, 0.0],
            "lon": [1.0, 0.0],
            "year": [2000, 2000],
            "month": [1, 1],
            "day": [1, 1],
            "hour": [0, 6],
            "slp_min": [100000.0, 99999.0],
            "sfcWind_max": [5.5, 5.7],
            "zg_avg_250": [5090.0, 5091.0],
            "orog_max": [10.0, 8.0],
        }
        expected = {
            "length": 3,
            "step": [1, 2, 3, 4, 5],
            "grid_y": [5, 4, 3, 2, 1],
            "grid_x": [6, 5, 4, 3, 2],
            "lat": [1.0, 0.0, -1.0, -2.0, -3.0],
            "lon": [1.0, 0.0, 359.0, 358.0, 357.0],
            "year": [2000, 2000, 2000, 2000, 2000],
            "month": [1, 1, 1, 1, 1],
            "day": [1, 1, 1, 1, 2],
            "hour": [0, 6, 12, 18, 0],
            "slp_min": [100000.0, 99999.0, 99998.0, 99997.0, 99996.0],
            "sfcWind_max": [5.5, 5.7, 5.9, 6.1, 6.3],
            "zg_avg_250": [5090.0, 5091.0, 5092.0, 5093.0, 5094.0],
            "orog_max": [10.0, 8.0, 6.0, 4.0, 2.0],
        }
        cube = realistic_3d()
        new_var = {
            "slp_min": 99995.0,
            "sfcWind_max": 6.5,
            "zg_avg_250": 5095.0,
            "orog_max": 0.0,
        }
        fill_trajectory_gaps(storm, 6, 356.0, -4.0, 1, 0, cube, 6, new_var)
        self.assertTempestDictEqual(expected, storm)

    def test_fill_traj_gap_different_directions(self):
        """Test increasing latitude and decreasing longitude"""
        storm = {
            "length": 3,
            "step": [1, 2],
            "grid_y": [4, 5],
            "grid_x": [6, 5],
            "lat": [0.0, 1.0],
            "lon": [1.0, 0.0],
            "year": [2000, 2000],
            "month": [1, 1],
            "day": [1, 1],
            "hour": [0, 6],
            "slp_min": [100000.0, 99999.0],
            "sfcWind_max": [5.5, 5.7],
            "zg_avg_250": [5090.0, 5091.0],
            "orog_max": [10.0, 8.0],
        }
        expected = {
            "length": 3,
            "step": [1, 2, 3, 4, 5],
            "grid_y": [4, 5, 6, 7, 8],
            "grid_x": [6, 5, 4, 3, 2],
            "lat": [0.0, 1.0, 2.0, 3.0, 4.0],
            "lon": [1.0, 0.0, 359.0, 358.0, 357.0],
            "year": [2000, 2000, 2000, 2000, 2000],
            "month": [1, 1, 1, 1, 1],
            "day": [1, 1, 1, 1, 2],
            "hour": [0, 6, 12, 18, 0],
            "slp_min": [100000.0, 99999.0, 99998.0, 99997.0, 99996.0],
            "sfcWind_max": [5.5, 5.7, 5.9, 6.1, 6.3],
            "zg_avg_250": [5090.0, 5091.0, 5092.0, 5093.0, 5094.0],
            "orog_max": [10.0, 8.0, 6.0, 4.0, 2.0],
        }
        cube = realistic_3d()
        new_var = {
            "slp_min": 99995.0,
            "sfcWind_max": 6.5,
            "zg_avg_250": 5095.0,
            "orog_max": 0.0,
        }
        fill_trajectory_gaps(storm, 6, 356.0, 5.0, 1, 9, cube, 6, new_var)
        self.assertTempestDictEqual(expected, storm)

    def test_fill_traj_gap_non_integer(self):
        """
        Test increasing latitude and decreasing longitude with non-integer
        delta.
        """
        storm = {
            "length": 3,
            "step": [1, 2],
            "grid_y": [4, 5],
            "grid_x": [5, 3],
            "lat": [0.0, 1.5],
            "lon": [1.0, 359.5],
            "year": [2000, 2000],
            "month": [1, 1],
            "day": [1, 1],
            "hour": [0, 6],
            "slp_min": [100000.0, 99999.0],
            "sfcWind_max": [5.5, 5.7],
            "zg_avg_250": [5090.0, 5091.0],
            "orog_max": [10.0, 8.0],
        }
        expected = {
            "length": 3,
            "step": [1, 2, 3, 4, 5],
            "grid_y": [4, 5, 6, 7, 8],
            "grid_x": [5, 3, 4, 5, 6],
            "lat": [0.0, 1.5, 3.0, 4.5, 6.0],
            "lon": [1.0, 359.5, 358.0, 356.5, 355.0],
            "year": [2000, 2000, 2000, 2000, 2000],
            "month": [1, 1, 1, 1, 1],
            "day": [1, 1, 1, 1, 2],
            "hour": [0, 6, 12, 18, 0],
            "slp_min": [100000.0, 99999.0, 99998.0, 99997.0, 99996.0],
            "sfcWind_max": [5.5, 5.7, 5.9, 6.1, 6.3],
            "zg_avg_250": [5090.0, 5091.0, 5092.0, 5093.0, 5094.0],
            "orog_max": [10.0, 8.0, 6.0, 4.0, 2.0],
        }
        cube = realistic_3d()
        new_var = {
            "slp_min": 99995.0,
            "sfcWind_max": 6.5,
            "zg_avg_250": 5095.0,
            "orog_max": 0.0,
        }
        fill_trajectory_gaps(storm, 6, 353.5, 7.5, 10, 12, cube, 6, new_var)
        self.assertTempestDictEqual(expected, storm)


class TestCalculateGapTime(TempestHelperTestCase):
    """Test tempest_helper.trajectory_manipulations._calculate_gap_time()"""

    def test_simple(self):
        """Basic test"""
        cube = realistic_3d()
        actual = _calculate_gap_time(cube, 1978, 7, 19, 6, 6)
        expected = (1978, 7, 19, 12)
        self.assertEqual(expected, actual)

    def test_gregorian_over_leap_year(self):
        """Basic test"""
        cube = realistic_3d()
        actual = _calculate_gap_time(cube, 1978, 12, 31, 21, 4)
        expected = (1979, 1, 1, 1)
        self.assertEqual(expected, actual)

    def test_360day_calendar(self):
        """Test a different calendar"""
        cube = realistic_3d()
        cal_360day = cf_units.Unit(
            "hours since 1970-01-01 00:00:00",
            calendar=cf_units.CALENDAR_360_DAY,
        )
        cube.coord("time").units = cal_360day
        actual = _calculate_gap_time(cube, 1978, 2, 29, 21, 12)
        expected = (1978, 2, 30, 9)
        self.assertEqual(expected, actual)


class TestStormsOverlapInTime(TempestHelperTestCase):
    """Test tempest_helper.trajectory_manipulations.storms_overlap_in_time()"""

    def test_simple(self):
        """Basic test"""
        storm = {
            "length": 3,
            "step": [1, 2, 3],
            "grid_y": [0, 2, 4],
            "grid_x": [0, 2, 4],
            "lat": [0.0, 1.0, 2.0],
            "lon": [0.0, 1.0, 2.0],
            "year": [2000, 2000, 2000],
            "month": [1, 1, 1],
            "day": [1, 1, 1],
            "hour": [0, 6, 12],
            "slp_min": [100000.0, 99999.0, 99998.0],
            "sfcWind_max": [5.5, 5.7, 5.9],
            "zg_avg_250": [5090.0, 5091.0, 5092.0],
            "orog_max": [10.0, 8.0, 6.0],
        }
        # Some storms that do and don't overlap with the above storm in time
        storm1 = {
            "length": 2,
            "step": [1, 2],
            "grid_y": [1, 3],
            "grid_x": [1, 3],
            "lat": [2.0, 3.0],
            "lon": [2.0, 3.0],
            "year": [2000, 2000],
            "month": [1, 1],
            "day": [1, 1],
            "hour": [6, 12],
            "slp_min": [100000.0, 99999.0],
            "sfcWind_max": [5.5, 5.7],
            "zg_avg_250": [5090.0, 5091.0],
            "orog_max": [10.0, 8.0],
        }
        storm2 = {
            "length": 2,
            "step": [1, 2],
            "grid_y": [1, 3],
            "grid_x": [1, 3],
            "lat": [2.0, 3.0],
            "lon": [2.0, 3.0],
            "year": [2000, 2000],
            "month": [1, 1],
            "day": [1, 2],
            "hour": [18, 0],
            "slp_min": [100000.0, 99999.0],
            "sfcWind_max": [5.5, 5.7],
            "zg_avg_250": [5090.0, 5091.0],
            "orog_max": [10.0, 8.0],
        }
        storms = [storm1, storm2]

        # The storms that are expected in the final output (i.e. just the overlapping storms)
        expected_storms = [storm1]

        # Now test the overlap
        actual = storms_overlap_in_time(storm, storms)
        for exp_storm, act_storm in zip(expected_storms, actual):
            self.assertTempestDictEqual(exp_storm, act_storm)


class TestStormsOverlapInSpace(TempestHelperTestCase):
    """Test tempest_helper.trajectory_manipulations.storms_overlap_in_space()"""

    def test_simple(self):
        """Basic test"""
        storm = {
            "length": 3,
            "step": [1, 2, 3],
            "grid_y": [0, 2, 4],
            "grid_x": [0, 2, 4],
            "lat": [0.0, 1.0, 2.0],
            "lon": [0.0, 1.0, 2.0],
            "year": [2000, 2000, 2000],
            "month": [1, 1, 1],
            "day": [1, 1, 1],
            "hour": [6, 12, 18],
            "slp_min": [100000.0, 99999.0, 99998.0],
            "sfcWind_max": [5.5, 5.7, 5.9],
            "zg_avg_250": [5090.0, 5091.0, 5092.0],
            "orog_max": [10.0, 8.0, 6.0],
        }
        # Example storms that do and do not overlap in time/space
        storm1 = {
            "length": 2,
            "step": [1, 2],
            "grid_y": [0, 2],
            "grid_x": [0, 2],
            "lat": [0.0, 1.0],
            "lon": [0.0, 1.0],
            "year": [2000, 2000],
            "month": [1, 1],
            "day": [1, 1],
            "hour": [6, 12],
            "slp_min": [100000.0, 99999.0],
            "sfcWind_max": [5.5, 5.7],
            "zg_avg_250": [5090.0, 5091.0],
            "orog_max": [8.0, 6.0],
        }
        storm2 = {
            "length": 2,
            "step": [1, 2],
            "grid_y": [1, 3],
            "grid_x": [1, 3],
            "lat": [2.0, 3.0],
            "lon": [2.0, 3.0],
            "year": [2000, 2000],
            "month": [1, 1],
            "day": [1, 1],
            "hour": [0, 6],
            "slp_min": [100000.0, 99999.0],
            "sfcWind_max": [5.5, 5.7],
            "zg_avg_250": [5090.0, 5091.0],
            "orog_max": [10.0, 8.0],
        }
        storm3 = {
            "length": 2,
            "step": [0, 1],
            "grid_y": [1, 0],
            "grid_x": [1, 0],
            "lat": [-1.0, 0.0],
            "lon": [-1.0, 0.0],
            "year": [2000, 2000],
            "month": [1, 1],
            "day": [1, 1],
            "hour": [0, 6],
            "slp_min": [100000.0, 999990.0],
            "sfcWind_max": [5.5, 5.7],
            "zg_avg_250": [5090.0, 5091.0],
            "orog_max": [10.0, 8.0],
        }
        # Test for one storm being subset of another
        storms = [storm1, storm2]
        expected_storms = {'early': storm1, 'late': storm, 'time_c': 0, 'time_p': 0, 'offset': 0, 'method': 'remove'}
        actual = storms_overlap_in_space(storm, storms)
        print('actual ',actual)
        self.assertTempestDictSubdictEqual(expected_storms, actual)

        # Test for one storm extending another
        storms = [storm2, storm3]
        expected_storms = {'early': storm3, 'late': storm, 'time_c': 0, 'time_p': 1, 'offset': 1, 'method': 'extend'}
        actual = storms_overlap_in_space(storm, storms)
        print('actual ', actual)
        self.assertTempestDictSubdictEqual(expected_storms, actual)


class TestWriteTrackLine(TempestHelperTestCase):
    """Test tempest_helper.trajectory_manipulations.write_track_line()"""

    def test_simple(self):
        """Basic test"""
        storm = {
            "length": 3,
            "step": [1, 2],
            "grid_y": [0, 2],
            "grid_x": [0, 2],
            "lat": [0.0, 1.0],
            "lon": [0.0, 1.0],
            "year": [2000, 2000],
            "month": [1, 1],
            "day": [1, 1],
            "hour": [0, 6],
            "slp_min": [100000.0, 99999.0],
            "sfcWind_max": [5.5, 5.7],
            "zg_avg_250": [5090.0, 5091.0],
            "orog_max": [10.0, 8.0],
        }
        # TODO add the expected string and list output below
        exp_str = """multiline text here"""
        exp_list = []
        act_str, act_list = write_track_line(storm, 1, 1, make_column_names())
        self.assertEqual(exp_str, act_str)
        self.assertEqual(exp_list, act_list)


class TestRewriteTrackFile(TempestHelperTestCase):
    """Test tempest_helper.trajectory_manipulations.rewrite_track_file()"""

    def setUp(self):
        # See an unlimited diff in case of error
        self.maxDiff = None
        # Create temporary files
        _fd, self.tracked_file_Tm1 = tempfile.mkstemp(suffix=".txt")
        _fd, self.tracked_file_T = tempfile.mkstemp(suffix=".txt")
        _fd, self.tracked_file_Tm1_adjust = tempfile.mkstemp(suffix=".txt")
        _fd, self.tracked_file_T_adjust = tempfile.mkstemp(suffix=".txt")

    def tearDown(self):
        # Remove the temporary files
        os.remove(self.tracked_file_Tm1)
        os.remove(self.tracked_file_T)
        os.remove(self.tracked_file_Tm1_adjust)
        os.remove(self.tracked_file_T_adjust)

    def test_simple(self):
        # TODO add text for input files here
        tm1 = """multiline text here"""
        t = """multiline text here"""
        with open(self.tracked_file_Tm1, "w") as fh:
            fh.write(tm1)
        with open(self.tracked_file_T, "w") as fh:
            fh.write(t)

        # TODO add expected text for generated files here
        exp_tm1 = """multiline text here"""
        exp_t = """multiline text here"""

        # TODO write the storms that are required in the adjusted files
        storms_match = []

        # Rewrite the files
        rewrite_track_file(
            self.tracked_file_Tm1,
            self.tracked_file_T,
            self.tracked_file_Tm1_adjust,
            self.tracked_file_T_adjust,
            storms_match,
            make_column_names(),
        )

        # Read the adjusted file contents from the files
        with open(self.tracked_file_Tm1_adjust) as fh:
            act_tm1 = fh.read()
        with open(self.tracked_file_T_adjust) as fh:
            act_t = fh.read()

        self.assertEqual(exp_tm1, act_tm1)
        self.assertEqual(exp_t, act_t)
