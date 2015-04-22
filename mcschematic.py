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

    @property
    def width(self):
        return self.root_tag.data