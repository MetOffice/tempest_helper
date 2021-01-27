# (C) British Crown Copyright 2020, Met Office.
# Please see LICENSE for license details.
from math import isclose
from typing import Any, Dict
from unittest import TestCase


class TempestHelperTestCase(TestCase):
    """
    Add an assertTempestDictEqual method to TestCase to compare the
    dictionaries used in tempest_helper. Values can be ints, floats or lists
    of these two types; other types of value will fail.

    Instance attributes `self.rel_tol` and `self.abs_tol` can be set in child
    instances to set the relative and absolute tolerance passed to
    `math.isclose()` to test all floats with.
    """

    @classmethod
    def setUpClass(cls):
        cls.rel_tol = 1e-9
        cls.abs_tol = 0.0

    def assertTempestDictEqual(
        self, expected: Dict[Any, Any], actual: Dict[Any, Any]
    ) -> None:
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
