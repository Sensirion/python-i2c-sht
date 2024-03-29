# -*- coding: utf-8 -*-
# (c) Copyright 2020 Sensirion AG, Switzerland

from __future__ import absolute_import, division, print_function
from sensirion_shdlc_driver import ShdlcSerialPort, ShdlcConnection
from sensirion_shdlc_sensorbridge import SensorBridgePort, \
    SensorBridgeShdlcDevice, SensorBridgeI2cProxy
from sensirion_i2c_driver import I2cConnection
from sensirion_i2c_sht.sht2x import Sht2xI2cDevice
from sensirion_i2c_sht.sht3x import Sht3xI2cDevice
from sensirion_i2c_sht.sht4x import Sht4xI2cDevice
import pytest

from sensirion_i2c_sht.shtc3 import Shtc3I2cDevice
from sensirion_i2c_sht.sts4x import Sts4xI2cDevice


def pytest_addoption(parser):
    """
    Register command line options
    """
    parser.addoption("--serial-port", action="store", type="string")
    parser.addoption("--serial-bitrate", action="store", type="int",
                     default=460800)


def _get_serial_port(config, validate=False):
    """
    Get the serial port to be used for the tests.
    """
    port = config.getoption("--serial-port")
    if (validate is True) and (port is None):
        raise ValueError("Please specify the serial port to be used with "
                         "the '--serial-port' argument.")
    return port


def _get_serial_bitrate(config):
    """
    Get the serial port bitrate to be used for the tests.
    """
    return config.getoption("--serial-bitrate")


def pytest_report_header(config):
    """
    Add extra information to test report header
    """
    lines = []
    lines.append("SensorBridge serial port: " + str(_get_serial_port(config)))
    lines.append("SensorBridge serial bitrate: " +
                 str(_get_serial_bitrate(config)))
    return '\n'.join(lines)


@pytest.fixture(scope="session")
def bridge(request):
    serial_port = _get_serial_port(request.config, validate=True)
    serial_bitrate = _get_serial_bitrate(request.config)
    with ShdlcSerialPort(serial_port, serial_bitrate) as port:
        dev = SensorBridgeShdlcDevice(ShdlcConnection(port), slave_address=0)
        yield dev


@pytest.fixture
def sht2x(bridge):
    # Configure SensorBridge port 1 for SHT2x
    bridge.set_i2c_frequency(SensorBridgePort.ONE, frequency=100e3)
    bridge.set_supply_voltage(SensorBridgePort.ONE, voltage=3.3)
    bridge.switch_supply_on(SensorBridgePort.ONE)

    # Create SHT2x device
    i2c_transceiver = SensorBridgeI2cProxy(bridge, port=SensorBridgePort.ONE)
    sht2x = Sht2xI2cDevice(I2cConnection(i2c_transceiver))

    yield sht2x

    # make sure the channel is powered off after executing tests
    bridge.switch_supply_off(SensorBridgePort.ONE)


@pytest.fixture
def sht3x(bridge):
    # Configure SensorBridge port 1 for SHT3x
    bridge.set_i2c_frequency(SensorBridgePort.ONE, frequency=100e3)
    bridge.set_supply_voltage(SensorBridgePort.ONE, voltage=3.3)
    bridge.switch_supply_on(SensorBridgePort.ONE)

    # Create SHT3x device
    i2c_transceiver = SensorBridgeI2cProxy(bridge, port=SensorBridgePort.ONE)
    sht3x = Sht3xI2cDevice(I2cConnection(i2c_transceiver))

    yield sht3x

    # make sure the channel is powered off after executing tests
    bridge.switch_supply_off(SensorBridgePort.ONE)


@pytest.fixture
def sht4x(bridge):
    # Configure SensorBridge port 1 for SHT4x
    bridge.set_i2c_frequency(SensorBridgePort.ONE, frequency=100e3)
    bridge.set_supply_voltage(SensorBridgePort.ONE, voltage=3.3)
    bridge.switch_supply_on(SensorBridgePort.ONE)

    # Create SHT4x device
    i2c_transceiver = SensorBridgeI2cProxy(bridge, port=SensorBridgePort.ONE)
    sht4x = Sht4xI2cDevice(I2cConnection(i2c_transceiver))

    yield sht4x

    # make sure the channel is powered off after executing tests
    bridge.switch_supply_off(SensorBridgePort.ONE)


@pytest.fixture
def sts4x(bridge):
    # Configure SensorBridge port 1 for STS4x
    bridge.set_i2c_frequency(SensorBridgePort.ONE, frequency=100e3)
    bridge.set_supply_voltage(SensorBridgePort.ONE, voltage=3.3)
    bridge.switch_supply_on(SensorBridgePort.ONE)

    # Create STS4x device
    i2c_transceiver = SensorBridgeI2cProxy(bridge, port=SensorBridgePort.ONE)
    sts4x = Sts4xI2cDevice(I2cConnection(i2c_transceiver))

    yield sts4x

    # make sure the channel is powered off after executing tests
    bridge.switch_supply_off(SensorBridgePort.ONE)


@pytest.fixture
def shtc3(bridge):
    # Configure SensorBridge port 1 for SHTC3
    bridge.set_i2c_frequency(SensorBridgePort.ONE, frequency=100e3)
    bridge.set_supply_voltage(SensorBridgePort.ONE, voltage=3.3)
    bridge.switch_supply_on(SensorBridgePort.ONE)

    # Create SHTC3 device
    i2c_transceiver = SensorBridgeI2cProxy(bridge, port=SensorBridgePort.ONE)
    shtc3 = Shtc3I2cDevice(I2cConnection(i2c_transceiver))

    yield shtc3

    # make sure the channel is powered off after executing tests
    bridge.switch_supply_off(SensorBridgePort.ONE)
