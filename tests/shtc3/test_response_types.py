# -*- coding: utf-8 -*-
# (c) Copyright 2020 Sensirion AG, Switzerland

from __future__ import absolute_import, division, print_function
from sensirion_i2c_sht.shtc3 import Shtc3Humidity, Shtc3Temperature
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
    result = Shtc3Temperature(value.get('ticks'))
    assert type(result) is Shtc3Temperature
    assert type(result.ticks) is int
    assert result.ticks == value.get('ticks')
    assert type(result.degrees_celsius) is float
    assert result.degrees_celsius == value.get('degrees_celsius')
    assert type(result.degrees_fahrenheit) is float
    assert result.degrees_fahrenheit == value.get('degrees_fahrenheit')


@pytest.mark.parametrize("value", [
    dict({'ticks': 0, 'percent_rh': 0.0}),
    dict({'ticks': 65535, 'percent_rh': 100.0}),
])
def test_humidity(value):
    """
    Test if the Humidity() type works as expected for different values.
    """
    result = Shtc3Humidity(value.get('ticks'))
    assert type(result) is Shtc3Humidity
    assert type(result.ticks) is int
    assert result.ticks == value.get('ticks')
    assert type(result.percent_rh) is float
    assert result.percent_rh == value.get('percent_rh')
