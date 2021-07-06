# -*- coding: utf-8 -*-
# (c) Copyright 2021 Sensirion AG, Switzerland

from __future__ import absolute_import, division, print_function
from sensirion_i2c_driver import SensirionI2cCommand, CrcCalculator
from .response_types import Sts4xTemperature
from struct import unpack


class Sts4xI2cCmdBase(SensirionI2cCommand):
    """
    STS4x I²C base command.
    """
    def __init__(self, command, tx_data, rx_length, read_delay,
                 post_processing_time=0.0):
        """
        Constructs a new STS4x I²C command.

        :param int/None command:
            The command ID to be sent to the device. None means that no
            command will be sent, i.e. only ``tx_data`` (if not None) will
            be sent. No CRC is added to these bytes since the command ID
            usually already contains a CRC.
        :param bytes-like/list/None tx_data:
            Bytes to be extended with CRCs and then sent to the I²C device.
            None means that no write header will be sent at all (if ``command``
            is None too). An empty list means to send the write header (even if
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
        :param float post_processing_time:
            Maximum time in seconds the device needs for post processing of
            this command until it is ready to receive the next command. For
            example after a device reset command, the device might need some
            time until it is ready again. Usually this is 0.0s, i.e. no post
            processing is needed.
        """
        super(Sts4xI2cCmdBase, self).__init__(
            command=command,
            tx_data=tx_data,
            rx_length=rx_length,
            read_delay=read_delay,
            timeout=0.0,  # STS4x does not support clock stretching
            crc=CrcCalculator(8, 0x31, 0xFF),
            command_bytes=1,
            post_processing_time=post_processing_time,
        )


class Sts4xI2cCmdMeasBase(Sts4xI2cCmdBase):
    """
    Base STS4x command for a single shot measurement.
    """
    def __init__(self, command, read_delay):
        """
        Constructs a new command.

        :param int/None command:
            The command word to be sent to the device. None means that no
            command will be sent, i.e. only ``tx_words`` (if not None) will
            be sent.
        :param float read_delay:
            Delay (in Seconds) to be inserted between the end of the write
            operation and the beginning of the read operation. This is needed
            if the device needs some time to prepare the RX data, e.g. if it
            has to perform a measurement. Set to 0.0 to indicate that no delay
            is needed, i.e. the device does not need any processing time.
        """
        super(Sts4xI2cCmdMeasBase, self).__init__(
            command=command,
            tx_data=b'',
            rx_length=3,
            read_delay=read_delay,
        )

    def interpret_response(self, data):
        """
        Converts the raw response from the device to the proper data type.

        :param bytes data:
            Received raw bytes from the read operation.
        :return:
            The measured temperature.

            - temperature (:py:class:`~sensirion_i2c_sht.sts4x.response_types.Sts4xTemperature`) -
              Temperature response object.
        :rtype:
            :py:class:`~sensirion_i2c_sht.sts4x.response_types.Sts4xTemperature`
        """  # noqa: E501

        checked_data = SensirionI2cCommand.interpret_response(self, data)
        temperature_ticks, = unpack(">H", checked_data)
        return Sts4xTemperature(temperature_ticks)


class Sts4xI2cCmdMeasHighRes(Sts4xI2cCmdMeasBase):
    """
    STS4x command for a single shot measurement with high repeatability.
    """
    def __init__(self):
        """
        Constructs a new command.
        """
        super(Sts4xI2cCmdMeasHighRes, self).__init__(
            command=0xFD,
            read_delay=0.009,
        )


class Sts4xI2cCmdMeasMediumRes(Sts4xI2cCmdMeasBase):
    """
    STS4x command for a single shot measurement with medium repeatability.
    """
    def __init__(self):
        """
        Constructs a new command.
        """
        super(Sts4xI2cCmdMeasMediumRes, self).__init__(
            command=0xF6,
            read_delay=0.005,
        )


class Sts4xI2cCmdMeasLowRes(Sts4xI2cCmdMeasBase):
    """
    STS4x command for a single shot measurement with low repeatability.
    """
    def __init__(self):
        """
        Constructs a new command.
        """
        super(Sts4xI2cCmdMeasLowRes, self).__init__(
            command=0xE0,
            read_delay=0.002,
        )


class Sts4xI2cCmdSoftReset(Sts4xI2cCmdBase):
    """
    STS4x command for a soft reset.
    """
    def __init__(self):
        """
        Constructs a new command.
        """
        super(Sts4xI2cCmdSoftReset, self).__init__(
            command=0x94,
            tx_data=b'',
            rx_length=None,
            read_delay=0.,
            post_processing_time=0.001,
        )


class Sts4xI2cCmdReadSerial(Sts4xI2cCmdBase):
    """
    STS4x command to read the serial number.
    """
    def __init__(self):
        """
        Constructs a new command.
        """
        super(Sts4xI2cCmdReadSerial, self).__init__(
            command=0x89,
            tx_data=b'',
            rx_length=6,
            read_delay=0.001,
        )

    def interpret_response(self, data):
        """
        Converts the raw response from the device to the proper data type.

        :param bytes data:
            Received raw bytes from the read operation.
        :return: The serial number.
        :rtype: int
        """
        checked_data = Sts4xI2cCmdBase.interpret_response(self, data)
        words = unpack(">2H", checked_data)
        return words[0] * 65536 + words[1]
