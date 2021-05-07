# -*- coding: utf-8 -*-
# (c) Copyright 2020 Sensirion AG, Switzerland

from __future__ import absolute_import, division, print_function
from sensirion_i2c_sht.sht4x import Sht4xTemperature, Sht4xHumidity, \
    Sht4xRepeatability, Sht4xHeaterActivationDuration, Sht4xHeaterPower
import pytest


@pytest.mark.needs_device
@pytest.mark.needs_sht4x
@pytest.mark.parametrize("repeatability", [
    Sht4xRepeatability.HIGH,
    Sht4xRepeatability.MEDIUM,
    Sht4xRepeatability.LOW,
])
def test_single_shot_measurement(sht4x, repeatability):
    """
    Test if the command is accepted by the device and returns the proper
    result.
    """
    temperature, humidity = sht4x.single_shot_measurement(repeatability)
    assert type(temperature) is Sht4xTemperature
    assert type(temperature.ticks) is int
    assert type(humidity) is Sht4xHumidity
    assert type(humidity.ticks) is int


@pytest.mark.needs_device
@pytest.mark.needs_sht4x
@pytest.mark.parametrize("power", [
    Sht4xHeaterPower.HIGH,
    Sht4xHeaterPower.MEDIUM,
    Sht4xHeaterPower.LOW,
])
@pytest.mark.parametrize("duration", [
    Sht4xHeaterActivationDuration.LONG,
    Sht4xHeaterActivationDuration.SHORT,
])
def test_activate_heater(sht4x, power, duration):
    """
    Test if the command is accepted by the device and returns the proper
    result.
    """
    temperature, humidity = sht4x.activate_heater(power, duration)
    assert type(temperature) is Sht4xTemperature
    assert type(temperature.ticks) is int
    assert type(humidity) is Sht4xHumidity
    assert type(humidity.ticks) is int


@pytest.mark.needs_device
@pytest.mark.needs_sht4x
def test_soft_reset(sht4x):
    """
    Test if the command is accepted by the device and returns the proper
    result.
    """
    result = sht4x.soft_reset()
    assert result is None


@pytest.mark.needs_device
@pytest.mark.needs_sht4x
def test_read_serial_number(sht4x):
    """
    Test if the command is accepted by the device and returns the proper
    result.
    """
    result = sht4x.read_serial_number()
    assert type(result) is int
