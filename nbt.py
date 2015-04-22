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

import logging
import gzip
import struct
import array
# import collections.abc
# import numpy

log = logging.getLogger(__name__)

# NBT Tag types
TAG_END = 0
TAG_BYTE = 1
TAG_SHORT = 2
TAG_INT = 3
TAG_LONG = 4
TAG_FLOAT = 5
TAG_DOUBLE = 6
TAG_BYTE_ARRAY = 7
TAG_STRING = 8
TAG_LIST = 9
TAG_COMPOUND = 10
TAG_INT_ARRAY = 11

# NBT Payload Structures
nbt_signed_byte = struct.Struct('>b')
nbt_signed_short = struct.Struct('>h')
nbt_unsigned_short = struct.Struct('>H')
nbt_signed_int = struct.Struct('>i')
nbt_signed_long = struct.Struct('>q')
nbt_float = struct.Struct('>f')
nbt_double = struct.Struct('>d')


class DataInput(object):
    '''This class is a simple port of the Java DataInput class type.'''

    def __init__(self, data=b''):
        self.data = bytearray(data)

    def read_raw_byte(self):
        if len(self.data) >= 1:
            retval = self.data[0:1]
            del self.data[0]
            return bytes(retval)
        else:
            raise EOFError

    def read_byte(self):
        return nbt_signed_byte.unpack(self.read_raw_byte())[0]

    def read_raw_short(self):
        if len(self.data) >= 2:
            retval = self.data[0:2]
            del self.data[0:2]
            return bytes(retval)
        else:
            raise EOFError

    def read_unsigned_short(self):
        return nbt_unsigned_short.unpack(self.read_raw_short())[0]

    def read_raw_int(self):
        if len(self.data) >= 4:
            retval = self.data[0:4]
            del self.data[0:4]
            return bytes(retval)
        else:
            raise EOFError

    def read_int(self):
        return nbt_signed_int.unpack(self.read_raw_int())[0]

    def read_raw_long(self):
        if len(self.data) >= 8:
            retval = self.data[0:8]
            del self.data[0:8]
            return bytes(retval)
        else:
            raise EOFError

    def read_raw_float(self):
        return self.read_raw_int()

    def read_raw_double(self):
        return self.read_raw_long()

    def read_utf(self):
        utf_length = self.read_unsigned_short()

        if len(self.data) >= utf_length:
            utf_data = self.data[0:utf_length]
            del self.data[0:utf_length]
            return utf_data.decode('utf-8')
        else:
            raise EOFError

    def read_fully(self, length):
        if len(self.data) >= length:
            retval = self.data[0:length]
            del self.data[0:length]
            return bytes(retval)
        else:
            raise EOFError


class NBTTagBase(object):
    __slots__ = ['name', '_data']

    datastruct = None

    def __init__(self, data=None):
        self.name = ''
        self.data = data

    @property
    def data(self):
        if self.datastruct is None:
            return self._data
        else:
            if self._data is not None:
                return self.datastruct.unpack(self._data)[0]
            else:
                return None

    @data.setter
    def data(self, value):
        if value is not None and self.datastruct is not None:
            value = self.datastruct.pack(value)

        self._data = value


class NBTTagEnd(NBTTagBase):
    __slots__ = ()

    def read(self):
        pass


class NBTTagByte(NBTTagBase):
    __slots__ = ()

    datastruct = nbt_signed_byte

    def read(self, data_input):
        self._data = data_input.read_raw_byte()


class NBTTagShort(NBTTagBase):
    __slots__ = ()

    datastruct = nbt_signed_short

    def read(self, data_input):
        self._data = data_input.read_raw_short()


class NBTTagInt(NBTTagBase):
    __slots__ = ()

    datastruct = nbt_signed_int

    def read(self, data_input):
        self._data = data_input.read_raw_int()


class NBTTagLong(NBTTagBase):
    __slots__ = ()

    datastruct = nbt_signed_long

    def read(self, data_input):
        self._data = data_input.read_raw_long()


class NBTTagFloat(NBTTagBase):
    __slots__ = ()

    datastruct = nbt_float

    def read(self, data_input):
        self._data = data_input.read_raw_float()


class NBTTagDouble(NBTTagBase):
    __slots__ = ()

    datastruct = nbt_double

    def read(self, data_input):
        self._data = data_input.read_raw_double()


class NBTTagByteArray(NBTTagBase):
    __slots__ = ()

    def __init__(self):
        # super().__init__(data=SignedByteArray())
        super().__init__(data=array.array('b'))

    def read(self, data_input):
        num_bytes = data_input.read_int()
        self.data = array.array('b', data_input.read_fully(num_bytes))


class NBTTagString(NBTTagBase):
    __slots__ = ()

    def read(self, data_input):
        self.data = data_input.read_utf()


class NBTTagList(NBTTagBase):
    __slots__ = 'tag_type'

    def __init__(self):
        self.tag_type = None
        super().__init__(data=[])

    def read(self, data_input):
        self.data.clear()
        self.tag_type = data_input.read_byte()

        for i in range(data_input.read_int()):
            nbt_tag = nbt_tag_classes[self.tag_type]()
            nbt_tag.read(data_input)
            self.data.append(nbt_tag.data)


class NBTTagCompound(NBTTagBase):
    __slots__ = ()

    def __init__(self):
        super().__init__(data=[])

    def read(self, data_input):
        self.data.clear()

        while True:
            nbt_tag = read_nbt_tag(data_input)

            if isinstance(nbt_tag, NBTTagEnd):
                break

            self.data.append(nbt_tag)


class NBTTagIntArray():
    __slots__ = ()

    def __init__(self):
        super().__init__(data=array.array('i'))

    def read(self, data_input):
        length = data_input.read_int()
        self.data = array.array('i')*length

        for i in range(0, length):
            self.data[i] = data_input.read_int()


nbt_tag_classes = [NBTTagEnd, NBTTagByte, NBTTagShort, NBTTagInt, NBTTagLong, NBTTagFloat, NBTTagDouble,
                   NBTTagByteArray, NBTTagString, NBTTagList, NBTTagCompound, NBTTagIntArray]


def read_nbt_tag(data_input):
    nbt_tag_type = data_input.read_byte()

    nbt_tag = nbt_tag_classes[nbt_tag_type]()
    if nbt_tag_type != TAG_END:
        nbt_tag.name = data_input.read_utf()
        nbt_tag.read(data_input)

    return nbt_tag


def read_nbt(filename):
    '''
    Read NBT data from a GZip compressed data stream and return the root TAG_Compound.

    Argument: data, type: bytes
    Return type: NBTTagCompound
    '''

    with open(filename, 'rb') as f:
        data = f.read()

    # Try to decompress gzip data
    try:
        data_input = DataInput(gzip.decompress(data))
    except:
        log.warning('Unable to decompress data stream. Assuming file is uncompressed.')
        data_input = DataInput(data)

    nbt_tag_type = data_input.read_byte()

    if nbt_tag_type != TAG_COMPOUND:
        log.error('Root tag must be a named compound tag.')
        return None

    nbt_tag = NBTTagCompound()
    nbt_tag.name = data_input.read_utf()
    nbt_tag.read(data_input)

    return nbt_tag
