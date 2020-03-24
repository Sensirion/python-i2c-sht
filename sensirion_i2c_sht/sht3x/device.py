# -*- coding: utf-8 -*-
# (c) Copyright 2020 Sensirion AG, Switzerland

from __future__ import absolute_import, division, print_function
from sensirion_i2c_driver.device import I2cDevice
from .commands import Sht3xI2cCmdMeasHighRes, Sht3xI2cCmdMeasMediumRes, \
    Sht3xI2cCmdMeasLowRes, Sht3xI2cCmdHeaterOn, Sht3xI2cCmdHeaterOff, \
    Sht3xI2cCmdReadStatusRegister, Sht3xI2cCmdResetStatusRegister, \
    Sht3xI2cCmdSoftReset


class Sht3xI2cDevice(I2cDevice):
    """
    SHT3x I²C device class to allow executing I²C commands.
    """

    def __init__(self, connection, slave_address=0x44):
        """
        Constructs a new SHT3x I²C device.

        :param ~sensirion_i2c_driver.connection.I2cConnection connection:
            The I²C connection to use for communication.
        :param byte slave_address:
            The I²C slave address, defaults to 0x44.
        """
        super(Sht3xI2cDevice, self).__init__(connection, slave_address)

    def single_shot_measurement(self, repeatability='high'):
        """
        Trigger a measurement and read the temperature and humidity.

        :param str repeatability:
            Configure the desired repeatability. Available option are
            'high', 'medium' and 'low'.
        :return:
            The measured temperature and humidity.

            - temperature (:py:class:`~sensirion_i2c_sht.sht3x.types.Temperature`) -
              Temperature response object.
            - humidity (:py:class:`~sensirion_i2c_sht.sht3x.types.Humidity`) -
              Humidity response object.
        :rtype:
            tuple
        """  # noqa: E501
        if repeatability.lower() == 'high':
            result = self.execute(Sht3xI2cCmdMeasHighRes())
        elif repeatability.lower() == 'medium':
            result = self.execute(Sht3xI2cCmdMeasMediumRes())
        elif repeatability.lower() == 'low':
            result = self.execute(Sht3xI2cCmdMeasLowRes())
        else:
            raise ValueError('Unknown argument for repeatability.')
        return result

    def heater_on(self):
        """
        Switch on the internal heater.
        """
        self.execute(Sht3xI2cCmdHeaterOn())

    def heater_off(self):
        """
        Switch off the internal heater.
        """
        self.execute(Sht3xI2cCmdHeaterOff())

    def read_status_register(self):
        """
        Read out the status register.

        :return: The status register.
        :rtype: :py:class:`~sensirion_i2c_sht.sht3x.types.StatusRegister`
        """
        return self.execute(Sht3xI2cCmdReadStatusRegister())

    def clear_status_register(self):
        """
        Clear the status register. All flags (Bit 15, 11, 10, 4) in the status
        register can be cleared (set to zero).
        """
        self.execute(Sht3xI2cCmdResetStatusRegister())

    def soft_reset(self):
        """
        Perform a soft reset for the device. This can be used to force the
        system into a well-defined state without removing the power supply.
        """
        self.execute(Sht3xI2cCmdSoftReset())
