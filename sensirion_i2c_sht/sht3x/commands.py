# -*- coding: utf-8 -*-
# (c) Copyright 2019 Sensirion AG, Switzerland

from __future__ import absolute_import, division, print_function
from sensirion_i2c_driver.sensirion_word_command import SensirionWordI2cCommand
from sensirion_i2c_driver.crc_calculator import CrcCalculator
from .types import Temperature, Humidity, StatusRegister


class Sht3xI2cCmdBase(SensirionWordI2cCommand):
    """
    SHT3x I²C base command.
    """
    def __init__(self, command, tx_words, rx_length, read_delay, timeout):
        """
        Constructs a new SHT3x I²C command.

        :param int/None command:
            The command word to be sent to the device. None means that no
            command will be sent, i.e. only ``tx_words`` (if not None) will
            be sent.
        :param list/None tx_words:
            Words (list of integers) to be sent to the I²C device. None means
            that no write header will be sent at all (if ``command`` is None
            too). An empty list means to send the write header (even if
            ``command`` is None), but without data following it.
        :param int/None rx_length:
            Number of bytes to be read from the I²C device, including CRC
            bytes. None means that no read header is sent at all. Zero means
            to send the read header, but without reading any data.
        :param float read_delay:
            Delay (in Seconds) to be inserted between the end of the write
            operation and the beginning of the read operation. This is needed
            if the device needs some time to prepare the RX data, e.g. if it
            has to perform a measurement. Set to 0.0 to indicate that no delay
            is needed, i.e. the device does not need any processing time.
        """
        super(Sht3xI2cCmdBase, self).__init__(
            command=command,
            tx_words=tx_words,
            rx_length=rx_length,
            read_delay=read_delay,
            timeout=timeout,
            crc=CrcCalculator(8, 0x31, 0xFF),
            command_bytes=2,
        )


class Sht3xI2cCmdMeasHighRes(Sht3xI2cCmdBase):
    """
    SHT3x command for a single shot measurement with high repeatability and
    clock stretching disabled.
    """
    def __init__(self):
        """
        Constructs a new command.
        """
        super(Sht3xI2cCmdMeasHighRes, self).__init__(
            command=0x2400,
            tx_words=[],
            rx_length=6,
            read_delay=0.02,
            timeout=0.,
        )

    def interpret_response(self, data):
        """
        Converts the raw response from the device to the proper data type.

        :param bytes data:
            Received raw bytes from the read operation.
        :return:
            The measured temperature and humidity.

            - temperature (:py:class:`~sensirion_i2c_sht.sht3x.types.Temperature`) -
              Temperature response object.
            - humidity (:py:class:`~sensirion_i2c_sht.sht3x.types.Humidity`) -
              Humidity response object.
        :rtype:
            tuple
        """  # noqa: E501
        words = SensirionWordI2cCommand.interpret_response(self, data)
        return Temperature(words[0]), Humidity(words[1])


class Sht3xI2cCmdMeasMediumRes(Sht3xI2cCmdBase):
    """
    SHT3x command for a single shot measurement with medium repeatability and
    clock stretching disabled.
    """
    def __init__(self):
        """
        Constructs a new command.
        """
        super(Sht3xI2cCmdMeasMediumRes, self).__init__(
            command=0x240B,
            tx_words=[],
            rx_length=6,
            read_delay=0.01,
            timeout=0.,
        )

    def interpret_response(self, data):
        """
        Converts the raw response from the device to the proper data type.

        :param bytes data:
            Received raw bytes from the read operation.
        :return:
            The measured temperature and humidity.

            - temperature (:py:class:`~sensirion_i2c_sht.sht3x.types.Temperature`) -
              Temperature response object.
            - humidity (:py:class:`~sensirion_i2c_sht.sht3x.types.Humidity`) -
              Humidity response object.
        :rtype:
            tuple
        """  # noqa: E501
        words = SensirionWordI2cCommand.interpret_response(self, data)
        return Temperature(words[0]), Humidity(words[1])


class Sht3xI2cCmdMeasLowRes(Sht3xI2cCmdBase):
    """
    SHT3x command for a single shot measurement with low repeatability and
    clock stretching disabled.
    """
    def __init__(self):
        """
        Constructs a new command.
        """
        super(Sht3xI2cCmdMeasLowRes, self).__init__(
            command=0x2416,
            tx_words=[],
            rx_length=6,
            read_delay=0.005,
            timeout=0.,
        )

    def interpret_response(self, data):
        """
        Converts the raw response from the device to the proper data type.

        :param bytes data:
            Received raw bytes from the read operation.
        :return:
            The measured temperature and humidity.

            - temperature (:py:class:`~sensirion_i2c_sht.sht3x.types.Temperature`) -
              Temperature response object.
            - humidity (:py:class:`~sensirion_i2c_sht.sht3x.types.Humidity`) -
              Humidity response object.
        :rtype:
            tuple
        """  # noqa: E501
        words = SensirionWordI2cCommand.interpret_response(self, data)
        return Temperature(words[0]), Humidity(words[1])


class Sht3xI2cCmdHeaterOn(Sht3xI2cCmdBase):
    """
    SHT3x command to enable the internal heater.
    """
    def __init__(self):
        """
        Constructs a new command.
        """
        super(Sht3xI2cCmdHeaterOn, self).__init__(
            command=0x306D,
            tx_words=[],
            rx_length=None,
            read_delay=0.,
            timeout=0.,
        )


class Sht3xI2cCmdHeaterOff(Sht3xI2cCmdBase):
    """
    SHT3x command to disable the internal heater.
    """
    def __init__(self):
        """
        Constructs a new command.
        """
        super(Sht3xI2cCmdHeaterOff, self).__init__(
            command=0x3066,
            tx_words=[],
            rx_length=None,
            read_delay=0.,
            timeout=0.,
        )


class Sht3xI2cCmdSoftReset(Sht3xI2cCmdBase):
    """
    SHT3x command for a soft reset.
    """
    def __init__(self):
        """
        Constructs a new command.
        """
        super(Sht3xI2cCmdSoftReset, self).__init__(
            command=0x30A2,
            tx_words=[],
            rx_length=None,
            read_delay=0.,
            timeout=0.,
        )


class Sht3xI2cCmdReadStatusRegister(Sht3xI2cCmdBase):
    """
    SHT3x command to read the status register.
    """
    def __init__(self):
        """
        Constructs a new command.
        """
        super(Sht3xI2cCmdReadStatusRegister, self).__init__(
            command=0xF32D,
            tx_words=[],
            rx_length=3,
            read_delay=0.,
            timeout=0.,
        )

    def interpret_response(self, data):
        """
        Converts the raw response from the device to the proper data type.

        :param bytes data:
            Received raw bytes from the read operation.
        :return: The status register.
        :rtype: :py:class:`~sensirion_i2c_sht.sht3x.types.StatusRegister`
        """
        words = SensirionWordI2cCommand.interpret_response(self, data)
        return StatusRegister(words[0])


class Sht3xI2cCmdResetStatusRegister(Sht3xI2cCmdBase):
    """
    SHT3x command to reset the status register.
    """
    def __init__(self):
        """
        Constructs a new command.
        """
        super(Sht3xI2cCmdResetStatusRegister, self).__init__(
            command=0x3041,
            tx_words=[],
            rx_length=None,
            read_delay=0.,
            timeout=0.,
        )
