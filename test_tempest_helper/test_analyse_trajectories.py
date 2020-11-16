# (C) British Crown Copyright 2020, Met Office.
# Please see LICENSE for license details.
from unittest import TestCase
from .utils import make_loaded_trajectories

from tempest_helper import count_trajectories, count_hemispheric_trajectories


class TestCountHemispheric(TestCase):
    def test_northern(self):
        storms = make_loaded_trajectories()
        actual_south, actual_north = count_hemispheric_trajectories(storms)
        expected_south = 1
        self.assertEqual(expected_south, actual_south)
        expected_north = 2
        self.assertEqual(expected_north, actual_north)


class TestCountTrajectories(TestCase):
    def test_normal(self):
        storms = make_loaded_trajectories()
        actual = count_trajectories(storms)
        expected = 3
        self.assertEqual(expected, actual)

    def test_none(self):
        storms = []
        actual = count_trajectories(storms)
        expected = 0
        self.assertEqual(expected, actual)
