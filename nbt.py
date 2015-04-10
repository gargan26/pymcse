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
import collections
import struct
import numpy

log = logging.getLogger(__name__)

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
# TAG_SHORT_ARRAY = 12

string_len_format = struct.Struct('>H')


class TAG_Value(object):
    '''Simple values. Subclasses override fmt to change the type and size. Subclasses may set data_type instead of
    overriding setValue for automatic data type coercion'''
    __slots__ = ('_name', '_value')

    def __init__(self, value=0, name=''):
        self.value = value
        self.name = name

    fmt = struct.Struct('=c')
    tagID = NotImplemented
    data_type = NotImplemented

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        '''Change the TAG's value. Data types are checked and coerced if needed.'''
        self._value = self.data_type(new_value)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        '''Change the TAG's name. Coerced to a unicode.'''
        self._name = str(new_name)

    @classmethod
    def load_from(cls, ctx):
        data = ctx.data[ctx.offset:]
        value, = cls.fmt.unpack_from(data)
        self = cls(value=value)
        ctx.offset += self.fmt.size
        return self

    # def __repr__(self):
    #     return '<%s name="%s" value=%r>' % (str(self.__class__.__name__), self.name, self.value)

    # def write_tag(self, buf):
    #     buf.write(chr(self.tagID))

    # def write_name(self, buf):
    #     if self.name is not None:
    #         write_string(self.name, buf)

    # def write_value(self, buf):
    #     buf.write(self.fmt.pack(self.value))


class TAG_Byte(TAG_Value):
    __slots__ = ()
    tagID = TAG_BYTE
    fmt = struct.Struct('>b')
    data_type = int


class TAG_Short(TAG_Value):
    __slots__ = ()
    tagID = TAG_SHORT
    fmt = struct.Struct('>h')
    data_type = int


class TAG_Int(TAG_Value):
    __slots__ = ()
    tagID = TAG_INT
    fmt = struct.Struct('>i')
    data_type = int


class TAG_Long(TAG_Value):
    __slots__ = ()
    tagID = TAG_LONG
    fmt = struct.Struct('>q')
    data_type = int


class TAG_Float(TAG_Value):
    __slots__ = ()
    tagID = TAG_FLOAT
    fmt = struct.Struct('>f')
    data_type = float


class TAG_Double(TAG_Value):
    __slots__ = ()
    tagID = TAG_DOUBLE
    fmt = struct.Struct('>d')
    data_type = float


class TAG_Byte_Array(TAG_Value):
    '''Like a string, but for binary data. Four length bytes instead of two. Value is a numpy array, and you can change
    its elements'''
    __slots__ = ()

    tagID = TAG_BYTE_ARRAY

    def __init__(self, value=None, name=''):
        if value is None:
            value = numpy.zeros(0, self.dtype)
        self.name = name
        self.value = value

    def __repr__(self):
        return '<{0} name="{1}" length={2}>'.format(self.__class__, self.name, len(self.value))

    def data_type(self, value):
        return numpy.array(value, self.dtype)

    dtype = numpy.dtype('uint8')

    @classmethod
    def load_from(cls, ctx):
        data = ctx.data[ctx.offset:]
        string_len, = TAG_Int.fmt.unpack_from(data)
        value = fromstring(data[4:string_len * cls.dtype.itemsize + 4], cls.dtype)
        self = cls(value)
        ctx.offset += string_len * cls.dtype.itemsize + 4
        return self

    # def write_value(self, buf):
    #     value_str = self.value.tostring()
    #     buf.write(struct.pack('>I%ds' % (len(value_str),), self.value.size, value_str))


class TAG_String(TAG_Value):
    tagID = TAG_STRING


class TAG_List(TAG_Value, collections.MutableSequence):
    tagID = TAG_LIST


class TAG_Compound(TAG_Value, collections.MutableMapping):
    '''A heterogeneous list of named tags. Names must be unique within the TAG_Compound. Add tags to the compound using
    the subscript operator []. This will automatically name the tags.'''
    __slots__ = ()

    tagID = TAG_COMPOUND

    # ALLOW_DUPLICATE_KEYS = False

    def __init__(self, value=None, name=''):
        self.value = value or []
        self.name = name

    def __repr__(self):
        return '<{0} name="{1}" keys={2!r}>'.format(self.__class__.__name__, self.name, list(self.keys()))

    def data_type(self, val):
        for i in val:
            self.check_value(i)
        return list(val)

    def check_value(self, val):
        if not isinstance(val, TAG_Value):
            raise TypeError('Invalid type for TAG_Compound element: {0}'.format(val.__class__.__name__))
        if not val.name:
            raise ValueError('Tag needs a name to be inserted into TAG_Compound: {0}'.format(val))

    @classmethod
    def load_from(cls, ctx):
        self = cls()
        while ctx.offset < len(ctx.data):
            tag_type = ctx.data[ctx.offset]
            ctx.offset += 1

            if tag_type == TAG_END:
                break

            tag_name = load_string(ctx)
            tag = tag_classes[tag_type].load_from(ctx)
            tag.name = tag_name

            self._value.append(tag)

        return self

    # def save(self, filename_or_buf=None, compressed=True):
    #     '''
    #     Save the TAG_Compound element to a file. Since this element is the root tag, it can be named.
    #     Pass a filename to save the data to a file. Pass a file-like object (with a read() method)
    #     to write the data to that object. Pass nothing to return the data as a string.
    #     '''
    #     if self.name is None:
    #         self.name = ''
    #
    #     buf = StringIO()
    #     self.write_tag(buf)
    #     self.write_name(buf)
    #     self.write_value(buf)
    #     data = buf.getvalue()
    #
    #     if compressed:
    #         gzio = BytesIO()
    #         gz = gzip.GzipFile(fileobj=gzio, mode='wb')
    #         gz.write(data)
    #         gz.close()
    #         data = gzio.getvalue()
    #
    #     if filename_or_buf is None:
    #         return data
    #
    #     if isinstance(filename_or_buf, str):
    #         f = open(filename_or_buf, 'wb')
    #         f.write(data)
    #     else:
    #         filename_or_buf.write(data)

    # def write_value(self, buf):
    #     for tag in self.value:
    #         tag.write_tag(buf)
    #         tag.write_name(buf)
    #         tag.write_value(buf)
    #
    #     buf.write('\x00')

    # --- collection functions ---

    def __delitem__(self, key):
        self.value.__delitem__(self.value.index(self[key]))

    def __getitem__(self, key):
        for tag in self.value:
            if tag.name == key:
                return tag
        raise KeyError('Key {0} not found'.format(key))

    def __iter__(self):
        return map(lambda x: x.name, self.value)

    def __len__(self):
        return self.value.__len__()

    def __setitem__(self, key, item):
        '''Automatically wraps lists and tuples in a TAG_List, and wraps strings in a TAG_String.'''
        if isinstance(item, (list, tuple)):
            item = TAG_List(item)
        elif isinstance(item, str):
            item = TAG_String(item)

        item.name = key
        self.check_value(item)

        # remove any items already named 'key'.
        # if not self.ALLOW_DUPLICATE_KEYS:
        self._value = [x for x in self._value if x.name != key]

        self._value.append(item)

    # def __contains__(self, key):
    #     return key in [x.name for x in self.value]

    # def add(self, value):
    #     if value.name is None:
    #         raise ValueError('Tag %r must have a name.' % value)
    #
    #     self[value.name] = value

    # def get_all(self, key):
    #     return [v for v in self._value if v.name == key]


class TAG_Int_Array(TAG_Byte_Array):
    tagID = TAG_INT_ARRAY

tag_classes = {cls.tagID: cls for cls in (TAG_Byte, TAG_Short, TAG_Int, TAG_Long, TAG_Float, TAG_Double, TAG_Byte_Array, TAG_String, TAG_List, TAG_Compound, TAG_Int_Array)}


class NBTData(object):
    def __init__(self, data=None, offset=0):
        self.data = data
        self.offset = offset


def load_string(ctx):
    data = ctx.data[ctx.offset:]
    string_len, = string_len_format.unpack_from(data)

    value = data[2:string_len+2].decode('utf-8')
    ctx.offset += string_len + 2
    return value


def load(data):
    '''Unserialize NBT data from data and return the root TAG_Compound object.'''

    if isinstance(data, str):
        data = data.encode('utf-8')

    if not len(data):
        raise RuntimeError('NBT data is empty.')

    # Let's try to gunzip the data, if this fails assume the data is already uncompressed
    try:
        data = gzip.decompress(data)
    except OSError:
        pass

    tag_type = data[0]
    if tag_type != TAG_COMPOUND:
        magic = data[:4]
        raise RuntimeError('NBT root TAG_Compound missing or invalid. (NBT data starts with "{0}" (0x{1:X}))'.format(magic.decode('utf-8'), int.from_bytes(magic, 'little')))

    nbt_data = NBTData(data, offset=1)

    tag_name = load_string(nbt_data)
    tag = TAG_Compound.load_from(nbt_data)
    tag.name = tag_name

    return tag
