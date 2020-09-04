# -*- coding: utf-8 -*-
# (c) Copyright 2020 Sensirion AG, Switzerland

from __future__ import absolute_import, division, print_function
from enum import IntEnum

import logging
log = logging.getLogger(__name__)


class Sht3xRepeatability(IntEnum):
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
