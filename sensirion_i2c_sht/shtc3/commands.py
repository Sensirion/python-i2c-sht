# -*- coding: utf-8 -*-
# (c) Copyright 2021 Sensirion AG, Switzerland

from __future__ import absolute_import, division, print_function

import logging
from struct import unpack

from sensirion_i2c_driver import SensirionI2cCommand, CrcCalculator
from .response_types import Shtc3Temperature, Shtc3Humidity

log = logging.getLogger(__name__)


class Shtc3I2cCmdBase(SensirionI2cCommand):
    """
    shtc3 I²C base command.
    """

    def __init__(self, command, tx_data, rx_length, read_delay, timeout,
                 post_processing_time=0.0):
        """
        Constructs a new shtc3 I²C command.

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
        :param float post_processing_time:
            Maximum time in seconds the device needs for post processing of
            this command until it is ready to receive the next command. For
            example after a device reset command, the device might need some
            time until it is ready again. Usually this is 0.0s, i.e. no post
            processing is needed.
        """
        super(Shtc3I2cCmdBase, self).__init__(
            command=command,
            tx_data=tx_data,
            rx_length=rx_length,
            read_delay=read_delay,
            timeout=timeout,
            crc=CrcCalculator(8, 0x31, 0xFF, 0x00),
            command_bytes=2,
            post_processing_time=post_processing_time,
        )


class Shtc3I2cCmdMeasureNormalModeTicksClockStretching(Shtc3I2cCmdBase):
    """
    Measure Normal Mode Ticks Clock Stretching I²C Command

    Measure in normal mode with clock stretching enabled.
    """

    def __init__(self):
        """
        Constructor.
        """
        super(Shtc3I2cCmdMeasureNormalModeTicksClockStretching, self).__init__(
            command=0x7CA2,
            tx_data=None,
            rx_length=6,
            read_delay=0.013,
            timeout=0,
            post_processing_time=0.0,
        )

    def interpret_response(self, data):
        """
        Validates the CRCs of the received data from the device and returns
        the interpreted data.

        :param bytes data:
            Received raw bytes from the read operation.
        :return:
            - temperature (:py:class:`~sensirion_i2c_sht.shtc3.response_types.Shtc3xTemperature`) -
              Temperature response object.
            - humidity (:py:class:`~sensirion_i2c_sht.shtc3.response_types.Shtc3Humidity`) -
              Humidity response object.
        :rtype: tuple
        :raise ~sensirion_i2c_driver.errors.I2cChecksumError:
            If a received CRC was wrong.
        """
        # check and remove CRCs
        checked_data = Shtc3I2cCmdBase.interpret_response(self, data)

        # convert raw received data into proper data types
        temperature_ticks = int(unpack(">H", checked_data[0:2])[0])  # uint16
        humidity_ticks = int(unpack(">H", checked_data[2:4])[0])  # uint16
        return Shtc3Temperature(temperature_ticks), Shtc3Humidity(humidity_ticks)


class Shtc3I2cCmdMeasureLowestPowerModeTicksClockStretching(Shtc3I2cCmdBase):
    """
    Measure Lowest Power Mode Ticks Clock Stretching I²C Command

    Measure in low power mode with clock stretching enabled.
    """

    def __init__(self):
        """
        Constructor.
        """
        super(Shtc3I2cCmdMeasureLowestPowerModeTicksClockStretching, self).__init__(
            command=0x6458,
            tx_data=None,
            rx_length=6,
            read_delay=0.001,
            timeout=0,
            post_processing_time=0.0,
        )

    def interpret_response(self, data):
        """
        Validates the CRCs of the received data from the device and returns
        the interpreted data.

        :param bytes data:
            Received raw bytes from the read operation.
        :return:
            - temperature (:py:class:`~sensirion_i2c_sht.shtc3.response_types.Shtc3xTemperature`) -
              Temperature response object.
            - humidity (:py:class:`~sensirion_i2c_sht.shtc3.response_types.Shtc3Humidity`) -
              Humidity response object.
        :rtype: tuple
        :raise ~sensirion_i2c_driver.errors.I2cChecksumError:
            If a received CRC was wrong.
        """
        # check and remove CRCs
        checked_data = Shtc3I2cCmdBase.interpret_response(self, data)

        # convert raw received data into proper data types
        temperature_ticks = int(unpack(">H", checked_data[0:2])[0])  # uint16
        humidity_ticks = int(unpack(">H", checked_data[2:4])[0])  # uint16
        return Shtc3Temperature(temperature_ticks), Shtc3Humidity(humidity_ticks)


class Shtc3I2cCmdMeasureNormalModeTicks(Shtc3I2cCmdBase):
    """
    Measure Normal Mode Ticks I²C Command

    Measure in normal mode with clock stretching disabled.
    """

    def __init__(self):
        """
        Constructor.
        """
        super(Shtc3I2cCmdMeasureNormalModeTicks, self).__init__(
            command=0x7866,
            tx_data=None,
            rx_length=6,
            read_delay=0.013,
            timeout=0,
            post_processing_time=0.0,
        )

    def interpret_response(self, data):
        """
        Validates the CRCs of the received data from the device and returns
        the interpreted data.

        :param bytes data:
            Received raw bytes from the read operation.
        :return:
            - temperature (:py:class:`~sensirion_i2c_sht.shtc3.response_types.Shtc3xTemperature`) -
              Temperature response object.
            - humidity (:py:class:`~sensirion_i2c_sht.shtc3.response_types.Shtc3Humidity`) -
              Humidity response object.
        :rtype: tuple
        :raise ~sensirion_i2c_driver.errors.I2cChecksumError:
            If a received CRC was wrong.
        """
        # check and remove CRCs
        checked_data = Shtc3I2cCmdBase.interpret_response(self, data)

        # convert raw received data into proper data types
        temperature_ticks = int(unpack(">H", checked_data[0:2])[0])  # uint16
        humidity_ticks = int(unpack(">H", checked_data[2:4])[0])  # uint16
        return Shtc3Temperature(temperature_ticks), Shtc3Humidity(humidity_ticks)


class Shtc3I2cCmdMeasureLowestPowerModeTicks(Shtc3I2cCmdBase):
    """
    Measure Lowest Power Mode Ticks I²C Command

    Measure in low power mode with clock stretching disabled.
    """

    def __init__(self):
        """
        Constructor.
        """
        super(Shtc3I2cCmdMeasureLowestPowerModeTicks, self).__init__(
            command=0x609C,
            tx_data=None,
            rx_length=6,
            read_delay=0.001,
            timeout=0,
            post_processing_time=0.0,
        )

    def interpret_response(self, data):
        """
        Validates the CRCs of the received data from the device and returns
        the interpreted data.

        :param bytes data:
            Received raw bytes from the read operation.
        :return:
            - temperature (:py:class:`~sensirion_i2c_sht.shtc3.response_types.Shtc3xTemperature`) -
              Temperature response object.
            - humidity (:py:class:`~sensirion_i2c_sht.shtc3.response_types.Shtc3Humidity`) -
              Humidity response object.
        :rtype: tuple
        :raise ~sensirion_i2c_driver.errors.I2cChecksumError:
            If a received CRC was wrong.
        """
        # check and remove CRCs
        checked_data = Shtc3I2cCmdBase.interpret_response(self, data)

        # convert raw received data into proper data types
        temperature_ticks = int(unpack(">H", checked_data[0:2])[0])  # uint16
        humidity_ticks = int(unpack(">H", checked_data[2:4])[0])  # uint16
        return Shtc3Temperature(temperature_ticks), Shtc3Humidity(humidity_ticks)


class Shtc3I2cCmdProductId(Shtc3I2cCmdBase):
    """
    Product Id I²C Command

    Read out the product id.

    .. note:: The SHTC3 has an ID register which contains an SHTC3- specific
              product code. The read-out of the ID register can be used to
              verify the presence of the sensor and proper communication.
    """

    def __init__(self):
        """
        Constructor.
        """
        super(Shtc3I2cCmdProductId, self).__init__(
            command=0xEFC8,
            tx_data=None,
            rx_length=3,
            read_delay=0.001,
            timeout=0,
            post_processing_time=0.0,
        )

    def interpret_response(self, data):
        """
        Validates the CRCs of the received data from the device and returns
        the interpreted data.

        :param bytes data:
            Received raw bytes from the read operation.
        :return: SHTC3-specific product code
        :rtype: int
        :raise ~sensirion_i2c_driver.errors.I2cChecksumError:
            If a received CRC was wrong.
        """
        # check and remove CRCs
        checked_data = Shtc3I2cCmdBase.interpret_response(self, data)

        # convert raw received data into proper data types
        product_id = int(unpack(">H", checked_data[0:2])[0]) & 0x083F  # uint16
        return product_id


class Shtc3I2cCmdSoftReset(Shtc3I2cCmdBase):
    """
    Soft Reset I²C Command

    Perform a soft reset. reset all internal state machines and reload
    calibration data from the memory.

    .. note:: A reset of the sensor can be achieved in three ways: • Soft
              reset: use this function • I2C general call: all devices on the
              I2C bus are reset by sending the command 0x06 to the I2C address
              0x00. • Power down (incl.pulling SCL and SDA low)
    """

    def __init__(self):
        """
        Constructor.
        """
        super(Shtc3I2cCmdSoftReset, self).__init__(
            command=0x805D,
            tx_data=None,
            rx_length=None,
            read_delay=0.0,
            timeout=0,
            post_processing_time=0.001,
        )


class Shtc3I2cCmdWakeUp(Shtc3I2cCmdBase):
    """
    Wake Up I²C Command

    Wake-up command of the sensor.

    .. note:: When the sensor is in sleep mode, it requires the
              wake-up command before any further communication
    """

    def __init__(self):
        """
        Constructor.
        """
        super(Shtc3I2cCmdWakeUp, self).__init__(
            command=0x3517,
            tx_data=None,
            rx_length=None,
            read_delay=0.0,
            timeout=0,
            post_processing_time=0.001,
        )


class Shtc3I2cCmdSleep(Shtc3I2cCmdBase):
    """
    Sleep I²C Command

    Sleep command of the sensor.

    .. note:: Upon VDD reaching the power-up voltage level V_POR , the SHTC3
              enters the idle state after a duration of 240us. After that,
              the sensor should be set to sleep.
    """

    def __init__(self):
        """
        Constructor.
        """
        super(Shtc3I2cCmdSleep, self).__init__(
            command=0xB098,
            tx_data=None,
            rx_length=None,
            read_delay=0.0,
            timeout=0,
        )
