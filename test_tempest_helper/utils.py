# (C) British Crown Copyright 2021, Met Office.
# Please see LICENSE for license details.
from math import isclose
from typing import Any, ClassVar, Dict, List, Optional
from unittest import TestCase

from netCDF4 import Dataset
import numpy as np


class TempestHelperTestCase(TestCase):
    """
    A subclass of :py:obj:`unittest.TestCase` that contains additional assertion
    methods to test complex data types.

    :cvar float rel_tol: relative tolerance for comparisons (default 1e-9)
    :cvar float abs_tol: absolute tolerance for comparisons (default 0.0)
    """

    rel_tol: ClassVar[float] = 1e-9
    abs_tol: ClassVar[float] = 0.0

    def assertNetcdfEqual(
        self,
        actual_path: str,
        expected_global: str,
        expected_variables_metadata: str,
        expected_variables_values: list,
        globals_ignore: Optional[List[str]] = ["directory"],
    ) -> None:
        """
        Load the netCDF file specified by `actual_path` and compare it against the
        attributes and values specified.

        The directory attribute in the netCDF file's global attributes is
        ignored by default but this can be changed by setting the `globals_ignore`
        attribute appropriately.

        :param str actual_path: The path of the netCDF file to test.
        :param str expected_global: The expected global attribute values as displayed
            by ``str(netCDF4.Dataset)`` except for any attributes that are specified
            in the `globals_ignore` parameter.
        :param str expected_variables_metadata: The expected variable attribute
            values as displayed by ``str(netCDF4.Dataset.variables)``.
        :param list expected_variables_values: List of :py:obj:`numpy.array` objects
            containing the data for each variable in the file.
        :param list globals_ignore: Global attributes to ignore.
        """
        # In netCDF4 prior to v1.5.2 variable names were underlined and the
        # control characters to do this must be removed before comparison.
        underline_code_1 = "\x1b[4m"
        underline_code_2 = "\x1b[0m"

        with Dataset(actual_path) as rootgroup:
            # Check globals
            for expected, actual in zip(
                expected_global.splitlines(),
                str(rootgroup)
                .replace(underline_code_1, "")
                .replace(underline_code_2, "")
                .splitlines(),
            ):
                ignore_line = False
                for ignore in globals_ignore:
                    if actual.lstrip().startswith(f"{ignore}:"):
                        ignore_line = True
                        continue
                if not ignore_line:
                    self.assertEqual(expected, actual, msg="Mismatch in globals")
            # Check variable metadata
            self.assertEqual(expected_variables_metadata, str(rootgroup.variables))
            # Check variable values
            var_values = [rootgroup[var_name][:] for var_name in rootgroup.variables]
            if len(expected_variables_values) != len(var_values):
                self.fail(
                    "Length of expected_variables_values does not match "
                    "actual length"
                )
            for expected, actual in zip(expected_variables_values, var_values):
                np.testing.assert_allclose(
                    expected, actual, rtol=self.rel_tol, atol=self.abs_tol
                )

    def assertTempestDictEqual(
        self, expected: Dict[Any, Any], actual: Dict[Any, Any]
    ) -> None:
        """
        Compare the dictionaries used in tempest_helper. Values can be ints,
        floats or lists of these two types; other types of value will fail.

        Class `TempestHelperTestCase` instance attributes
        `self.rel_tol` and `self.abs_tol` can be set in child
        instances to set the relative and absolute tolerance passed to
        `math.isclose()` to test all floats with.

        :param dict expected: The expected Tempest dictionary.
        :param dict actual: The actual Tempest dictionary.
        """
        expected_keys = sorted(list(expected.keys()))
        actual_keys = sorted(list(actual.keys()))
        if expected_keys != actual_keys:
            self.fail(f"Keys differ {expected_keys} != {actual_keys}")
        for key in expected_keys:
            if not isinstance(expected[key], type(actual[key])):
                self.fail(
                    f"{key} type {type(expected[key]).__name__} != "
                    f"{type(actual[key]).__name__}"
                )
            elif isinstance(expected[key], int):
                if not expected[key] == actual[key]:
                    self.fail(f"{key} {expected[key]} != {actual[key]}")
            elif isinstance(expected[key], float):
                if not isclose(
                    expected[key],
                    actual[key],
                    rel_tol=self.rel_tol,
                    abs_tol=self.abs_tol,
                ):
                    self.fail(
                        f"{key} is not close {expected[key]}, {actual[key]} "
                        f"with rel_tol={self.rel_tol} abs_tol={self.abs_tol}"
                    )
            elif isinstance(expected[key], list):
                if len(expected[key]) != len(actual[key]):
                    self.fail(
                        f"{key} length {len(expected[key])} != " f"{len(actual[key])}"
                    )
                for a, b in zip(expected[key], actual[key]):
                    if type(a) != type(b):
                        self.fail(f"{key} value type {a} != {b}")
                    elif isinstance(a, int):
                        if not a == b:
                            self.fail(f"{key} value {a} != {b}")
                    elif isinstance(b, float):
                        if not isclose(
                            a, b, rel_tol=self.rel_tol, abs_tol=self.abs_tol
                        ):
                            self.fail(
                                f"{key} value is not close {a} {b} "
                                f"with rel_tol={self.rel_tol} "
                                f"abs_tol={self.abs_tol}"
                            )
                    else:
                        self.fail(
                            f"{key} no test for value {a} type " f"{type(a).__name__}"
                        )
            else:
                self.fail(f"{key} no test for type {type(expected[key]).__name__}")


def make_loaded_trajectories():
    """
    Make an example structure of trajectories as returned by
    `tempest_helper.get_trajectories()`.

    :returns: A simulated list of trajectories.
    :rtype: list
    """
    storms = []
    # Northern hemisphere
    storm = {}
    storm["length"] = 2  # 2 time points
    storm["grid_x"] = [67, 68],
    storm["grid_y"] = [85, 86],
    storm["lon"] = [1.0, 2.0]
    storm["lat"] = [10.0, 11.0]
    storm["year"] = [2014, 2014]
    storm["month"] = [12, 12]
    storm["day"] = [21, 21]
    storm["hour"] = [0, 6]
    storm["step"] = [1, 2]
    storm["slp_min"] = [9.997331e04, 9.978512e04]
    storm["sfcWind_max"] = [1.206617e01, 1.079898e01]
    storm["zg_avg_250"] = [5.092293e03, 5.112520e03]
    storm["orog_max"] = [0.000000e00, 0.000000e00]
    storms.append(storm)
    # Southern hemisphere
    storm = {}
    storm["length"] = 2  # 2 time points
    storm["grid_x"] = [67, 68],
    storm["grid_y"] = [85, 86],
    storm["lon"] = [1.0, 2.0]
    storm["lat"] = [-1.0, 0.0]
    storm["year"] = [2014, 2014]
    storm["month"] = [12, 12]
    storm["day"] = [21, 21]
    storm["hour"] = [0, 6]
    storm["step"] = [1, 2]
    storm["slp_min"] = [9.997331e04, 9.978512e04]
    storm["sfcWind_max"] = [1.206617e01, 1.079898e01]
    storm["zg_avg_250"] = [5.092293e03, 5.112520e03]
    storm["orog_max"] = [0.000000e00, 0.000000e00]
    storms.append(storm)
    # Northern hemisphere
    storm = {}
    storm["length"] = 2  # 2 time points in file
    storm["grid_x"] = [67, 68, 69],
    storm["grid_y"] = [85, 86, 87],
    storm["lon"] = [1.0, 1.5, 2.0]
    storm["lat"] = [0.0, 0.5, 1.0]
    storm["year"] = [2014, 2014, 2014]
    storm["month"] = [12, 12, 12]
    storm["day"] = [21, 21, 21]
    storm["hour"] = [0, 6, 12]
    storm["step"] = [1, 2, 3]
    storm["slp_min"] = [9.997331e04, 9.9879215e04, 9.978512e04]
    storm["sfcWind_max"] = [1.206617e01, 1.1432575e01, 1.079898e01]
    storm["zg_avg_250"] = [5.092293e03, 5.1024065e3, 5.112520e03]
    storm["orog_max"] = [0.000000e00, 0.000000e00, 0.000000e00]
    storms.append(storm)
    return storms


def make_column_names():
    """
    Make an example column names dictionary for
    `tempest_helper.save_trajectories()`.

    :returns: A dict of column names and indices
    :rtype: dict
    """
    column_initial = "grid_x,grid_y,"
    column_final = ",year,month,day,hour"
    stitch_in_fmt = "lon,lat,slp_min,sfcWind_max,zg_avg_250,orog_max"
    col_names = column_initial + stitch_in_fmt + column_final
    names = col_names.split(',')
    column_names = {}
    for im, name in enumerate(names):
        column_names[name] = im
    return column_names
