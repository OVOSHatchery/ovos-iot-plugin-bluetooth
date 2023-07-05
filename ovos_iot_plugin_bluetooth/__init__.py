import time

import bluetooth
from ovos_PHAL_plugin_commonIOT.opm.base import Sensor, IOTScannerPlugin


class BluetoothDevice(Sensor):
    def __init__(self, device_id, host, name="generic bluetooth device", raw_data=None):
        device_id = device_id or f"bluetooth:{host}"
        raw_data = raw_data or {"name": name, "description": "bluetooth device"}
        super().__init__(device_id, host, name, raw_data=raw_data)
        self.ttl = self.raw_data.get("keeptime", 30)

    @property
    def is_on(self):
        # if seen in last 30 seconds, report online
        if time.time() - self.raw_data.get("last_seen", 0) > self.ttl:
            return False
        return True


class BluetoothPlugin(IOTScannerPlugin):

    def scan(self):
        for addr, name in bluetooth.discover_devices(lookup_names=True):
            device_id = f"{name}:{addr}"
            ts = time.time()
            alias = self.aliases.get(device_id) or name
            dev = BluetoothDevice(device_id, addr, alias,
                                  raw_data={"address": addr,
                                            "last_seen": ts,
                                            "keeptime": self.ttl,
                                            "alias": alias,
                                            "name": name,
                                            "device_type": "bluetooth"})
            yield dev

    def get_device(self, ip):
        # NOTE: for bluetooth this is the MAC address, not IP
        for device in self.scan():
            if device.host == ip:
                return device
        return None

