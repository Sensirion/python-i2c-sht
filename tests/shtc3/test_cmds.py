# -*- coding: utf-8 -*-
# (c) Copyright 2020 Sensirion AG, Switzerland

from __future__ import absolute_import, division, print_function
from sensirion_i2c_sht.shtc3 import Shtc3PowerMode, Shtc3Humidity, Shtc3Temperature
import pytest


@pytest.mark.needs_device
@pytest.mark.needs_shtc3
@pytest.mark.parametrize("power_mode", [
    Shtc3PowerMode.NORMAL,
    Shtc3PowerMode.LOW,
])
def test_measure(shtc3, power_mode):
    """
    Test if the command is accepted by the device and returns the proper
    result.
    """
    temperature, humidity = shtc3.measure(power_mode)
    assert type(temperature) is Shtc3Temperature
    assert type(temperature.ticks) is int
    assert type(humidity) is Shtc3Humidity
    assert type(humidity.ticks) is int


@pytest.mark.needs_device
@pytest.mark.needs_shtc3
def test_soft_reset(shtc3):
    """
    Test if the command is accepted by the device and returns the proper
    result.
    """
    shtc3.wake_up()
    result = shtc3.soft_reset()
    shtc3.enter_sleep()
    assert result is None


@pytest.mark.needs_device
@pytest.mark.needs_shtc3
def test_read_product_id(shtc3):
    """
    Test if the command is accepted by the device and returns the proper
    result.
    """
    shtc3.wake_up()
    result = shtc3.read_product_id()
    shtc3.enter_sleep()
    assert type(result) is int
