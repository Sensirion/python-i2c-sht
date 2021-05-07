# -*- coding: utf-8 -*-
# (c) Copyright 2021 Sensirion AG, Switzerland

from __future__ import absolute_import, division, print_function
from sensirion_i2c_driver import I2cDevice
from .commands import Sht4xI2cCmdMeasHighRes, Sht4xI2cCmdMeasMediumRes, \
    Sht4xI2cCmdMeasLowRes, Sht4xI2cCmdSoftReset, Sht4xI2cCmdReadSerial, \
    Sht4xI2cCmdHeaterHighPowerLong, Sht4xI2cCmdHeaterHighPowerShort, \
    Sht4xI2cCmdHeaterMediumPowerLong, Sht4xI2cCmdHeaterMediumPowerShort, \
    Sht4xI2cCmdHeaterLowPowerLong, Sht4xI2cCmdHeaterLowPowerShort
from .data_types import Sht4xRepeatability, Sht4xHeaterActivationDuration, \
    Sht4xHeaterPower


class Sht4xI2cDevice(I2cDevice):
    """
    SHT4x I²C device class to allow executing I²C commands.
    """

    def __init__(self, connection, slave_address=0x44):
        """
        Constructs a new SHT4x I²C device.

        :param ~sensirion_i2c_driver.connection.I2cConnection connection:
            The I²C connection to use for communication.
        :param byte slave_address:
            The I²C slave address, defaults to 0x44.
        """
        super(Sht4xI2cDevice, self).__init__(connection, slave_address)

    def single_shot_measurement(self, repeatability=Sht4xRepeatability.HIGH):
        """
        Trigger a measurement and read the temperature and humidity.

        :param `~sensirion_i2c_sht.sht4x.data_types.Sht4xRepeatability` repeatability:
            Configure the repeatability setting.
        :raises ValueError:
            If the passed repeatability is not valid.
        :return:
            The measured temperature and humidity.

            - temperature (:py:class:`~sensirion_i2c_sht.sht4x.response_types.Sht4xTemperature`) -
              Temperature response object.
            - humidity (:py:class:`~sensirion_i2c_sht.sht4x.response_types.Sht4xHumidity`) -
              Humidity response object.
        :rtype:
            tuple
        """  # noqa: E501
        if repeatability == Sht4xRepeatability.HIGH:
            result = self.execute(Sht4xI2cCmdMeasHighRes())
        elif repeatability == Sht4xRepeatability.MEDIUM:
            result = self.execute(Sht4xI2cCmdMeasMediumRes())
        elif repeatability == Sht4xRepeatability.LOW:
            result = self.execute(Sht4xI2cCmdMeasLowRes())
        else:
            raise ValueError('Unknown argument for repeatability.')
        return result

    def activate_heater(self, power=Sht4xHeaterPower.HIGH,
                        duration=Sht4xHeaterActivationDuration.LONG):
        """
        Activate the heater and trigger a high precision measurement.

        Important notes for operating the heater:

            - The heater is designed for a maximum duty cycle of 5%.
            - During operation of the heater, sensor specifications are not
              valid.
            - The temperature sensor can additionally be affected by the
              thermally induced mechanical  stress, offsetting the temperature
              reading from the actual temperature.
            - The sensor’s temperature (base temperature + temperature increase
              from heater) must not exceed Tmax = 125 °C in order to have
              proper electrical functionality of the chip.

        If higher heating temperatures are desired, consecutive heating
        commands have to be sent to the sensor. The heater shall only be
        operated in ambient temperatures below 65°C else it could drive the
        sensor outside of its maximal operating temperature.

        :param `~sensirion_i2c_sht.sht4x.data_types.Sht4xHeaterPower` power:
            Configure the heater power setting.
        :param `~sensirion_i2c_sht.sht4x.data_types.Sht4xHeaterActivationDuration` duration:
            Configure the heater activation duration.
        :raises ValueError:
            If the passed parameters are not valid.
        :return:
            The measured temperature and humidity.

            - temperature (:py:class:`~sensirion_i2c_sht.sht4x.response_types.Sht4xTemperature`) -
              Temperature response object.
            - humidity (:py:class:`~sensirion_i2c_sht.sht4x.response_types.Sht4xHumidity`) -
              Humidity response object.
        :rtype:
            tuple
        """  # noqa: E501
        if power == Sht4xHeaterPower.HIGH:
            if duration == Sht4xHeaterActivationDuration.LONG:
                result = self.execute(Sht4xI2cCmdHeaterHighPowerLong())
            elif duration == Sht4xHeaterActivationDuration.SHORT:
                result = self.execute(Sht4xI2cCmdHeaterHighPowerShort())
            else:
                raise ValueError('Unknown argument for duration.')
        elif power == Sht4xHeaterPower.MEDIUM:
            if duration == Sht4xHeaterActivationDuration.LONG:
                result = self.execute(Sht4xI2cCmdHeaterMediumPowerLong())
            elif duration == Sht4xHeaterActivationDuration.SHORT:
                result = self.execute(Sht4xI2cCmdHeaterMediumPowerShort())
            else:
                raise ValueError('Unknown argument for duration.')
        elif power == Sht4xHeaterPower.LOW:
            if duration == Sht4xHeaterActivationDuration.LONG:
                result = self.execute(Sht4xI2cCmdHeaterLowPowerLong())
            elif duration == Sht4xHeaterActivationDuration.SHORT:
                result = self.execute(Sht4xI2cCmdHeaterLowPowerShort())
            else:
                raise ValueError('Unknown argument for duration.')
        else:
            raise ValueError('Unknown argument for power.')
        return result

    def soft_reset(self):
        """
        Perform a soft reset for the device. This can be used to force the
        system into a well-defined state without removing the power supply.
        """
        return self.execute(Sht4xI2cCmdSoftReset())

    def read_serial_number(self):
        """
        Read the serial number from the device.

        :return: The serial number.
        :rtype: int
        """
        return self.execute(Sht4xI2cCmdReadSerial())
