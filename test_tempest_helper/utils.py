# (C) British Crown Copyright 2021, Met Office.
# Please see LICENSE for license details.
from math import isclose
import re
import subprocess
from typing import Any, ClassVar, Dict, List, Optional
from unittest import TestCase

# Earlier versions of netCDF4 (prior to 1.5.6 didn't include the tocdl() method
import netCDF4

if not hasattr(netCDF4.Dataset, "tocdl"):

    class Dataset(netCDF4.Dataset):
        def tocdl(self, coordvars=False, data=False, outfile=None):
            self.sync()
            if coordvars:
                ncdumpargs = "-cs"
            else:
                ncdumpargs = "-s"
            if not data:
                ncdumpargs += "h"
            result = subprocess.run(
                ["ncdump", ncdumpargs, self.filepath()],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                encoding="utf-8",
            )
            if outfile is None:
                return result.stdout
            else:
                f = open(outfile, "w")
                f.write(result.stdout)
                f.close()

else:
    from netCDF4 import Dataset  # noqa


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
        expected_cdl: str,
        globals_ignore: Optional[List[str]] = [
            "directory",
            "_NCProperties",
            "_SuperblockVersion",
            r"netcdf.*{",
        ],
    ) -> None:
        """
        Load the netCDF file specified by `actual_path` and compare it against the
        specified netCDF CDL representation of the file, metadata and contents.

        The initial name line, and the directory, _SuperblockVersion and _NCProperties
        attributes are ignored by default but this can be changed by setting the
        `globals_ignore` attribute appropriately.

        :param str actual_path: The path of the netCDF file to test.
        :param str expected_cdl: The expected netCDF cdl for the file as displayed
            by the ncdump program.
        :param list globals_ignore: lines including these regular expressions to ignore.
        """

        with Dataset(actual_path) as rootgroup:
            for expected, actual in zip(
                expected_cdl.splitlines(),
                rootgroup.tocdl(data=True).splitlines(),
            ):
                ignore_line = False
                for ignore in globals_ignore:
                    if re.search(ignore, expected):
                        ignore_line = True
                        continue
                if not ignore_line:
                    self.assertEqual(expected, actual, msg="Mismatch in CDL")

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
    Make sn example structure of trajectories as returned by
    `tempest_helper.get_trajectories()`.

    :returns: A simulated list of trajectories.
    :rtype: list
    """
    storms = []
    # Northern hemisphere
    storm = {}
    storm["length"] = 2  # 2 time points
    storm["lon"] = [1.0, 2.0]
    storm["lat"] = [10.0, 11.0]
    storm["year"] = [2014, 2014]
    storm["month"] = [12, 12]
    storm["day"] = [21, 21]
    storm["hour"] = [0, 6]
    storm["step"] = [1, 2]
    storm["slp"] = [9.997331e04, 9.978512e04]
    storm["sfcWind"] = [1.206617e01, 1.079898e01]
    storm["zg"] = [5.092293e03, 5.112520e03]
    storm["orog"] = [0.000000e00, 0.000000e00]
    storms.append(storm)
    # Southern hemisphere
    storm = {}
    storm["length"] = 2  # 2 time points
    storm["lon"] = [1.0, 2.0]
    storm["lat"] = [-1.0, 0.0]
    storm["year"] = [2014, 2014]
    storm["month"] = [12, 12]
    storm["day"] = [21, 21]
    storm["hour"] = [0, 6]
    storm["step"] = [1, 2]
    storm["slp"] = [9.997331e04, 9.978512e04]
    storm["sfcWind"] = [1.206617e01, 1.079898e01]
    storm["zg"] = [5.092293e03, 5.112520e03]
    storm["orog"] = [0.000000e00, 0.000000e00]
    storms.append(storm)
    # Northern hemisphere
    storm = {}
    storm["length"] = 2  # 2 time points in file
    storm["lon"] = [1.0, 1.5, 2.0]
    storm["lat"] = [0.0, 0.5, 1.0]
    storm["year"] = [2014, 2014, 2014]
    storm["month"] = [12, 12, 12]
    storm["day"] = [21, 21, 21]
    storm["hour"] = [0, 6, 12]
    storm["step"] = [1, 2, 3]
    storm["slp"] = [9.997331e04, 9.9879215e04, 9.978512e04]
    storm["sfcWind"] = [1.206617e01, 1.1432575e01, 1.079898e01]
    storm["zg"] = [5.092293e03, 5.1024065e3, 5.112520e03]
    storm["orog"] = [0.000000e00, 0.000000e00, 0.000000e00]
    storms.append(storm)
    return storms
