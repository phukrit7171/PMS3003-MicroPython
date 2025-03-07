from machine import UART
import time

class PMS3003:
    def __init__(self, uart_id=2, baudrate=9600, tx=17, rx=16, timeout=3000):
        """
        Initialize the PMS3003 sensor.
        :param uart_id: UART interface ID (default: 2)
        :param baudrate: Baud rate (default: 9600)
        :param tx: TX pin (default: 17)
        :param rx: RX pin (default: 16)
        :param timeout: Read timeout in milliseconds (default: 3000)
        """
        self.uart = UART(uart_id, baudrate=baudrate, tx=tx, rx=rx, timeout=timeout)
        time.sleep(1)  # Allow sensor to stabilize

    def read_data(self):
        """Read and parse data from PMS3003 sensor."""
        if self.uart.any():  # Check if data is available
            data = self.uart.read(32)  # Read 32 bytes (frame size)
            if data and len(data) == 32 and data[0] == 0x42 and data[1] == 0x4D:
                pm1_0 = (data[4] << 8) | data[5]
                pm2_5 = (data[6] << 8) | data[7]
                pm10  = (data[8] << 8) | data[9]
                return {
                    "PM1.0": pm1_0,
                    "PM2.5": pm2_5,
                    "PM10": pm10
                }
            else:
                return None  # Invalid data received
        return None  # No data available
    
    def toString(self, data):
        """Convert sensor data to a formatted string."""
        if data:
            return f"PM1.0: {data['PM1.0']} µg/m³, PM2.5: {data['PM2.5']} µg/m³, PM10: {data['PM10']} µg/m³"
        return "No valid data received"

if __name__ == "__main__":
    sensor = PMS3003()
    result = sensor.read_data()
    print(sensor.toString(result))

