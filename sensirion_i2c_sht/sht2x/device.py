# -*- coding: utf-8 -*-
# (c) Copyright 2020 Sensirion AG, Switzerland

from __future__ import absolute_import, division, print_function
from sensirion_i2c_driver.device import I2cDevice
from sensirion_i2c_driver.errors import I2cError
from .commands import Sht2xI2cMeasureTemperature, Sht2xI2cMeasureHumidity, \
    Sht2xI2cCmdSoftReset, Sht2xI2cCmdReadOtp, Sht2xI2cCmdReadMetalRom


class Sht2xI2cDevice(I2cDevice):
    """
    SHT2x I²C device class to allow executing I²C commands.
    """

    def __init__(self, connection, slave_address=0x40):
        """
        Constructs a new SHT2x I²C device.

        :param ~sensirion_i2c_driver.connection.I2cConnection connection:
            The I²C connection to use for communication.
        :param byte slave_address:
            The I²C slave address, defaults to 0x44.
        """
        super(Sht2xI2cDevice, self).__init__(connection, slave_address)

    def single_shot_measurement(self):
        """
        Trigger a measurement and read the temperature and humidity.

        :return:
            The measured temperature and humidity.

            - temperature (:py:class:`~sensirion_i2c_sht.sht2x.response_types.Sht2xTemperature`) -
              Temperature response object.
            - humidity (:py:class:`~sensirion_i2c_sht.sht2x.response_types.Sht2xHumidity`) -
              Humidity response object.
        :rtype:
            tuple
        """  # noqa: E501
        temperature = self.execute(Sht2xI2cMeasureTemperature())
        humidity = self.execute(Sht2xI2cMeasureHumidity())
        if self.connection.is_multi_channel:
            result = list()
            for t, rh in zip(temperature, humidity):
                if isinstance(t, I2cError):
                    result.append(t)
                elif isinstance(rh, I2cError):
                    result.append(rh)
                else:
                    result.append((t, rh))
        else:
            if isinstance(temperature, I2cError):
                result = temperature
            elif isinstance(humidity, I2cError):
                result = humidity
            else:
                result = (temperature, humidity)
        return result

    def soft_reset(self):
        """
        Perform a soft reset for the device. This can be used to force the
        system into a well-defined state without removing the power supply.
        """
        return self.execute(Sht2xI2cCmdSoftReset())

    def read_serial_number(self):
        """
        Read the extended serial number from the device.

        :return: The extended serial number.
        :rtype: int
        """
        # read both from otp and metrom
        data_bytes_otp = self.execute(Sht2xI2cCmdReadOtp(0x0F, 4))
        data_words_metrom = self.execute(Sht2xI2cCmdReadMetalRom(2))
        if self.connection.is_multi_channel:
            serials = list()
            for part1, part2 in zip(data_bytes_otp, data_words_metrom):
                if isinstance(part1, I2cError):
                    serials.append(part1)
                elif isinstance(part2, I2cError):
                    serials.append(part2)
                else:
                    sn_otp = part1[0] << 24 | part1[1] << 16 | \
                             part1[2] << 8 | part1[3]
                    sn = (part2[1] << 48) | sn_otp << 16 | part2[0]
                    serials.append(sn)
        else:
            if isinstance(data_bytes_otp, I2cError):
                serials = data_bytes_otp
            elif isinstance(data_words_metrom, I2cError):
                serials = data_words_metrom
            else:
                sn_otp = data_bytes_otp[0] << 24 | \
                         data_bytes_otp[1] << 16 | data_bytes_otp[2] << 8 | \
                         data_bytes_otp[3]
                sn = (data_words_metrom[1] << 48) | sn_otp << 16 | \
                    data_words_metrom[0]
                serials = sn
        return serials
