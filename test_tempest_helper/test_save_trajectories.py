# (C) British Crown Copyright 2022, Met Office.
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
        print("column_names ", column_names)
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
        print("written nc file ", self.track_file)
        print("os_stat ", os.stat(self.track_file))

    def tearDown(self):
        os.remove(self.track_file)

    def test_everything_passes(self):
        expected_cdl = """netcdf test_nc {
dimensions:
	tracks = 3 ;
	record = 6 ;
variables:
	int FIRST_PT(tracks) ;
		FIRST_PT:units = "ordinal" ;
		FIRST_PT:long_name = "first_pt" ;
		FIRST_PT:description = "Index to first point of this track number" ;
		FIRST_PT:_Storage = "contiguous" ;
		FIRST_PT:_Endianness = "little" ;
	int NUM_PTS(tracks) ;
		NUM_PTS:units = "ordinal" ;
		NUM_PTS:long_name = "num_pts" ;
		NUM_PTS:description = "Number of points for this track" ;
		NUM_PTS:_Storage = "contiguous" ;
		NUM_PTS:_Endianness = "little" ;
	int TRACK_ID(tracks) ;
		TRACK_ID:units = "ordinal" ;
		TRACK_ID:long_name = "track_id" ;
		TRACK_ID:description = "Tropical cyclone track number" ;
		TRACK_ID:_Storage = "contiguous" ;
		TRACK_ID:_Endianness = "little" ;
	int index(record) ;
		index:units = "ordinal" ;
		index:long_name = "track_id" ;
		index:description = "Track sequence number (0 - length of track-1)" ;
		index:_Storage = "contiguous" ;
		index:_Endianness = "little" ;
	double time(record) ;
		time:units = "days since 1869-01-01 00:00:00" ;
		time:calendar = "360_day" ;
		time:standard_name = "time" ;
		time:long_name = "time" ;
		time:_Storage = "contiguous" ;
		time:_Endianness = "little" ;
	float lon(record) ;
		lon:units = "degrees_east" ;
		lon:standard_name = "longitude" ;
		lon:long_name = "longitude" ;
		lon:description = "Longitude (degrees east) associated with tracked variable" ;
		lon:_Storage = "contiguous" ;
		lon:_Endianness = "little" ;
	float lat(record) ;
		lat:units = "degrees_north" ;
		lat:standard_name = "latitude" ;
		lat:long_name = "latitude" ;
		lat:description = "Latitude (degrees north) associated with tracked variable" ;
		lat:_Storage = "contiguous" ;
		lat:_Endianness = "little" ;
	double slp_min(record) ;
		slp_min:standard_name = "air_pressure_at_mean_sea_level" ;
		slp_min:long_name = "Sea Level Pressure" ;
		slp_min:description = "Sea level pressure for tracked variable" ;
		slp_min:units = "Pa" ;
		slp_min:_Storage = "contiguous" ;
		slp_min:_Endianness = "little" ;
	double sfcWind_max(record) ;
		sfcWind_max:standard_name = "wind_speed" ;
		sfcWind_max:long_name = "Near-surface Wind Speed" ;
		sfcWind_max:description = "near-surface (usually 10 metres) wind speed" ;
		sfcWind_max:units = "m s-1" ;
		sfcWind_max:_Storage = "contiguous" ;
		sfcWind_max:_Endianness = "little" ;
	double zg_avg_250(record) ;
		zg_avg_250:standard_name = "geopotential_height" ;
		zg_avg_250:long_name = "Geopotential Height" ;
		zg_avg_250:description = "Geopotential height difference" ;
		zg_avg_250:units = "m" ;
		zg_avg_250:_Storage = "contiguous" ;
		zg_avg_250:_Endianness = "little" ;
	double orog_max(record) ;
		orog_max:standard_name = "surface_altitude" ;
		orog_max:long_name = "Surface Altitude" ;
		orog_max:description = "Surface altitude (height above sea level)" ;
		orog_max:units = "m" ;
		orog_max:_Storage = "contiguous" ;
		orog_max:_Endianness = "little" ;

// global attributes:
		:title = "Tempest TC tracks" ;
		:directory = "/var/tmp" ;
		:tracked_data_frequency = "6hr" ;
		:mo_runid = "u-ax358" ;
		:grid = "N96" ;
		:start_date = "" ;
		:end_date = "" ;
		:institution_id = "MOHC" ;
		:algorithm = "TempestExtremes_v2" ;
		:algorithm_ref = "Ullrich and Zarzycki 2017; Zarzycki and Ullrich 2017; Ullrich et al. 2020" ;
		:detect_cmd = "wibble" ;
		:stitch_cmd = "wobble" ;
		:_NCProperties = "version=2,netcdf=4.8.1,hdf5=1.12.1" ;
		:_SuperblockVersion = 2 ;
		:_IsNetcdf4 = 1 ;
		:_Format = "netCDF-4" ;
data:

 FIRST_PT = 0, 2, 4 ;

 NUM_PTS = 2, 2, 2 ;

 TRACK_ID = 0, 1, 2 ;

 index = 0, 1, 0, 1, 0, 1 ;

 time = 52550, 52550.25, 52550, 52550.25, 52550, 52550.25 ;

 lon = 1, 2, 1, 2, 1, 1.5 ;

 lat = 10, 11, -1, 0, 0, 0.5 ;

 slp_min = 99973.31, 99785.12, 99973.31, 99785.12, 99973.31, 99879.215 ;

 sfcWind_max = 12.06617, 10.79898, 12.06617, 10.79898, 12.06617, 11.432575 ;

 zg_avg_250 = 5092.293, 5112.52, 5092.293, 5112.52, 5092.293, 5102.4065 ;

 orog_max = 0, 0, 0, 0, 0, 0 ;
}
"""  # noqa
        self.assertNetcdfEqual(self.track_file, expected_cdl)
