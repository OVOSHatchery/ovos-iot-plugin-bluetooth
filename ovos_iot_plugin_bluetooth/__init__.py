import bluetooth

from ovos_plugin_manager.templates.iot import IOTDevicePlugin, IOTScannerPlugin


class BluetoothDevice(IOTDevicePlugin):
    def __init__(self, device_id, host, name="generic bluetooth device", raw_data=None):
        device_id = device_id or f"bluetooth:{host}"
        raw_data = raw_data or {"name": name, "description": "bluetooth device"}
        super().__init__(device_id, host, name, raw_data)

    @property
    def as_dict(self):
        return {
            "host": self.host,
            "name": self.name,
            "model": self.product_model,
            "device_type": "generic bluetooth device",
            "device_id": self.device_id,
            "state": self.is_on,
            "raw": self.raw_data
        }

    @property
    def product_model(self):
        return self.raw_data.get("model", "bluetooth")

    @property
    def device_id(self):
        return self.raw_data.get("deviceId")

    @property
    def name(self):
        return self.raw_data["alias"]


class BluetoothPlugin(IOTScannerPlugin):
    def scan(self):
        for addr, name in bluetooth.discover_devices(lookup_names=True):
            device_id = f"{name}:{addr}"
            yield BluetoothDevice(device_id, addr, name, {"address": addr, "name": name, "device_type": "bluetooth"})

    def get_device(self, ip):
        # NOTE: for bluetooth this is the MAC address, not IP
        for device in self.scan():
            if device.host == ip:
                return device
        return None


if __name__ == "__main__":
    from pprint import pprint

    for host in BluetoothPlugin().scan():
        pprint(host.as_dict)
