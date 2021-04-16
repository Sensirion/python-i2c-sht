# -*- coding: utf-8 -*-
# (c) Copyright 2021 Sensirion AG, Switzerland

from __future__ import absolute_import, division, print_function
from enum import IntEnum

import logging
log = logging.getLogger(__name__)


class Sht4xRepeatability(IntEnum):
    """
    An enum containing all available repeatability settings for the
    temperature and humidity measurement.

    .. note: The repeatability setting influences the measurement
             duration and thus the overall energy consumption of the sensor.
             Check the datasheet for further information.
    """
    HIGH = 1    #: High repeatability
    MEDIUM = 2  #: Medium repeatability
    LOW = 3     #: Low repeatability


class Sht4xHeaterPower(IntEnum):
    """
    An enum containing all available heater power settings.
    """
    HIGH = 1    #: High power (typ. 200mW @ 3.3V)
    MEDIUM = 2  #: Medium power (typ. 110mW @ 3.3V)
    LOW = 3     #: Lowest power (typ. 20mW @ 3.3V)


class Sht4xHeaterActivationDuration(IntEnum):
    """
    An enum containing all available heater activation duration settings.
    """
    LONG = 1    #: Long duration (typ. 1 second)
    SHORT = 2   #: Short duration (typ. 0.1 seconds)
