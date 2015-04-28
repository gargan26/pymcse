# pymcse, Python Minecraft Schematic Editor
# Copyright (C) 2015  Gargan26
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

import os
import logging
import nbt
import numpy

log = logging.getLogger(__name__)


def load_schematic(filename):
    if not filename:
        log.error('Filename not given.')
    elif not os.path.exists(filename):
        log.error('File not found: {0}'.format(filename))

    log.info('Opening {0}'.format(filename))

    try:
        root_tag = nbt.read_nbt(filename)
        if root_tag.name.lower() == 'schematic':
            return MCSchematic(root_tag=root_tag)
        else:
            raise IOError('NBT data does not conform to Schematic standards.')
    except:
        raise IOError('Unable to load schematic data.')


class MCSchematic(object):
    def __init__(self, root_tag=None):
        if root_tag is not None:
            self.root_tag = root_tag
            self.width = root_tag['Width']
            self.height = root_tag['Height']
            self.length = root_tag['Length']
            self.materials = root_tag['Materials']

    # Helper function to check for a valid range and raise an overflow error if invalid.
    def check_range(self, value, lower_bound, upper_bound, var='Data'):
        if lower_bound <= value <= upper_bound:
            return value
        else:
            raise OverflowError('{0} must be in the range of {1} <= x <= {2}'.format(var, lower_bound, upper_bound))

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, width):
        # NBT requires a signed short for Width, but negative or zero widths don't make sense.
        self._width = self.check_range(width, 1, 32767, 'Width')

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, height):
        # Same thing as width, height <= 0 is invalid
        self._height = self.check_range(height, 1, 32767, 'Height')

    @property
    def length(self):
        return self._length

    @length.setter
    def length(self, length):
        # Same thing as width, length <= 0 is invalid
        self._length = self.check_range(length, 1, 32767, 'Length')

    @property
    def materials(self):
        return self._materials

    # For now, materials will just be a string...
    @materials.setter
    def materials(self, materials):
        if isinstance(materials, str):
            self._materials = materials
        else:
            raise ValueError('Materials must be a string. (For now)')