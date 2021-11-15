# -*- coding: utf-8 -*-
# (c) Copyright 2021 Sensirion AG, Switzerland

from __future__ import absolute_import, division, print_function
from enum import IntEnum

import logging
log = logging.getLogger(__name__)


class Shtc3PowerMode(IntEnum):
    """
    An enum containing all available power mode settings for the
    temperature and humidity measurement.

    .. note: The power mode setting influences the measurement
             duration and thus the overall energy consumption of the sensor.
             Check the datasheet for further information.
    """
    LOW = 1     #: Low power mode
    NORMAL = 2  #: Normal power mode
