# -*- coding: utf-8 -*-
# (c) Copyright 2020 Sensirion AG, Switzerland

from __future__ import absolute_import, division, print_function
from sensirion_i2c_sht.sht2x import Sht2xTemperature, Sht2xHumidity
import pytest


@pytest.mark.needs_device
@pytest.mark.needs_sht2x
def test_single_shot_measurement(sht2x):
    """
    Test if the command is accepted by the device and returns the proper
    result.
    """
    temperature, humidity = sht2x.single_shot_measurement()
    assert type(temperature) is Sht2xTemperature
    assert type(temperature.ticks) is int
    assert type(humidity) is Sht2xHumidity
    assert type(humidity.ticks) is int


@pytest.mark.needs_device
@pytest.mark.needs_sht2x
def test_soft_reset(sht2x):
    """
    Test if the command is accepted by the device and returns the proper
    result.
    """
    result = sht2x.soft_reset()
    assert result is None


@pytest.mark.needs_device
@pytest.mark.needs_sht2x
def test_read_serial_number(sht2x):
    """
    Test if the command is accepted by the device and returns the proper
    result.
    """
    result = sht2x.read_serial_number()
    assert type(result) is int
