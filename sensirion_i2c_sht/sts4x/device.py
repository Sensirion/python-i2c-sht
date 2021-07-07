# -*- coding: utf-8 -*-
# (c) Copyright 2021 Sensirion AG, Switzerland

from __future__ import absolute_import, division, print_function
from sensirion_i2c_driver import I2cDevice
from .commands import Sts4xI2cCmdMeasHighRes, Sts4xI2cCmdMeasMediumRes, \
    Sts4xI2cCmdMeasLowRes, Sts4xI2cCmdSoftReset, Sts4xI2cCmdReadSerial
from .data_types import Sts4xRepeatability


class Sts4xI2cDevice(I2cDevice):
    """
    STS4x I²C device class to allow executing I²C commands.
    """

    def __init__(self, connection, slave_address=0x44):
        """
        Constructs a new STS4x I²C device.

        :param ~sensirion_i2c_driver.connection.I2cConnection connection:
            The I²C connection to use for communication.
        :param byte slave_address:
            The I²C slave address, defaults to 0x44.
        """
        super(Sts4xI2cDevice, self).__init__(connection, slave_address)

    def single_shot_measurement(self, repeatability=Sts4xRepeatability.HIGH):
        """
        Trigger a measurement and read the temperature.

        :param `~sensirion_i2c_sht.sts4x.data_types.Sts4xRepeatability` repeatability:
            Configure the repeatability setting.
        :raises ValueError:
            If the passed repeatability is not valid.
        :return:
            The measured temperature

            - temperature (:py:class:`~sensirion_i2c_sht.sts4x.response_types.Sts4xTemperature`) -
              Temperature response object.
        :rtype:
            tuple
        """  # noqa: E501
        if repeatability == Sts4xRepeatability.HIGH:
            result = self.execute(Sts4xI2cCmdMeasHighRes())
        elif repeatability == Sts4xRepeatability.MEDIUM:
            result = self.execute(Sts4xI2cCmdMeasMediumRes())
        elif repeatability == Sts4xRepeatability.LOW:
            result = self.execute(Sts4xI2cCmdMeasLowRes())
        else:
            raise ValueError('Unknown argument for repeatability.')
        return result

    def soft_reset(self):
        """
        Perform a soft reset for the device. This can be used to force the
        system into a well-defined state without removing the power supply.
        """
        return self.execute(Sts4xI2cCmdSoftReset())

    def read_serial_number(self):
        """
        Read the serial number from the device.

        :return: The serial number.
        :rtype: int
        """
        return self.execute(Sts4xI2cCmdReadSerial())
