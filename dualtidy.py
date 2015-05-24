#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

"""Lightweight GTK tray battery monitor that supports more than one battery."""

from ctypes import cdll, byref, create_string_buffer
from gi.repository import Gtk, GObject
import subprocess
import re
import signal

ACPI_CMD = 'acpi'
ICON_TIMEOUT = 5000
NOTIFY_TIMEOUT = 120000


class Battery:

    """Main battery class."""

    def __init__(self, num=0):
        self.num = num
        self.icon = Gtk.StatusIcon()
        self.update_icon()
        GObject.timeout_add(ICON_TIMEOUT, self.update_icon)
        GObject.timeout_add(NOTIFY_TIMEOUT, self.notify)

    def get_battery_info(self):
        """Get battery state and percentage using acpi."""
        missing = {
            'state': "Missing",
            'percentage': 0,
            'tooltip': "Battery not found",
        }
        text = subprocess.check_output(ACPI_CMD).decode().split('\n')
        try:
            text = text[self.num]
        except IndexError:
            return missing
        if not text:
            return missing
        if not re.match("[^:]+:[^,]+,.+", text):
            return {
                'state': "Unknown",
                'percentage': 0,
                'tooltip': "Not Parsable: %s" % text,
            }
        data = text.split(',')
        return {
            'state': data[0].split(':')[1].strip(' '),
            'percentage': int(data[1].strip(' %')),
            'tooltip': text.split(':', 1)[1][1:],
        }

    @staticmethod
    def get_icon_name(state, percentage):
        """Get icon name according to battery state and percentage."""
        if state == 'Discharging':
            if percentage < 10:
                icon = 'battery-000'
            elif percentage < 20:
                icon = 'battery-020'
            elif percentage < 40:
                icon = 'battery-040'
            elif percentage < 60:
                icon = 'battery-060'
            elif percentage < 80:
                icon = 'battery-080'
            else:
                icon = 'battery-100'

        elif state == 'Charging':
            if percentage < 10:
                icon = 'battery-000-charging'
            elif percentage < 20:
                icon = 'battery-020-charging'
            elif percentage < 40:
                icon = 'battery-040-charging'
            elif percentage < 60:
                icon = 'battery-060-charging'
            elif percentage < 80:
                icon = 'battery-080-charging'
            else:
                icon = 'battery-100-charging'

        elif state == 'Charged' or (state == 'Unknown' and percentage == 100):
            icon = 'battery-charged'

        elif state == 'Full':
            icon = 'battery-100'

        else:
            icon = 'battery-missing'

        return icon

    def update_icon(self):
        """Update tray icon if needed."""
        info = self.get_battery_info()
        icon_name = self.get_icon_name(info['state'], info['percentage'])
        self.icon.set_from_icon_name(icon_name)
        self.icon.set_tooltip_text(info['tooltip'])
        return True

    def notify(self):
        """Send a notification on empty or full battery."""
        info = self.get_battery_info()
        state = info['state']
        percentage = info['percentage']
        tooltip = info['tooltip']
        if state in ['Charging', 'Unknown'] and percentage >= 80:
            cmd = ['notify-send', '-i', 'battery-full-charged-symbolic',
                   'Battery Full', 'Unplug']
            subprocess.call(cmd)
        elif state == 'Discharging' and percentage <= 20:
            cmd = ['notify-send', '-i', 'battery-caution-symbolic',
                   'Low Battery', tooltip]
            subprocess.call(cmd)
        return True


def main():
    """Initialize one instance of Battery class per battery."""
    name = create_string_buffer(b'dualtidy')
    libc = cdll.LoadLibrary('libc.so.6')
    libc.prctl(15, byref(name), 0, 0, 0)
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    num_batteries = len(subprocess.check_output(ACPI_CMD).decode().split('\n')) - 1
    Battery(0)
    for i in range(1, num_batteries):
        Battery(num=i)

    Gtk.main()


if __name__ == '__main__':
    main()
