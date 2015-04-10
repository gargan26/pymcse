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
    log.info('Opening ' + filename)

    if not filename or not os.path.exists(filename):
        raise IOError('File not found: ' + filename)

    with open(filename, 'rb') as f:
        rawbytes = f.read()

    if len(rawbytes) < 4:
        raise ValueError('{0} is too small! ({1})'.format(filename, len(rawbytes)))

    # data = gzip.decompress(rawbytes)

    root_tag = nbt.read_compressed(rawbytes)
    ## return MCSchematic(root_tag=root_tag, filename=filename)

    raise IOError('Unable to load schematic data.')