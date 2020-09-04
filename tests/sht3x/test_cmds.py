# -*- coding: utf-8 -*-
# (c) Copyright 2020 Sensirion AG, Switzerland

from __future__ import absolute_import, division, print_function
from sensirion_i2c_sht.sht3x import Sht3xTemperature, Sht3xHumidity, \
    Sht3xStatusRegister, Sht3xRepeatability
import pytest


@pytest.fixture
def sht3x_with_cmd_status_check(sht3x):
    """
    SHT3x fixture with a check of the command status after the command was
    executed.
    """
    # clear status and check command_status flag is not set
    sht3x.clear_status_register()
    status = sht3x.read_status_register()
    assert status.command_status is False

    # execute command
    yield sht3x

    # read status and check command_status flag is still not set
    status = sht3x.read_status_register()
    assert status.command_status is False


@pytest.mark.needs_device
@pytest.mark.needs_sht3x
@pytest.mark.parametrize("repeatability", [
    Sht3xRepeatability.HIGH,
    Sht3xRepeatability.MEDIUM,
    Sht3xRepeatability.LOW,
])
def test_single_shot_measurement(sht3x_with_cmd_status_check, repeatability):
    """
    Test if the command is accepted by the device and returns the proper
    result.
    """
    temperature, humidity = \
        sht3x_with_cmd_status_check.single_shot_measurement(repeatability)
    assert type(temperature) is Sht3xTemperature
    assert type(temperature.ticks) is int
    assert type(humidity) is Sht3xHumidity
    assert type(humidity.ticks) is int


@pytest.mark.needs_device
@pytest.mark.needs_sht3x
def test_heater_on(sht3x_with_cmd_status_check):
    """
    Test if the command is accepted by the device and returns the proper
    result.
    """
    result = sht3x_with_cmd_status_check.heater_on()
    assert result is None


@pytest.mark.needs_device
@pytest.mark.needs_sht3x
def test_heater_off(sht3x_with_cmd_status_check):
    """
    Test if the command is accepted by the device and returns the proper
    result.
    """
    result = sht3x_with_cmd_status_check.heater_off()
    assert result is None


@pytest.mark.needs_device
@pytest.mark.needs_sht3x
def test_read_status_register(sht3x_with_cmd_status_check):
    """
    Test if the command is accepted by the device and returns the proper
    result.
    """
    result = sht3x_with_cmd_status_check.read_status_register()
    assert type(result) is Sht3xStatusRegister
    assert type(result.raw) is int


@pytest.mark.needs_device
@pytest.mark.needs_sht3x
def test_clear_status_register(sht3x_with_cmd_status_check):
    """
    Test if the command is accepted by the device and returns the proper
    result.
    """
    result = sht3x_with_cmd_status_check.clear_status_register()
    assert result is None


@pytest.mark.needs_device
@pytest.mark.needs_sht3x
def test_soft_reset(sht3x_with_cmd_status_check):
    """
    Test if the command is accepted by the device and returns the proper
    result.
    """
    result = sht3x_with_cmd_status_check.soft_reset()
    assert result is None
