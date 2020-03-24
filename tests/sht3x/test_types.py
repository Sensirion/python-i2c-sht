# -*- coding: utf-8 -*-
# (c) Copyright 2019 Sensirion AG, Switzerland

from __future__ import absolute_import, division, print_function
from sensirion_i2c_sht.sht3x.types import Temperature, Humidity, StatusRegister
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
    result = Temperature(value.get('ticks'))
    assert type(result) is Temperature
    assert type(result.ticks) is int
    assert result.ticks == value.get('ticks')
    assert type(result.degrees_celsius) is float
    assert result.degrees_celsius == value.get('degrees_celsius')
    assert type(result.degrees_fahrenheit) is float
    assert result.degrees_fahrenheit == value.get('degrees_fahrenheit')


@pytest.mark.parametrize("value", [
    dict({'ticks': 0, 'percent_rh': 0.}),
    dict({'ticks': 65535, 'percent_rh': 100.}),
])
def test_humidity(value):
    """
    Test if the Humidity() type works as expected for different values.
    """
    result = Humidity(value.get('ticks'))
    assert type(result) is Humidity
    assert type(result.ticks) is int
    assert result.ticks == value.get('ticks')
    assert type(result.percent_rh) is float
    assert result.percent_rh == value.get('percent_rh')


@pytest.mark.parametrize("value", [
    dict({'input': 0x0000,
          'write_data_checksum_status': False,
          'command_status': False,
          'system_reset_detected': False,
          'temperature_tracking_alert': False,
          'humidity_tracking_alert': False,
          'heater_status': False,
          'alert_pending_status': False}),
    dict({'input': 0x0001,
          'write_data_checksum_status': True,
          'command_status': False,
          'system_reset_detected': False,
          'temperature_tracking_alert': False,
          'humidity_tracking_alert': False,
          'heater_status': False,
          'alert_pending_status': False}),
    dict({'input': 0x0002,
          'write_data_checksum_status': False,
          'command_status': True,
          'system_reset_detected': False,
          'temperature_tracking_alert': False,
          'humidity_tracking_alert': False,
          'heater_status': False,
          'alert_pending_status': False}),
    dict({'input': 0x0010,
          'write_data_checksum_status': False,
          'command_status': False,
          'system_reset_detected': True,
          'temperature_tracking_alert': False,
          'humidity_tracking_alert': False,
          'heater_status': False,
          'alert_pending_status': False}),
    dict({'input': 0x0400,
          'write_data_checksum_status': False,
          'command_status': False,
          'system_reset_detected': False,
          'temperature_tracking_alert': True,
          'humidity_tracking_alert': False,
          'heater_status': False,
          'alert_pending_status': False}),
    dict({'input': 0x0800,
          'write_data_checksum_status': False,
          'command_status': False,
          'system_reset_detected': False,
          'temperature_tracking_alert': False,
          'humidity_tracking_alert': True,
          'heater_status': False,
          'alert_pending_status': False}),
    dict({'input': 0x2000,
          'write_data_checksum_status': False,
          'command_status': False,
          'system_reset_detected': False,
          'temperature_tracking_alert': False,
          'humidity_tracking_alert': False,
          'heater_status': True,
          'alert_pending_status': False}),
    dict({'input': 0x8000,
          'write_data_checksum_status': False,
          'command_status': False,
          'system_reset_detected': False,
          'temperature_tracking_alert': False,
          'humidity_tracking_alert': False,
          'heater_status': False,
          'alert_pending_status': True}),
    dict({'input': 0xFFFF,
          'write_data_checksum_status': True,
          'command_status': True,
          'system_reset_detected': True,
          'temperature_tracking_alert': True,
          'humidity_tracking_alert': True,
          'heater_status': True,
          'alert_pending_status': True}),
])
def test_status_register(value):
    """
    Test if the StatusRegister() type works as expected for different values.
    """
    result = StatusRegister(value.get('input'))
    assert type(result) is StatusRegister
    for i, k in enumerate(value):
        if k != 'input':
            assert type(eval('result.{}'.format(k))) is bool
            assert eval('result.{}'.format(k)) == value.get(k)
