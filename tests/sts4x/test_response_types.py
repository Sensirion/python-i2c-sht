# -*- coding: utf-8 -*-
# (c) Copyright 2021 Sensirion AG, Switzerland

from __future__ import absolute_import, division, print_function
from sensirion_i2c_sht.sts4x import Sts4xTemperature
import pytest


@pytest.mark.parametrize("value", [
    dict({'ticks': 0, 'degrees_celsius': -45., 'degrees_fahrenheit': -49.}),
    dict(
        {'ticks': 65535, 'degrees_celsius': 130., 'degrees_fahrenheit': 266.}),
])
def test_temperature(value):
    """
    Test if the Temperature() type works as expected for different values.
    """
    result = Sts4xTemperature(value.get('ticks'))
    assert type(result) is Sts4xTemperature
    assert type(result.ticks) is int
    assert result.ticks == value.get('ticks')
    assert type(result.degrees_celsius) is float
    assert result.degrees_celsius == value.get('degrees_celsius')
    assert type(result.degrees_fahrenheit) is float
    assert result.degrees_fahrenheit == value.get('degrees_fahrenheit')
