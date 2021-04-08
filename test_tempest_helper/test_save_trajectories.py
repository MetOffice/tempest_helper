# (C) British Crown Copyright 2021, Met Office.
# Please see LICENSE for license details.
import os
import tempfile

import numpy as np

from tempest_helper import save_trajectories_netcdf
from .utils import TempestHelperTestCase, make_loaded_trajectories


class TestSaveTrajectoriesNetcdf(TempestHelperTestCase):
    """Test tempest_helper.save_trajectories.save_trajectories_netcdf"""

    def setUp(self):
        # See an unlimited diff in case of error
        self.maxDiff = None
        # Make a track file
        storms = make_loaded_trajectories()
        _fd, self.track_file = tempfile.mkstemp(suffix=".nc")
        save_trajectories_netcdf(
            os.path.dirname(self.track_file),
            os.path.basename(self.track_file),
            storms,
            "360_day",
            "days since 1869-01-01 00:00:00",
            {},
            "6hr",
            "u-ax358",
            "N96",
            "wibble",
            "wobble",
            ["slp"],
        )

    def tearDown(self):
        os.remove(self.track_file)

    def test_everything_passes(self):
        expected_globals = """<class 'netCDF4._netCDF4.Dataset'>
root group (NETCDF4 data model, file format HDF5):
    title: Tempest TC tracks
    directory: /var/temp
    tracked_data_frequency: 6hr
    mo_runid: u-ax358
    grid: N96
    start_date: 
    end_date: 
    institution_id: MOHC
    algorithm: TempestExtremes_v2
    algorithm_ref: Ullrich and Zarzycki 2017; Zarzycki and Ullrich 2017; Ullrich et al. 2020
    detect_cmd: wibble
    stitch_cmd: wobble
    dimensions(sizes): tracks(3), record(6)
    variables(dimensions): int32 \x1b[4mFIRST_PT\x1b[0m(tracks), int32 \x1b[4mNUM_PTS\x1b[0m(tracks), int32 \x1b[4mTRACK_ID\x1b[0m(tracks), int32 \x1b[4mindex\x1b[0m(record), float64 \x1b[4mtime\x1b[0m(record), float32 \x1b[4mlon\x1b[0m(record), float32 \x1b[4mlat\x1b[0m(record), float64 \x1b[4mslp\x1b[0m(record)
    groups: 
"""
        expected_var_metedata = """OrderedDict([('FIRST_PT', <class 'netCDF4._netCDF4.Variable'>
int32 FIRST_PT(tracks)
    units: ordinal
    long_name: first_pt
    description: Index to first point of this track number
unlimited dimensions: 
current shape = (3,)
filling on, default _FillValue of -2147483647 used
), ('NUM_PTS', <class 'netCDF4._netCDF4.Variable'>
int32 NUM_PTS(tracks)
    units: ordinal
    long_name: num_pts
    description: Number of points for this track
unlimited dimensions: 
current shape = (3,)
filling on, default _FillValue of -2147483647 used
), ('TRACK_ID', <class 'netCDF4._netCDF4.Variable'>
int32 TRACK_ID(tracks)
    units: ordinal
    long_name: track_id
    description: Tropical cyclone track number
unlimited dimensions: 
current shape = (3,)
filling on, default _FillValue of -2147483647 used
), ('index', <class 'netCDF4._netCDF4.Variable'>
int32 index(record)
    units: ordinal
    long_name: track_id
    description: Track sequence number (0-length of track-1)
unlimited dimensions: 
current shape = (6,)
filling on, default _FillValue of -2147483647 used
), ('time', <class 'netCDF4._netCDF4.Variable'>
float64 time(record)
    units: days since 1869-01-01 00:00:00
    calendar: 360_day
    standard_name: time
    long_name: time
unlimited dimensions: 
current shape = (6,)
filling on, default _FillValue of 9.969209968386869e+36 used
), ('lon', <class 'netCDF4._netCDF4.Variable'>
float32 lon(record)
    units: degrees_east
    standard_name: longitude
    long_name: longitude
    description: Longitude (degrees east) associated with tracked variable
unlimited dimensions: 
current shape = (6,)
filling on, default _FillValue of 9.969209968386869e+36 used
), ('lat', <class 'netCDF4._netCDF4.Variable'>
float32 lat(record)
    units: degrees_north
    standard_name: latitude
    long_name: latitude
    description: Latitude (degrees north) associated with tracked variable
unlimited dimensions: 
current shape = (6,)
filling on, default _FillValue of 9.969209968386869e+36 used
), ('slp', <class 'netCDF4._netCDF4.Variable'>
float64 slp(record)
    standard_name: air_pressure_at_mean_sea_level
    long_name: Sea Level Pressure
    description: Sea level pressure for tracked variable
    units: Pa
unlimited dimensions: 
current shape = (6,)
filling on, default _FillValue of 9.969209968386869e+36 used
)])"""
        expected_var_values = [
            np.array([0, 2, 4]),
            np.array([2, 2, 2]),
            np.array([0, 1, 2]),
            np.array([0, 1, 0, 1, 0, 1]),
            np.array([52550.0, 52550.25, 52550.0, 52550.25, 52550.0, 52550.25]),
            np.array([1.0, 2.0, 1.0, 2.0, 1.0, 1.5]),
            np.array([10.0, 11.0, -1.0, 0.0, 0.0, 0.5]),
            np.array(
                [
                    9.997331e04,
                    9.978512e04,
                    9.997331e04,
                    9.978512e04,
                    9.997331e04,
                    9.9879215e04,
                ]
            ),
        ]

        self.assertNetcdfEqual(
            self.track_file,
            expected_globals,
            expected_var_metedata,
            expected_var_values,
        )
