#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import sys
import glob
import unittest

from mock import Mock
from mock import patch

try:
    sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
    from mxserial import Serials
except ImportError as e:
    print "Please check the python PATH for import test module. (%s)" \
        % __file__
    exit(1)


class TestInterfacesClass(unittest.TestCase):

    def setUp(self):
        self.root_path = os.path.abspath(os.path.dirname(__file__) + "/../../")
        jsons = glob.glob(os.path.join(self.root_path, "data/*.json"))
        backups = glob.glob(os.path.join(self.root_path, "data/*.backup"))
        for file in jsons + backups:
            os.unlink(file)
        self.serials = Serials(name="serials", path=self.root_path)

    def tearDown(self):
        pass

    def test_get_serial(self):
        """Add a LogProfile, with a vaild config, \
           should return LogProfile instance"""
        for serial in self.serials.getAll():
            self.assertIn("dev", serial)
            self.assertIn("devDisplayName", serial)
            self.assertIn("mode", serial)
            self.assertIn("id", serial)

    @patch("mxserial.sh")
    def test_set_serial(self, sh):
        m = Mock()
        sh.setinterface = m
        self.serials.update(1, {"mode": "rs422/rs485-4w"})
        m.assert_called_once_with("/dev/ttyM0", 2)

if __name__ == "__main__":
    unittest.main()
