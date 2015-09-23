import sh
import logging
from sanji.model import Model
from voluptuous import Schema, REMOVE_EXTRA, Any

_logger = logging.getLogger("sanji.serial")

SERIAL_SCHEMA = Schema({
    "id": int,
    "dev": str,
    "devDisplayName": str,
    "mode": Any("rs232", "rs485-2w", "rs422/rs485-4w")
}, extra=REMOVE_EXTRA)

SERIAL_MODE = {
    "rs232": 0,
    "rs485-2w": 1,
    "rs422/rs485-4w": 2
}


class Serial(dict):
    def set_mode(self):
        _logger.debug("Set serial:%s mode:%s" % (self["dev"], self["mode"]))
        out = sh.setinterface(self["dev"], SERIAL_MODE[self["mode"]])
        return out


class Serials(Model):
    def __init__(self, *args, **kwargs):
        kwargs["schema"] = SERIAL_SCHEMA
        kwargs["model_cls"] = Serial
        super(Serials, self).__init__(*args, **kwargs)

    def set_all(self):
        for serial in self.getAll():
            serial.set_mode()

    def update(self, id, newObj):
        """Update an exist serial,\
           it will set serial mode if update successfully
           Returns:
               newSerial(serial): udpated serial
           Raises:
               ValueError: if device list contains invaild entry
        """
        serial = self.get(id)
        if serial is None:
            return None

        newSerial = super(Serials, self).update(
            id=id, newObj={"mode": newObj["mode"]})

        if newSerial:
            newSerial.set_mode()

        return newSerial
