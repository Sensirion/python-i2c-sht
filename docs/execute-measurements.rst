Install the SHT Driver
--------------------------

.. include:: driver-installation.rst


Use the SensorBridge on Windows
-------------------------------

1. Install the driver for the `Sensirion SEK-SensorBridge`_:

   .. code-block:: console

      python -m pip install sensirion-shdlc-sensorbridge

2. Connect the SEK-SensorBridge to your PC over USB.

   If the SEK-SensorBridge is not detected by your system, follow the
   `SensorBridge FTDI Driver Installation`_.

3. Connect the SHT sensor to the SEK-SensorBridge.

4. Run an example script in the activated virtual environment.

   By default, the script assumes that the SensorBridge is connected to the
   ``COM1`` serial port. If a different port is used, specify it with the
   ``--serial-port`` parameter:

   .. code-block:: console

        python examples/example_usage_sensorbridge_s.py --serial-port <your COM port>


.. _Sensirion SEK-SensorBridge: https://developer.sensirion.com/product-support/sek-sensorbridge/
.. _SensorBridge FTDI Driver Installation: https://sensirion.github.io/python-shdlc-sensorbridge/sensor-bridge-installation.html

Example script
~~~~~~~~~~~~~~

.. sourcecode:: python

    import time
    from sensirion_shdlc_driver import ShdlcSerialPort, ShdlcConnection
    from sensirion_shdlc_sensorbridge import SensorBridgePort, \
        SensorBridgeShdlcDevice, SensorBridgeI2cProxy
    from sensirion_i2c_driver import I2cConnection
    from sensirion_i2c_sht.sht3x import Sht3xI2cDevice

    # Connect to the SensorBridge with default settings:
    #  - baudrate:      460800
    #  - slave address: 0
    with ShdlcSerialPort(port='COM1', baudrate=460800) as port:
        bridge = SensorBridgeShdlcDevice(ShdlcConnection(port), slave_address=0)
        print("SensorBridge SN: {}".format(bridge.get_serial_number()))

        # Configure SensorBridge port 1 for SHT3x
        bridge.set_i2c_frequency(SensorBridgePort.ONE, frequency=100e3)
        bridge.set_supply_voltage(SensorBridgePort.ONE, voltage=3.3)
        bridge.switch_supply_on(SensorBridgePort.ONE)

        # Create SHT3x device
        i2c_transceiver = SensorBridgeI2cProxy(bridge, port=SensorBridgePort.ONE)
        sht3x = Sht3xI2cDevice(I2cConnection(i2c_transceiver))

        # Measure
        while True:
            temperature, humidity = sht3x.single_shot_measurement()
            # use default formatting for printing output:
            print("{}, {}".format(temperature, humidity))
            # custom printing of attributes:
            print("{:0.2f} °C ({} ticks), {:0.2f} %RH ({} ticks)".format(
                temperature.degrees_celsius, temperature.ticks,
                humidity.percent_rh, humidity.ticks))
            time.sleep(1.0)
