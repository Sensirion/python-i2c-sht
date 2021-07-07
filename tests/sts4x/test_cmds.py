# -*- coding: utf-8 -*-
# (c) Copyright 2021 Sensirion AG, Switzerland

from __future__ import absolute_import, division, print_function
import pytest

from sensirion_i2c_sht.sts4x import Sts4xRepeatability, Sts4xTemperature


@pytest.mark.needs_device
@pytest.mark.needs_sts4x
@pytest.mark.parametrize("repeatability", [
    Sts4xRepeatability.HIGH,
    Sts4xRepeatability.MEDIUM,
    Sts4xRepeatability.LOW,
])
def test_single_shot_measurement(sts4x, repeatability):
    """
    Test if the command is accepted by the device and returns the proper
    result.
    """
    temperature = sts4x.single_shot_measurement(repeatability)
    assert type(temperature) is Sts4xTemperature
    assert type(temperature.ticks) is int


@pytest.mark.needs_device
@pytest.mark.needs_sts4x
def test_soft_reset(sts4x):
    """
    Test if the command is accepted by the device and returns the proper
    result.
    """
    result = sts4x.soft_reset()
    assert result is None


@pytest.mark.needs_device
@pytest.mark.needs_sts4x
def test_read_serial_number(sts4x):
    """
    Test if the command is accepted by the device and returns the proper
    result.
    """
    result = sts4x.read_serial_number()
    assert type(result) is int
