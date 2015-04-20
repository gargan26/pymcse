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
nbt_unsigned_short = struct.Struct('>H')
nbt_signed_short = struct.Struct('>h')
nbt_signed_int = struct.Struct('>i')
nbt_signed_long = struct.Struct('>q')
nbt_float = struct.Struct('>f')
nbt_double = struct.Struct('>d')


class DataInput(object):
    '''This class is a simple port of the Java DataInput class type.'''

    def __init__(self, data=b''):
        if not isinstance(data, bytes):
            raise TypeError
        self.data = data
        self.index = 0

    def read_byte(self):
        if self.index < len(self.data):
            retval, = nbt_signed_byte.unpack_from(self.data, self.index)
            self.index += 1
            return retval
        else:
            raise EOFError

    def read_short(self):
        if self.index + 2 <= len(self.data):
            retval, = nbt_signed_short.unpack_from(self.data, self.index)
            self.index += 2
            return retval
        else:
            raise EOFError

    def read_unsigned_short(self):
        if self.index + 2 <= len(self.data):
            retval, = nbt_unsigned_short.unpack_from(self.data, self.index)
            self.index += 2
            return retval
        else:
            raise EOFError

    def read_int(self):
        if self.index + 4 <= len(self.data):
            retval, = nbt_signed_int.unpack_from(self.data, self.index)
            self.index += 4
            return retval
        else:
            raise EOFError

    def read_long(self):
        if self.index + 8 <= len(self.data):
            retval, = nbt_signed_long.unpack_from(self.data, self.index)
            self.index += 8
            return retval
        else:
            raise EOFError

    def read_float(self):
        if self.index + 4 <= len(self.data):
            retval, = nbt_float.unpack_from(self.data, self.index)
            self.index += 4
            return retval
        else:
            raise EOFError

    def read_double(self):
        if self.index + 8 <= len(self.data):
            retval, = nbt_double.unpack_from(self.data, self.index)
            self.index += 8
            return retval
        else:
            raise EOFError

    def read_utf(self):
        utf_length = self.read_unsigned_short()
        utf_data = self.data[self.index:self.index+utf_length]
        self.index += len(utf_data)

        if len(utf_data) < utf_length:
            raise EOFError

        return utf_data.decode('utf-8')

    def read_fully(self, length):
        if self.index + length <= len(self.data):
            retval = struct.unpack_from('>{0}b'.format(length), self.data, self.index)
            self.index += length
            return SignedByteList(retval)
        else:
            raise EOFError


class NBTTagBase(object):
    __slots__ = ['name', 'data']

    def __init__(self, data=None):
        self.name = ''
        self.data = data


class NBTTagEnd():
    pass


class NBTTagByte(NBTTagBase):
    __slots__ = []

    def read(self, data_input):
        self.data = data_input.read_byte()


class NBTTagShort(NBTTagBase):
    __slots__ = []

    def read(self, data_input):
        self.data = data_input.read_short()


class NBTTagInt(NBTTagBase):
    __slots__ = []

    def read(self, data_input):
        self.data = data_input.read_int()


class NBTTagLong(NBTTagBase):
    __slots__ = []

    def read(self, data_input):
        self.data = data_input.read_long()


class NBTTagFloat(NBTTagBase):
    __slots__ = []

    def read(self, data_input):
        self.data = data_input.read_float()


class NBTTagDouble(NBTTagBase):
    __slots__ = []

    def read(self, data_input):
        self.data = data_input.read_double()


class SignedByteList(list):
    def __setitem__(self, key, value):
        # Make sure the range is -128 to 127
        value %= 256

        if value > 127:
            value -= 256

        super().__setitem__(key, value)

    def append(self, p_object):
        # Make sure the range is -128 to 127
        p_object %= 256

        if p_object > 127:
            p_object -= 256

        super().append(p_object)


class NBTTagByteArray(NBTTagBase):
    __slots__ = []

    def __init__(self):
        super().__init__(data=SignedByteList())

    def read(self, data_input):
        num_bytes = data_input.read_int()
        self.data = data_input.read_fully(num_bytes)


class NBTTagString(NBTTagBase):
    __slots__ = []

    def read(self, data_input):
        self.data = data_input.read_utf()


class NBTTagList(NBTTagBase):
    __slots__ = 'tag_type'

    def __init__(self):
        super().__init__(data=[])
        self.tag_type = None

    def read(self, data_input):
        self.tag_type = data_input.read_byte()

        for i in range(data_input.read_int()):
            nbt_tag = nbt_tag_classes[self.tag_type]()
            nbt_tag.read(data_input)
            self.data.append(nbt_tag.data)


class NBTTagCompound(NBTTagBase):
    __slots__ = []

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
    pass


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



# TAG_END = 0
# TAG_BYTE = 1
# TAG_SHORT = 2
# TAG_INT = 3
# TAG_LONG = 4
# TAG_FLOAT = 5
# TAG_DOUBLE = 6
# TAG_BYTE_ARRAY = 7
# TAG_STRING = 8
# TAG_LIST = 9
# TAG_COMPOUND = 10
# TAG_INT_ARRAY = 11
# # TAG_SHORT_ARRAY = 12
#
# string_len_format = struct.Struct('>H')
#
#
# class TAG_Value(object):
#     '''Simple values. Subclasses override fmt to change the type and size. Subclasses may set data_type instead of
#     overriding setValue for automatic data type coercion'''
#     __slots__ = ('_name', '_value')
#
#     def __init__(self, value=0, name=''):
#         self.value = value
#         self.name = name
#
#     fmt = struct.Struct('=c')
#     tagID = NotImplemented
#     data_type = NotImplemented
#
#     @property
#     def value(self):
#         return self._value
#
#     @value.setter
#     def value(self, new_value):
#         '''Change the TAG's value. Data types are checked and coerced if needed.'''
#         self._value = self.data_type(new_value)
#
#     @property
#     def name(self):
#         return self._name
#
#     @name.setter
#     def name(self, new_name):
#         '''Change the TAG's name. Coerced to a unicode.'''
#         self._name = str(new_name)
#
#     @classmethod
#     def load_from(cls, ctx):
#         data = ctx.data[ctx.offset:]
#         value, = cls.fmt.unpack_from(data)
#         self = cls(value=value)
#         ctx.offset += self.fmt.size
#         return self
#
#     # def __repr__(self):
#     #     return '<%s name="%s" value=%r>' % (str(self.__class__.__name__), self.name, self.value)
#
#     # def write_tag(self, buf):
#     #     buf.write(chr(self.tagID))
#
#     # def write_name(self, buf):
#     #     if self.name is not None:
#     #         write_string(self.name, buf)
#
#     # def write_value(self, buf):
#     #     buf.write(self.fmt.pack(self.value))
#
#
# class TAG_Byte(TAG_Value):
#     __slots__ = ()
#     tagID = TAG_BYTE
#     fmt = struct.Struct('>b')
#     data_type = int
#
#
# class TAG_Short(TAG_Value):
#     __slots__ = ()
#     tagID = TAG_SHORT
#     fmt = struct.Struct('>h')
#     data_type = int
#
#
# class TAG_Int(TAG_Value):
#     __slots__ = ()
#     tagID = TAG_INT
#     fmt = struct.Struct('>i')
#     data_type = int
#
#
# class TAG_Long(TAG_Value):
#     __slots__ = ()
#     tagID = TAG_LONG
#     fmt = struct.Struct('>q')
#     data_type = int
#
#
# class TAG_Float(TAG_Value):
#     __slots__ = ()
#     tagID = TAG_FLOAT
#     fmt = struct.Struct('>f')
#     data_type = float
#
#
# class TAG_Double(TAG_Value):
#     __slots__ = ()
#     tagID = TAG_DOUBLE
#     fmt = struct.Struct('>d')
#     data_type = float
#
#
# class TAG_Byte_Array(TAG_Value):
#     '''Like a string, but for binary data. Four length bytes instead of two. Value is a bytearray, and you can change
#     its elements'''
#     __slots__ = ()
#
#     tagID = TAG_BYTE_ARRAY
#     data_type = bytearray
#
#     def __init__(self, value=None, name=''):
#         if value is None:
#             value = bytearray()
#         self.name = name
#         self.value = value
#
#     def __repr__(self):
#         return '<{0} name="{1}" length={2}>'.format(self.__class__, self.name, len(self.value))
#
#     @classmethod
#     def load_from(cls, ctx):
#         data = ctx.data[ctx.offset:]
#         string_len, = TAG_Int.fmt.unpack_from(data)
#         value = struct.Struct('>{0}b'.format(string_len)).unpack_from(data[4:])
#         self = cls(value)
#         ctx.offset += string_len + 4
#         return self
#
#     # def write_value(self, buf):
#     #     value_str = self.value.tostring()
#     #     buf.write(struct.pack('>I%ds' % (len(value_str),), self.value.size, value_str))
#
#
# class TAG_String(TAG_Value):
#     '''String in UTF-8
#     The value parameter must be a 'unicode' or a UTF-8 encoded 'str'
#     '''
#     __slots__ = ()
#
#     tagID = TAG_STRING
#     data_type = str
#
#     def __init__(self, value='', name=''):
#         if name:
#             self.name = name
#         self.value = value
#
#     # _decodeCache = {}
#
#     # def data_type(self, value):
#     #     if isinstance(value, str):
#     #         return value
#     #     else:
#     #         decoded = self._decodeCache.get(value)
#     #         if decoded is None:
#     #             decoded = value.decode('utf-8')
#     #             self._decodeCache[value] = decoded
#     #
#     #         return decoded
#
#     @classmethod
#     def load_from(cls, ctx):
#         value = load_string(ctx)
#         return cls(value)
#
#     # def write_value(self, buf):
#     #     write_string(self._value, buf)
#
#
# class TAG_List(TAG_Value, collections.MutableSequence):
#     '''
#     A homogenous list of unnamed data of a single TAG_* type.
#
#     Once created, the type can only be changed by emptying the list and adding an element of the new type. If created
#     with no arguments, returns a list of TAG_Compound.
#
#     Empty lists in the wild have been seen with type TAG_Byte
#     '''
#     __slots__ = 'list_type'
#
#     tagID = TAG_LIST
#
#     def __init__(self, value=None, name='', list_type=TAG_BYTE):
#         # can be created from a list of tags in value, with an optional
#         # name, or created from raw tag data, or created with list_type
#         # taken from a TAG class or instance
#
#         self.name = name
#         self.list_type = list_type
#         self.value = value or []
#
#     def __repr__(self):
#         return '<{0} name="{1}" list_type={2!r} length={3}>'.format(self.__class__.__name__, self.name,
#                                                                     tag_classes[self.list_type], len(self))
#
#     def data_type(self, value):
#         if value:
#             self.list_type = value[0].tagID
#         assert all([x.tagID == self.list_type for x in value])
#         return list(value)
#
#     @classmethod
#     def load_from(cls, ctx):
#         self = cls()
#         self.list_type = ctx.data[ctx.offset]
#         ctx.offset += 1
#
#         (list_length,) = TAG_Int.fmt.unpack_from(ctx.data, ctx.offset)
#         ctx.offset += TAG_Int.fmt.size
#
#         for i in range(list_length):
#             tag = tag_classes[self.list_type].load_from(ctx)
#             self.append(tag)
#
#         return self
#
#     # def write_value(self, buf):
#     #    buf.write(chr(self.list_type))
#     #    buf.write(TAG_Int.fmt.pack(len(self.value)))
#     #    for i in self.value:
#     #        i.write_value(buf)
#
#     def check_tag(self, value):
#         if value.tagID != self.list_type:
#             raise TypeError('Invalid type {0} for TAG_List({1})'.format(value.__class__, tag_classes[self.list_type]))
#
#     # --- collection methods ---
#
#     def __delitem__(self, index):
#         del self.value[index]
#
#     def __getitem__(self, index):
#         return self.value[index]
#
#     def __len__(self):
#         return len(self.value)
#
#     def __setitem__(self, index, value):
#         if isinstance(index, slice):
#             for tag in value:
#                 self.check_tag(tag)
#         else:
#             self.check_tag(value)
#
#         self.value[index] = value
#
#     def insert(self, index, value):
#         if len(self) == 0:
#             self.list_type = value.tagID
#         else:
#             self.check_tag(value)
#
#         value.name = ''
#         self.value.insert(index, value)
#
#     # def __iter__(self):
#     #     return iter(self.value)
#
#     # def __contains__(self, tag):
#     #     return tag in self.value
#
#
# class TAG_Compound(TAG_Value, collections.MutableMapping):
#     '''A heterogeneous list of named tags. Names must be unique within the TAG_Compound. Add tags to the compound using
#     the subscript operator []. This will automatically name the tags.'''
#     __slots__ = ()
#
#     tagID = TAG_COMPOUND
#
#     # ALLOW_DUPLICATE_KEYS = False
#
#     def __init__(self, value=None, name=''):
#         self.value = value or []
#         self.name = name
#
#     def __repr__(self):
#         return '<{0} name="{1}" keys={2!r}>'.format(self.__class__.__name__, self.name, list(self.keys()))
#
#     def data_type(self, val):
#         for i in val:
#             self.check_value(i)
#         return list(val)
#
#     def check_value(self, val):
#         if not isinstance(val, TAG_Value):
#             raise TypeError('Invalid type for TAG_Compound element: {0}'.format(val.__class__.__name__))
#         if not val.name:
#             raise ValueError('Tag needs a name to be inserted into TAG_Compound: {0}'.format(val))
#
#     @classmethod
#     def load_from(cls, ctx):
#         self = cls()
#         while ctx.offset < len(ctx.data):
#             tag_type = ctx.data[ctx.offset]
#             ctx.offset += 1
#
#             if tag_type == TAG_END:
#                 break
#
#             tag_name = load_string(ctx)
#             tag = tag_classes[tag_type].load_from(ctx)
#             tag.name = tag_name
#
#             self._value.append(tag)
#
#         return self
#
#     # def save(self, filename_or_buf=None, compressed=True):
#     #     '''
#     #     Save the TAG_Compound element to a file. Since this element is the root tag, it can be named.
#     #     Pass a filename to save the data to a file. Pass a file-like object (with a read() method)
#     #     to write the data to that object. Pass nothing to return the data as a string.
#     #     '''
#     #     if self.name is None:
#     #         self.name = ''
#     #
#     #     buf = StringIO()
#     #     self.write_tag(buf)
#     #     self.write_name(buf)
#     #     self.write_value(buf)
#     #     data = buf.getvalue()
#     #
#     #     if compressed:
#     #         gzio = BytesIO()
#     #         gz = gzip.GzipFile(fileobj=gzio, mode='wb')
#     #         gz.write(data)
#     #         gz.close()
#     #         data = gzio.getvalue()
#     #
#     #     if filename_or_buf is None:
#     #         return data
#     #
#     #     if isinstance(filename_or_buf, str):
#     #         f = open(filename_or_buf, 'wb')
#     #         f.write(data)
#     #     else:
#     #         filename_or_buf.write(data)
#
#     # def write_value(self, buf):
#     #     for tag in self.value:
#     #         tag.write_tag(buf)
#     #         tag.write_name(buf)
#     #         tag.write_value(buf)
#     #
#     #     buf.write('\x00')
#
#     # --- collection functions ---
#
#     def __delitem__(self, key):
#         self.value.__delitem__(self.value.index(self[key]))
#
#     def __getitem__(self, key):
#         for tag in self.value:
#             if tag.name == key:
#                 return tag
#         raise KeyError('Key {0} not found'.format(key))
#
#     def __iter__(self):
#         return map(lambda x: x.name, self.value)
#
#     def __len__(self):
#         return self.value.__len__()
#
#     def __setitem__(self, key, item):
#         '''Automatically wraps lists and tuples in a TAG_List, and wraps strings in a TAG_String.'''
#         if isinstance(item, (list, tuple)):
#             item = TAG_List(item)
#         elif isinstance(item, str):
#             item = TAG_String(item)
#
#         item.name = key
#         self.check_value(item)
#
#         # remove any items already named 'key'.
#         # if not self.ALLOW_DUPLICATE_KEYS:
#         self._value = [x for x in self._value if x.name != key]
#
#         self._value.append(item)
#
#     # def __contains__(self, key):
#     #     return key in [x.name for x in self.value]
#
#     # def add(self, value):
#     #     if value.name is None:
#     #         raise ValueError('Tag %r must have a name.' % value)
#     #
#     #     self[value.name] = value
#
#     # def get_all(self, key):
#     #     return [v for v in self._value if v.name == key]
#
#
# class TAG_Int_Array(TAG_Byte_Array):
#     tagID = TAG_INT_ARRAY
#
# tag_classes = {cls.tagID: cls for cls in (TAG_Byte, TAG_Short, TAG_Int, TAG_Long, TAG_Float, TAG_Double, TAG_Byte_Array, TAG_String, TAG_List, TAG_Compound, TAG_Int_Array)}
#
#
# class NBTData(object):
#     def __init__(self, data=None, offset=0):
#         self.data = data
#         self.offset = offset
#
#
# def load_string(ctx):
#     data = ctx.data[ctx.offset:]
#     string_len, = string_len_format.unpack_from(data)
#
#     value = data[2:string_len+2].decode('utf-8')
#     ctx.offset += string_len + 2
#     return value
#
#
# def load(data):
#     '''Unserialize NBT data from data and return the root TAG_Compound object.'''
#
#     if isinstance(data, str):
#         data = data.encode('utf-8')
#
#     if not len(data):
#         raise RuntimeError('NBT data is empty.')
#
#     # Let's try to gunzip the data, if this fails assume the data is already uncompressed
#     try:
#         data = gzip.decompress(data)
#     except OSError:
#         pass
#
#     tag_type = data[0]
#     if tag_type != TAG_COMPOUND:
#         magic = data[:4]
#         raise RuntimeError('NBT root TAG_Compound missing or invalid. (NBT data starts with "{0}" (0x{1:X}))'.format(magic.decode('utf-8'), int.from_bytes(magic, 'little')))
#
#     nbt_data = NBTData(data, offset=1)
#
#     tag_name = load_string(nbt_data)
#     tag = TAG_Compound.load_from(nbt_data)
#     tag.name = tag_name
#
#     return tag
