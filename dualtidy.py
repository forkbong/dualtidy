#!/usr/bin/env python2
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
import gtk
import gobject
import subprocess
import re
import signal

ACPI_CMD = 'acpi'
TIMEOUT = 5000

class Battery:

    """Main battery class."""

    def __init__(self, num=0):
        self.num = num
        self.icon = gtk.StatusIcon()
        self.update_icon()
        gobject.timeout_add(TIMEOUT, self.update_icon)

    def get_battery_info(self):
        """Get battery state and percentage using acpi."""
        try:
            text = subprocess.check_output(ACPI_CMD).split('\n')[self.num]
        except IndexError:
            return {'state':"Unknown", 'percentage':0, 'tooltip':"Battery not found"}
        if not re.match("[^:]+:[^,]+,.+", text):
            return {'state':"Unknown", 'percentage':0, 'tooltip':"Not Parsable: %s" % text}
        data = text.split(',')
        return {
            'state': data[0].split(':')[1].strip(' '),
            'percentage': int(data[1].strip(' %')),
            'tooltip': text.split(':',1)[1][1:]
        }

    def get_icon_name(self, state, percentage):
        if state == 'Discharging' or state == 'Unknown':
            if percentage < 10:
                return 'battery-empty-symbolic'
            elif percentage < 20:
                return 'battery-caution-symbolic'
            elif percentage < 40:
                return 'battery-low-symbolic'
            elif percentage < 60:
                return 'battery-good-symbolic'
            else:
                return 'battery-full-symbolic'

        elif state == 'Charging':
            if percentage >= 80:
                return 'battery-full-charging-symbolic'
            elif percentage >= 60:
                return 'battery-good-charging-symbolic'
            elif percentage >= 40:
                return 'battery-low-charging-symbolic'
            elif percentage >= 20:
                return 'battery-caution-charging-symbolic'
            else:
                return 'battery-empty-charging-symbolic'

        elif state == 'Charged':
            return 'battery-full-charged-symbolic'

        elif state == 'Full':
            return 'battery-full-symbolic'

        else:
            return 'battery-missing-symbolic'

    def update_icon(self):
        """Update tray icon if needed."""
        info = self.get_battery_info()
        icon_name = self.get_icon_name(info['state'], info['percentage'])
        self.icon.set_from_icon_name(icon_name)
        self.icon.set_tooltip_text(info['tooltip'])
        return True

def main():
    """Initialize one instance of Battery class per battery."""
    name = create_string_buffer(b'dualtidy')
    libc = cdll.LoadLibrary('libc.so.6')
    libc.prctl(15, byref(name), 0, 0, 0)
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    num_batteries = len(subprocess.check_output(ACPI_CMD).split('\n')) - 1
    for i in xrange(num_batteries):
        Battery(num=i)

    gtk.main()


if __name__ == '__main__':
    main()
