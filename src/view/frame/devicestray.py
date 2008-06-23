# Copyright (C) 2008 One Laptop Per Child
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import logging

from sugar.graphics.tray import HTray

from view.devices import deviceview
from model import shellmodel

_logger = logging.getLogger('DevicesTray')

class DevicesTray(HTray):
    def __init__(self):
        HTray.__init__(self)
        self._device_icons = {}

        devices_model = shellmodel.get_instance().get_devices()

        for device in devices_model:
            self._add_device(device)

        devices_model.connect('device-appeared',
                              self.__device_appeared_cb)
        devices_model.connect('device-disappeared',
                              self.__device_disappeared_cb)

    def _add_device(self, device):
        try:
            view = deviceview.create(device)
            # TODO: *Tray classes don't allow yet to set the alignment.
            self.add_item(view)
            view.show()
            self._device_icons[device.get_id()] = view
        except Exception, message:
            _logger.warn("Not able to add icon for device [%r], because of "
                         "an error (%s). Continuing." % (device, message))

    def _remove_device(self, device):
        self.remove_item(self._device_icons[device.get_id()])
        del self._device_icons[device.get_id()]

    def __device_appeared_cb(self, model, device):
        self._add_device(device)

    def __device_disappeared_cb(self, model, device):
        self._remove_device(device)
