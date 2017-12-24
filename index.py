#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import logging
from sanji.core import Sanji
from sanji.core import Route
from mxserial import Serials


_logger = logging.getLogger("sanji.serial.index")


class Index(Sanji):

    def init(self, *args, **kwargs):
        path_root = os.path.abspath(os.path.dirname(__file__))
        self.serials = Serials(name="serials", path=path_root)
        try:
            self.serials.set_all()
        except Exception, e:
            _logger.error(str(e))

    @Route(methods="get", resource="/system/serial")
    def get(self, message, response):
        return response(data=self.serials.getAll())

    @Route(methods="get", resource="/system/serial/:id")
    def get_by_id(self, message, response):
        serial = self.serials.get(int(message.param["id"])
        if serial is None:
            return response(code=404)
        return response(data=serial)

    @Route(methods="put", resource="/system/serial/:id")
    def put(self, message, response):
        updatedTemplate = self.serials.update(
            id=int(message.param["id"]), newObj=message.data)
        if updatedTemplate is None:
            return response(code=404)
        return response(data=updatedTemplate)


if __name__ == "__main__":
    from sanji.connection.mqtt import Mqtt
    FORMAT = "%(asctime)s - %(levelname)s - %(lineno)s - %(message)s"
    logging.basicConfig(level=0, format=FORMAT)
    _logger = logging.getLogger("sanji.serial")
    logging.getLogger("sh").setLevel(logging.WARN)
    index = Index(connection=Mqtt())
    index.start()
