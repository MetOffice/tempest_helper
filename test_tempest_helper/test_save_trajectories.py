# (C) British Crown Copyright 2021, Met Office.
# Please see LICENSE for license details.
import os
import tempfile

import numpy as np

from tempest_helper import save_trajectories_netcdf
from .utils import TempestHelperTestCase, make_loaded_trajectories, make_column_names


class TestSaveTrajectoriesNetcdf(TempestHelperTestCase):
    """Test tempest_helper.save_trajectories.save_trajectories_netcdf"""

    def setUp(self):
        # See an unlimited diff in case of error
        self.maxDiff = None
        # Make a track file
        storms = make_loaded_trajectories()
        column_names = make_column_names()
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
            column_names,
        )

    def tearDown(self):
        os.remove(self.track_file)

    def test_everything_passes(self):
        expected_globals = """<class 'netCDF4._netCDF4.Dataset'>
root group (NETCDF4 data model, file format HDF5):
    title: Tempest TC tracks
    directory: /var/tmp
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
    variables(dimensions): int32 FIRST_PT(tracks), int32 NUM_PTS(tracks), int32 TRACK_ID(tracks), int32 index(record), float64 time(record), float32 lon(record), float32 lat(record), float64 slp(record)
    groups: 
"""  # noqa
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
), ('slp_min', <class 'netCDF4._netCDF4.Variable'>
float64 slp_min(record)
    standard_name: air_pressure_at_mean_sea_level
    long_name: Sea Level Pressure
    description: Sea level pressure for tracked variable
    units: Pa
unlimited dimensions: 
current shape = (6,)
filling on, default _FillValue of 9.969209968386869e+36 used
), ('sfcWind_max', <class 'netCDF4._netCDF4.Variable'>
float64 sfcWind_max(record)
    standard_name: wind_speed
    long_name: Near-surface Wind Speed
    description: near-surface (usually 10 metres) wind speed
    units: m s-1
unlimited dimensions: 
current shape = (6,)
filling on, default _FillValue of 9.969209968386869e+36 used
), ('zg_avg_250', <class 'netCDF4._netCDF4.Variable'>
float64 zg_avg_250(record)
    standard_name: geopotential_height
    long_name: Geopotential Height
    description: Geopotential height difference
    units: m
unlimited dimensions: 
current shape = (6,)
filling on, default _FillValue of 9.969209968386869e+36 used
), ('orog_max', <class 'netCDF4._netCDF4.Variable'>
float64 orog_max(record)
    standard_name: surface_altitude
    long_name: Surface Altitude
    description: Surface altitude (height above sea level)
    units: m
unlimited dimensions: 
current shape = (6,)
filling on, default _FillValue of 9.969209968386869e+36 used
)])"""  # noqa
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
            np.array(
                [
                    1.206617e01,
                    1.079898e01,
                    1.206617e01,
                    1.079898e01,
                    1.206617e01,
                    1.1432575e01
                ]
            ),
            np.array(
                [
                    5.092293e03,
                    5.112520e03,
                    5.092293e03,
                    5.112520e03,
                    5.092293e03,
                    5.1024065e3
                ]
            ),
            np.array(
                [
                    0.000000e00,
                    0.000000e00,
                    0.000000e00,
                    0.000000e00,
                    0.000000e00,
                    0.000000e00
                ]
            ),
        ]

        self.assertNetcdfEqual(
            self.track_file,
            expected_globals,
            expected_var_metedata,
            expected_var_values,
        )
