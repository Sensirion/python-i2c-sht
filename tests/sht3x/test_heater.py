# -*- coding: utf-8 -*-
# (c) Copyright 2019 Sensirion AG, Switzerland

from __future__ import absolute_import, division, print_function
import pytest


@pytest.mark.needs_device
@pytest.mark.needs_sht3x
def test(sht3x):
    """
    Test if the heater commands work as expected by reading the status
    register.
    """
    # check that the heater is off on power up
    sht3x.clear_status_register()
    status = sht3x.read_status_register()
    assert status.heater_status is False

    # turn heater on and check that it is switched on
    sht3x.heater_on()
    status = sht3x.read_status_register()
    assert status.heater_status is True

    # turn heater off and check that it is switched off
    sht3x.heater_off()
    status = sht3x.read_status_register()
    assert status.heater_status is False
