# -*- coding: utf-8 -*-
# (c) Copyright 2020 Sensirion AG, Switzerland

from __future__ import absolute_import, division, print_function
from enum import IntEnum

import logging
log = logging.getLogger(__name__)


class Repeatability(IntEnum):
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


class Temperature(object):
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
        super(Temperature, self).__init__()

        #: The ticks (int) as received from the device.
        self.ticks = ticks

        #: The converted temperature in °C.
        self.degrees_celsius = -45. + 175. * ticks / 65535.

        #: The converted temperature in °F.
        self.degrees_fahrenheit = -49. + 315. * ticks / 65535.

    def __str__(self):
        return '{:0.1f} °C'.format(self.degrees_celsius)


class Humidity(object):
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
        super(Humidity, self).__init__()

        #: The ticks (int) as received from the device.
        self.ticks = ticks

        #: The converted humidity in %RH.
        self.percent_rh = 100. * ticks / 65535.

    def __str__(self):
        return '{:0.1f} %RH'.format(self.percent_rh)


class StatusRegister(object):
    """
    Represents the content of the status register.

    With the :py:attr:`status_register_word` you can access the raw data as
    received from the device. For each data field of the status register an
    attribute is available.

    :param int status_register_word:
        The read status register word as received from the device.
    """
    def __init__(self, status_register_word):
        """
        Creates an instance from the received raw data.
        """
        super(StatusRegister, self).__init__()

        #: The raw data word (int) as received from the device.
        self.status_register_word = status_register_word

        #: Write data checksum status (Bit 0, bool)
        #:
        #: - False: checksum of last write transfer was correct
        #: - True: checksum of last write transfer failed
        self.write_data_checksum_status = bool(status_register_word & (1 << 0))

        #: Command status (Bit 1, bool)
        #:
        #: - False: last command executed successfully
        #: - True: last command not processed. It was either invalid or failed
        #:   the integrated command checksum
        self.command_status = bool(status_register_word & (1 << 1))

        #: System reset detected (Bit 4, bool)
        #:
        #: - False: no reset detected since last clear status register command
        #: - True: reset detected (hard reset, soft reset command or
        #    supply fail)
        self.system_reset_detected = bool(status_register_word & (1 << 4))

        #: Temperature tracking alert (Bit 10, bool)
        #:
        #: - False: no alert
        #: - True: alert
        self.temperature_tracking_alert = \
            bool(status_register_word & (1 << 10))

        #: Humidity tracking alert (Bit 11, bool)
        #:
        #: - False: no alert
        #: - True: alert
        self.humidity_tracking_alert = bool(status_register_word & (1 << 11))

        #: Heater status (Bit 13, bool)
        #:
        #: - False: heater off
        #: - True: heater on
        self.heater_status = bool(status_register_word & (1 << 13))

        #: Alert pending status (Bit 15, bool)
        #:
        #: - False: no pending alerts
        #: - True: at least one pending alert
        self.alert_pending_status = bool(status_register_word & (1 << 15))

    def __str__(self):
        return '0x{:04X}'.format(self.status_register_word)
