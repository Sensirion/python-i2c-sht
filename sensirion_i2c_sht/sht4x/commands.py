# -*- coding: utf-8 -*-
# (c) Copyright 2021 Sensirion AG, Switzerland

from __future__ import absolute_import, division, print_function
from sensirion_i2c_driver import SensirionI2cCommand, CrcCalculator
from .response_types import Sht4xTemperature, Sht4xHumidity
from struct import unpack


class Sht4xI2cCmdBase(SensirionI2cCommand):
    """
    SHT4x I²C base command.
    """
    def __init__(self, command, tx_data, rx_length, read_delay,
                 post_processing_time=0.0):
        """
        Constructs a new SHT4x I²C command.

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
        super(Sht4xI2cCmdBase, self).__init__(
            command=command,
            tx_data=tx_data,
            rx_length=rx_length,
            read_delay=read_delay,
            timeout=0.0,  # SHT4x does not support clock stretching
            crc=CrcCalculator(8, 0x31, 0xFF),
            command_bytes=1,
            post_processing_time=post_processing_time,
        )


class Sht4xI2cCmdMeasBase(Sht4xI2cCmdBase):
    """
    Base SHT4x command for a single shot measurement.
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
        super(Sht4xI2cCmdMeasBase, self).__init__(
            command=command,
            tx_data=b'',
            rx_length=6,
            read_delay=read_delay,
        )

    def interpret_response(self, data):
        """
        Converts the raw response from the device to the proper data type.

        :param bytes data:
            Received raw bytes from the read operation.
        :return:
            The measured temperature and humidity.

            - temperature (:py:class:`~sensirion_i2c_sht.sht4x.response_types.Sht4xTemperature`) -
              Temperature response object.
            - humidity (:py:class:`~sensirion_i2c_sht.sht4x.response_types.Sht4xHumidity`) -
              Humidity response object.
        :rtype:
            tuple
        """  # noqa: E501
        checked_data = SensirionI2cCommand.interpret_response(self, data)
        temperature_ticks, humidity_ticks = unpack(">2H", checked_data)
        return Sht4xTemperature(temperature_ticks), \
            Sht4xHumidity(humidity_ticks)


class Sht4xI2cCmdMeasHighRes(Sht4xI2cCmdMeasBase):
    """
    SHT4x command for a single shot measurement with high repeatability.
    """
    def __init__(self):
        """
        Constructs a new command.
        """
        super(Sht4xI2cCmdMeasHighRes, self).__init__(
            command=0xFD,
            read_delay=0.009,
        )


class Sht4xI2cCmdMeasMediumRes(Sht4xI2cCmdMeasBase):
    """
    SHT4x command for a single shot measurement with medium repeatability.
    """
    def __init__(self):
        """
        Constructs a new command.
        """
        super(Sht4xI2cCmdMeasMediumRes, self).__init__(
            command=0xF6,
            read_delay=0.005,
        )


class Sht4xI2cCmdMeasLowRes(Sht4xI2cCmdMeasBase):
    """
    SHT4x command for a single shot measurement with low repeatability.
    """
    def __init__(self):
        """
        Constructs a new command.
        """
        super(Sht4xI2cCmdMeasLowRes, self).__init__(
            command=0xE0,
            read_delay=0.002,
        )


class Sht4xI2cCmdHeaterHighPowerLong(Sht4xI2cCmdMeasBase):
    """
    SHT4x command activate highest heater power and a high precision
    measurement (typ. 200mW @ 3.3V) for 1 second.
    """
    def __init__(self):
        """
        Constructs a new command.
        """
        super(Sht4xI2cCmdHeaterHighPowerLong, self).__init__(
            command=0x39,
            read_delay=1.109,
        )


class Sht4xI2cCmdHeaterHighPowerShort(Sht4xI2cCmdMeasBase):
    """
    SHT4x command activate highest heater power and a high precision
    measurement (typ. 200mW @ 3.3V) for 0.1 second.
    """
    def __init__(self):
        """
        Constructs a new command.
        """
        super(Sht4xI2cCmdHeaterHighPowerShort, self).__init__(
            command=0x32,
            read_delay=0.119,
        )


class Sht4xI2cCmdHeaterMediumPowerLong(Sht4xI2cCmdMeasBase):
    """
    SHT4x command activate medium heater power and a high precision
    measurement (typ. 110mW @ 3.3V) for 1 second.
    """
    def __init__(self):
        """
        Constructs a new command.
        """
        super(Sht4xI2cCmdHeaterMediumPowerLong, self).__init__(
            command=0x2F,
            read_delay=1.109,
        )


class Sht4xI2cCmdHeaterMediumPowerShort(Sht4xI2cCmdMeasBase):
    """
    SHT4x command activate medium heater power and a high precision
    measurement (typ. 110mW @ 3.3V) for 0.1 second.
    """
    def __init__(self):
        """
        Constructs a new command.
        """
        super(Sht4xI2cCmdHeaterMediumPowerShort, self).__init__(
            command=0x24,
            read_delay=0.119,
        )


class Sht4xI2cCmdHeaterLowPowerLong(Sht4xI2cCmdMeasBase):
    """
    SHT4x command activate lowest heater power and a high precision
    measurement (typ. 20mW @ 3.3V) for 1 second.
    """
    def __init__(self):
        """
        Constructs a new command.
        """
        super(Sht4xI2cCmdHeaterLowPowerLong, self).__init__(
            command=0x1E,
            read_delay=1.109,
        )


class Sht4xI2cCmdHeaterLowPowerShort(Sht4xI2cCmdMeasBase):
    """
    SHT4x command activate lowest heater power and a high precision
    measurement (typ. 20mW @ 3.3V) for 0.1 second.
    """
    def __init__(self):
        """
        Constructs a new command.
        """
        super(Sht4xI2cCmdHeaterLowPowerShort, self).__init__(
            command=0x15,
            read_delay=0.119,
        )


class Sht4xI2cCmdSoftReset(Sht4xI2cCmdBase):
    """
    SHT4x command for a soft reset.
    """
    def __init__(self):
        """
        Constructs a new command.
        """
        super(Sht4xI2cCmdSoftReset, self).__init__(
            command=0x94,
            tx_data=b'',
            rx_length=None,
            read_delay=0.,
            post_processing_time=0.001,
        )


class Sht4xI2cCmdReadSerial(Sht4xI2cCmdBase):
    """
    SHT4x command to read the serial number.
    """
    def __init__(self):
        """
        Constructs a new command.
        """
        super(Sht4xI2cCmdReadSerial, self).__init__(
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
        checked_data = Sht4xI2cCmdBase.interpret_response(self, data)
        words = unpack(">2H", checked_data)
        return words[0] * 65536 + words[1]
