# -*- coding: utf-8 -*-
# (c) Copyright 2021 Sensirion AG, Switzerland

from __future__ import absolute_import, division, print_function

import logging
log = logging.getLogger(__name__)


class Shtc3Temperature(object):
    """
    Represents a measurement response for the temperature.

    With the :py:attr:`ticks` you can access the raw data as received from the
    device. For the converted values you can choose between
    :py:attr:`degrees_celsius` and :py:attr:`degrees_fahrenheit`.

    :param int ticks:
        The read ticks as received from the device.
    """
    def __init__(self, ticks):
        """
        Creates an instance from the received raw data.
        """
        super(Shtc3Temperature, self).__init__()

        #: The ticks (int) as received from the device.
        self.ticks = ticks

        #: The converted temperature in °C.
        self.degrees_celsius = -45. + 175. * ticks / 65535.

        #: The converted temperature in °F.
        self.degrees_fahrenheit = -49. + 315. * ticks / 65535.

    def __str__(self):
        return '{:0.1f} °C'.format(self.degrees_celsius)


class Shtc3Humidity(object):
    """
    Represents a measurement response for the humidity.

    With the :py:attr:`ticks` you can access the raw data as received from the
    device. For the converted value the :py:attr:`percent_rh` attribute is
    available.

    :param int ticks:
        The read ticks as received from the device.
    """
    def __init__(self, ticks):
        """
        Creates an instance from the received raw data.
        """
        super(Shtc3Humidity, self).__init__()

        #: The ticks (int) as received from the device.
        self.ticks = ticks

        #: The converted humidity in %RH.
        self.percent_rh = 100. * ticks / 65535.

    def __str__(self):
        return '{:0.1f} %RH'.format(self.percent_rh)
