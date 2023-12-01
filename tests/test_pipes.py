#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 17:59:54 2023

@author: moritz
"""

# Python package index
import pytest

# custom modules
from src import pipes as pps


@pytest.mark.parametrize(
    "genders,expected_value",
    [
        ("male", 0),
        ("female", 1),
        ("female,female", 1),
        ("male,female", 0.5),
        ("female,female,male", 0.67),
    ],
)
def test_gender_ratio(genders, expected_value):
    ratio = pps.calculate_gender_ratio(genders)
    assert ratio == expected_value
