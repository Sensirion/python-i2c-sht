# -*- coding: utf-8 -*-
# (c) Copyright 2020 Sensirion AG, Switzerland

from __future__ import absolute_import, division, print_function
from sensirion_i2c_driver import SensirionI2cCommand, CrcCalculator, I2cCommand
from sensirion_i2c_driver.errors import I2cChecksumError
from .response_types import Sht2xTemperature, Sht2xHumidity
from struct import unpack


class Sht2xI2cCmdBase(SensirionI2cCommand):
    """
    Sht2x I²C base command.
    """
    def __init__(self, command, tx_data, rx_length, read_delay, timeout,
                 command_bytes=1, post_processing_time=0.0):
        """
        Constructs a new SHT2x I²C command.

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
        :param float timeout:
            Timeout (in Seconds) to be used in case of clock stretching. If the
            device stretches the clock longer than this value, the transceive
            operation will be aborted with a timeout error. Set to 0.0 to
            indicate that the device will not stretch the clock for this
            command.
        :param int command_bytes:
            Number of command bytes.
        :param float post_processing_time:
            Maximum time in seconds the device needs for post processing of
            this command until it is ready to receive the next command. For
            example after a device reset command, the device might need some
            time until it is ready again. Usually this is 0.0s, i.e. no post
            processing is needed.
        """
        super(Sht2xI2cCmdBase, self).__init__(
            command=command,
            tx_data=tx_data,
            rx_length=rx_length,
            read_delay=read_delay,
            timeout=timeout,
            crc=CrcCalculator(8, 0x31, 0x00),
            command_bytes=command_bytes,
            post_processing_time=post_processing_time,
        )


class Sht2xI2cMeasureHumidity(Sht2xI2cCmdBase):
    """
    Sht2x command for a single shot measurement with clock stretching disabled.
    """
    def __init__(self):
        """
        Constructs a new command.
        """
        super(Sht2xI2cMeasureHumidity, self).__init__(
            command=0xF5,
            tx_data=b'',
            rx_length=3,
            read_delay=0.029,
            timeout=0,
        )

    def interpret_response(self, data):
        """
        Converts the raw response from the device to the proper data type.

        :param bytes data: Received raw bytes from the read operation.
        :return: The read humidity.
        :rtype: :py:class:`~sensirion_i2c_sht.sht2x.response_types.Sht2xHumidity`
        """  # noqa: E501
        checked_data = SensirionI2cCommand.interpret_response(self, data)
        return Sht2xHumidity(unpack(">H", checked_data)[0])


class Sht2xI2cMeasureTemperature(Sht2xI2cCmdBase):
    """
    Sht2x command for a single shot measurement with clock stretching disabled.
    """
    def __init__(self):
        """
        Constructs a new command.
        """
        super(Sht2xI2cMeasureTemperature, self).__init__(
            command=0xF3,
            tx_data=b'',
            rx_length=3,
            read_delay=0.085,
            timeout=0,
        )

    def interpret_response(self, data):
        """
        Converts the raw response from the device to the proper data type.

        :param bytes data: Received raw bytes from the read operation.
        :return: The read temperature.
        :rtype: :py:class:`~sensirion_i2c_sht.sht2x.response_types.Sht2xTemperature`
        """  # noqa: E501
        checked_data = SensirionI2cCommand.interpret_response(self, data)
        return Sht2xTemperature(unpack(">H", checked_data)[0])


class Sht2xI2cCmdSoftReset(Sht2xI2cCmdBase):
    """
    Sht2x command for a soft reset.
    """
    def __init__(self):
        """
        Constructs a new command.
        """
        super(Sht2xI2cCmdSoftReset, self).__init__(
            command=0xFE,
            tx_data=b'',
            rx_length=None,
            read_delay=0.,
            timeout=0.,
            post_processing_time=0.015,
        )


class Sht2xI2cCmdReadOtp(I2cCommand):
    """
    Sht2x command to read from the OTP.
    """
    def __init__(self, address, number_of_bytes_to_read):
        """
        Constructs a new command.

        :param byte address: Address of OTP to read from.
        :param int number_of_bytes_to_read: Number of bytes to read.
        """
        super(Sht2xI2cCmdReadOtp, self).__init__(
            tx_data=[0xFA, address],
            rx_length=number_of_bytes_to_read * 2,
            read_delay=0., timeout=0.
        )
        self._crc = CrcCalculator(8, 0x31, 0x00)

    def interpret_response(self, data):
        """
        Converts the raw response from the device to the proper data type.

        :param bytes data: Received raw bytes from the read operation.
        :return: The read bytes from the OTP.
        :rtype: list(int)
        """
        data = bytearray(data)  # Python 2 compatibility
        otp_bytes = []
        # Each byte is followed by a crc
        for i in range(len(data)):
            if i % 2 == 0:
                otp_bytes.append(data[i])
            else:
                received_crc = data[i]
                expected_crc = self._crc(data[i - 1:i])
                if received_crc != expected_crc:
                    raise I2cChecksumError(received_crc, expected_crc, data)
        return otp_bytes


class Sht2xI2cCmdReadMetalRom(Sht2xI2cCmdBase):
    """
    Sht2x command to read from the metal ROM.
    """
    def __init__(self, number_of_words_to_read):
        """
        Constructs a new command.

        :param int number_of_words_to_read: Number of words to read.
        """
        super(Sht2xI2cCmdReadMetalRom, self).__init__(
            command=0xFCC9,
            tx_data=b'',
            rx_length=3 * number_of_words_to_read,
            read_delay=0.,
            timeout=0.,
            command_bytes=2,
        )

    def interpret_response(self, data):
        """
        Converts the raw response from the device to the proper data type.

        :param bytes data: Received raw bytes from the read operation.
        :return: The read words from the metal ROM.
        :rtype: list(int)
        """
        checked_data = SensirionI2cCommand.interpret_response(self, data)
        n_words = int(len(checked_data) / 2)
        words = unpack(">{}H".format(n_words), checked_data)
        return words
