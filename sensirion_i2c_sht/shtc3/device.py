# -*- coding: utf-8 -*-
# (c) Copyright 2021 Sensirion AG, Switzerland

from __future__ import absolute_import, division, print_function

from sensirion_i2c_driver import I2cDevice

from .commands import Shtc3I2cCmdMeasureNormalModeTicks, Shtc3I2cCmdMeasureLowestPowerModeTicks, \
    Shtc3I2cCmdMeasureNormalModeTicksClockStretching, Shtc3I2cCmdMeasureLowestPowerModeTicksClockStretching, \
    Shtc3I2cCmdProductId, Shtc3I2cCmdWakeUp, Shtc3I2cCmdSleep, Shtc3I2cCmdSoftReset
from .data_types import Shtc3PowerMode


class Shtc3I2cDevice(I2cDevice):
    """
    SHTC3 I²C device class to allow executing I²C commands.
    """

    def __init__(self, connection, slave_address=0x70):
        """
        Constructs a new SHTC3 I²C device.

        :param ~sensirion_i2c_driver.connection.I2cConnection connection:
            The I²C connection to use for communication.
        :param byte slave_address:
            The I²C slave address, defaults to 0x70.
        """
        super(Shtc3I2cDevice, self).__init__(connection, slave_address)

    def measure(self, power_mode=Shtc3PowerMode.NORMAL):
        """
        Trigger a measurement with clock stretching disabled and read the temperature and humidity.

        :param `~sensirion_i2c_sht.shtc3.data_types.Shtc3PowerMode` power_mode:
            Configure the power mode setting.
        :raises ValueError:
            If the passed power mode is not valid.
        :return:
            The measured temperature and humidity.

            - temperature (:py:class:`~sensirion_i2c_sht.shtc3.response_types.Shtc3xTemperature`) -
              Temperature response object.
            - humidity (:py:class:`~sensirion_i2c_sht.shtc3.response_types.Shtc3Humidity`) -
              Humidity response object.
        :rtype:
            tuple
        """  # noqa: E501
        self.wake_up()
        if power_mode == Shtc3PowerMode.NORMAL:
            result = self.execute(Shtc3I2cCmdMeasureNormalModeTicks())
        elif power_mode == Shtc3PowerMode.LOW:
            result = self.execute(Shtc3I2cCmdMeasureLowestPowerModeTicks())
        else:
            raise ValueError('Unknown argument for power_mode.')
        self.enter_sleep()
        return result

    def measure_clock_stretching(self, power_mode=Shtc3PowerMode.NORMAL):
        """
        Trigger a measurement with clock stretching enabled and read the temperature and humidity.

        :param `~sensirion_i2c_sht.shtc3.data_types.Shtc3PowerMode` power_mode:
            Configure the power mode setting.
        :raises ValueError:
            If the passed power mode is not valid.
        :return:
            The measured temperature and humidity.

            - temperature (:py:class:`~sensirion_i2c_sht.shtc3.response_types.Shtc3xTemperature`) -
              Temperature response object.
            - humidity (:py:class:`~sensirion_i2c_sht.shtc3.response_types.Shtc3Humidity`) -
              Humidity response object.
        :rtype:
            tuple
        """  # noqa: E501
        self.wake_up()
        if power_mode == Shtc3PowerMode.NORMAL:
            result = self.execute(Shtc3I2cCmdMeasureNormalModeTicksClockStretching())
        elif power_mode == Shtc3PowerMode.LOW:
            result = self.execute(Shtc3I2cCmdMeasureLowestPowerModeTicksClockStretching())
        else:
            raise ValueError('Unknown argument for power_mode.')
        self.enter_sleep()
        return result

    def read_product_id(self):
        """
        Read the product id from the device.

        :return: The product id.
        :rtype: int
        """
        return self.execute(Shtc3I2cCmdProductId())

    def wake_up(self):
        """
        wake up SHTC3.

        .. note:: When the sensor is in sleep mode, it requires the
                  wake-up command before any further communication
        """
        self.execute(Shtc3I2cCmdWakeUp())

    def enter_sleep(self):
        """
        Sleep command of the sensor.

        .. note:: Upon VDD reaching the power-up voltage level V_POR , the SHTC3
                  enters the idle state after a duration of 240us. After that,
                  the sensor should be set to sleep.
        """
        self.execute(Shtc3I2cCmdSleep())

    def soft_reset(self):
        """
        Perform a soft reset for the device. This can be used to force the
        system into a well-defined state without removing the power supply.
        """
        return self.execute(Shtc3I2cCmdSoftReset())
