# (C) British Crown Copyright 2020, Met Office.
# Please see LICENSE for license details.
import os
import shutil
import tempfile
import unittest

import iris
from iris.tests.stock import realistic_3d

from tempest_helper.load_trajectories import get_trajectories
from .utils import make_loaded_trajectories


class TestGetTrajectories(unittest.TestCase):
    """Test tempest_helper.load_trajectories.get_trajectories"""
    def setUp(self):
        # See an unlimited diff in case of error
        self.maxDiff = None
        # Create a directory for the input files
        self.runtime_dir = tempfile.mkdtemp()
        # Make a track file
        _fd, self.track_file = tempfile.mkstemp(suffix='.conf',
                                           dir=self.runtime_dir)
        track_file_contents = """start   2  2014    12   21   0  
    67  85  1.0  10.0   9.997331e+04    1.206617e+01    5.092293e+03    0.000000e+00    2014   12  21   0  
    66  86  2.0  11.0   9.978512e+04    1.079898e+01    5.112520e+03    0.000000e+00    2014   12  21   6
start   2  2014    12   21   0
    67  85  1.0  -1.0   9.997331e+04    1.206617e+01    5.092293e+03    0.000000e+00    2014   12  21   0  
    66  86  2.0  0.0   9.978512e+04    1.079898e+01    5.112520e+03    0.000000e+00    2014   12  21   6
start   2  2014    12   21   0
    67  85  1.0  0.0   9.997331e+04    1.206617e+01    5.092293e+03    0.000000e+00    2014   12  21   0  
    66  86  2.0  1.0   9.978512e+04    1.079898e+01    5.112520e+03    0.000000e+00    2014   12  21   12"""
        with open(self.track_file, 'w') as fh:
            fh.writelines([line.strip()+'\n'
                           for line in track_file_contents.split('\n')])

        # Make an example data file
        _fd, self.netcdf_file = tempfile.mkstemp(suffix='.nc',
                                                 dir=self.runtime_dir)
        cube = realistic_3d()
        iris.save(cube, self.netcdf_file)

    def tearDown(self):
        if os.path.isdir(self.runtime_dir):
            shutil.rmtree(self.runtime_dir, ignore_errors=True)

    def test_get_trajectories(self):
        expected = make_loaded_trajectories()
        actual = get_trajectories(self.track_file, self.netcdf_file, 6)
        self.assertEqual(expected, actual)