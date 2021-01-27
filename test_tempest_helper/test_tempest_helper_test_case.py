# (C) British Crown Copyright 2020, Met Office.
# Please see LICENSE for license details.
from .utils import TempestHelperTestCase


class TestTempestHelperTestCase(TempestHelperTestCase):
    """Test that the custom test case works itself!"""
    def setUp(self):
        self.expected = {'a': 1, 'b': [1, 2]}

    def test_custom_pass(self):
        actual = {'a': 1, 'b': [1, 2]}
        self.assertTempestDictEqual(self.expected, actual)

    def test_extra_key(self):
        actual = {'a': 1, 'b': [1, 2], 'c': 3}
        self.assertRaisesRegex(AssertionError, r"Keys differ.*",
                               self.assertTempestDictEqual, self.expected,
                               actual)

    def test_different_key_name(self):
        actual = {'a': 1, 'c': {'c': 3}}
        self.assertRaisesRegex(AssertionError, r"Keys differ.*",
                               self.assertTempestDictEqual, self.expected,
                               actual)

    def test_differing_types(self):
        actual = {'a': 1, 'b': {'c': 3}}
        self.assertRaisesRegex(AssertionError, "Key b type list != dict",
                               self.assertTempestDictEqual, self.expected,
                               actual)

    def test_differing_types_int_float(self):
        actual = {'a': 1., 'b': [1, 2]}
        self.assertRaisesRegex(AssertionError, "Key a type int != float",
                               self.assertTempestDictEqual, self.expected,
                               actual)

    def test_int(self):
        actual = {'a': 2, 'b': [1, 2]}
        self.assertRaisesRegex(AssertionError, "a 1 != 2",
                               self.assertTempestDictEqual, self.expected,
                               actual)

    def test_float_fail(self):
        expected = {'a': 1., 'b': [1, 2]}
        actual = {'a': 2., 'b': [1, 2]}
        self.assertRaisesRegex(AssertionError, "a is not close 1.0, 2.0 with "
                                               "rel_tol=1e-09 abs_tol=0.0",
                               self.assertTempestDictEqual, expected, actual)

    def test_float_default_tolerance_pass(self):
        expected = {'a': 1., 'b': [1, 2]}
        actual = {'a': 1.0000000001, 'b': [1, 2]}
        self.assertTempestDictEqual(expected, actual)

    def test_float_default_tolerance_fail(self):
        expected = {'a': 1., 'b': [1, 2]}
        actual = {'a': 1.000000001, 'b': [1, 2]}
        self.assertRaisesRegex(
            AssertionError,
            "a is not close 1.0, 1.000000001 with rel_tol=1e-09 abs_tol=0.0",
            self.assertTempestDictEqual,
            expected,
            actual)

    def test_float_abs_tolerance_pass(self):
        expected = {'a': 1., 'b': [1, 2]}
        actual = {'a': 2., 'b': [1, 2]}
        self.abs_tol = 2.
        self.assertTempestDictEqual(expected, actual)

    def test_float_abs_tolerance_fail(self):
        expected = {'a': 1., 'b': [1, 2]}
        actual = {'a': 2., 'b': [1, 2]}
        self.abs_tol = 0.5
        self.assertRaisesRegex(AssertionError, "a is not close 1.0, 2.0 with "
                                               "rel_tol=1e-09 abs_tol=0.5",
                               self.assertTempestDictEqual, expected, actual)

    def test_float_rel_tolerance_pass(self):
        expected = {'a': 1., 'b': [1, 2]}
        actual = {'a': 1.04, 'b': [1, 2]}
        self.rel_tol = 0.05
        self.assertTempestDictEqual(expected, actual)

    def test_float_rel_tolerance_fail(self):
        expected = {'a': 1., 'b': [1, 2]}
        actual = {'a': 1.06, 'b': [1, 2]}
        self.rel_tol = 0.05
        self.assertRaisesRegex(AssertionError, "a is not close 1.0, 1.06 with "
                                               "rel_tol=0.05 abs_tol=0.0",
                               self.assertTempestDictEqual, expected, actual)

    def test_different_list_length(self):
        actual = {'a': 1, 'b': [1, 2, 3]}
        self.assertRaisesRegex(AssertionError, "Key b length 2 != 3",
                               self.assertTempestDictEqual, self.expected,
                               actual)

    def test_different_list_type(self):
        actual = {'a': 1, 'b': [1., 2]}
        self.assertRaisesRegex(AssertionError, "Key b value type 1 != 1.0",
                               self.assertTempestDictEqual, self.expected,
                               actual)

    def test_list_int_value_passes(self):
        expected = {'a': 1, 'b': [1, 2]}
        actual = {'a': 1, 'b': [1, 2]}
        self.assertTempestDictEqual(expected, actual)

    def test_list_int_value_fails(self):
        expected = {'a': 1, 'b': [1, 2]}
        actual = {'a': 1, 'b': [2, 2]}
        self.assertRaisesRegex(AssertionError, "Key b value 1 != 2",
                               self.assertTempestDictEqual, expected, actual)

    def test_list_float_value_passes(self):
        expected = {'a': 1, 'b': [1., 2]}
        actual = {'a': 1, 'b': [1., 2]}
        self.assertTempestDictEqual(expected, actual)

    def test_list_float_value(self):
        expected = {'a': 1, 'b': [1., 2]}
        actual = {'a': 1, 'b': [2., 2]}
        self.assertRaisesRegex(
            AssertionError,
            "Key b value is not close 1.0 2.0 with rel_tol=1e-09 abs_tol=0.0",
            self.assertTempestDictEqual,
            expected,
            actual)

    def test_list_bad_value_type(self):
        expected = {'a': 1, 'b': ['1', 2]}
        actual = {'a': 1, 'b': ['1', 2]}
        self.assertRaisesRegex(AssertionError,
                               "Key b no test for value 1 type str",
                               self.assertTempestDictEqual, expected, actual)

    def test_bad_type(self):
        actual = {'a': 1, 'b': {'c': 3}}
        self.assertRaisesRegex(AssertionError, "Key b no test for type dict",
                               self.assertTempestDictEqual, actual, actual)
