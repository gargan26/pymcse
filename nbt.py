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

unsigned_short = struct.Struct('>H')
signed_short = struct.Struct('>h')
signed_int = struct.Struct('>i')


class DataInput(object):
    '''
    This class is a simple port of the Java DataInput class type.
    '''

    def __init__(self, data=b''):
        if not isinstance(data, bytes):
            raise TypeError
        self.data = data
        self.index = 0

    def read_byte(self):
        if self.index < len(self.data):
            return_byte = self.data[self.index]
            if return_byte > 127:
                return_byte -= 256
            self.index += 1
            return return_byte
        else:
            raise EOFError

    def read_short(self):
        if self.index + 1 < len(self.data):
            retval, = signed_short.unpack_from(self.data, self.index)
            self.index += 2
            return retval
        else:
            raise EOFError

    def read_unsigned_short(self):
        if self.index + 1 < len(self.data):
            retval, = unsigned_short.unpack_from(self.data, self.index)
            self.index += 2
            return retval
        else:
            raise EOFError

    def read_int(self):
        if self.index + 3 < len(self.data):
            retval, = signed_int.unpack_from(self.data, self.index)
            self.index += 4
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


class NBTBase(object):
    # public static final String[] NBT_TYPES = new String[] {"END", "BYTE", "SHORT", "INT", "LONG", "FLOAT", "DOUBLE", "BYTE[]", "STRING", "LIST", "COMPOUND", "INT[]"};

    # /**
    #  * Write the actual data contents of the tag, implemented in NBT extension classes
    #  */
    # abstract void write(DataOutput output) throws IOException;

    # abstract void read(DataInput input, int depth, NBTSizeTracker sizeTracker) throws IOException;

    # public abstract String toString();

    # /**
    #  * Gets the type byte for the tag.
    #  */
    # public abstract byte getId();

    # /**
    #  * Creates a new NBTBase object that corresponds with the passed in id.
    #  */
    @staticmethod
    def create_new_by_type(tag):
        if tag == TAG_END:
            return NBTTagEnd()
        elif tag == TAG_BYTE:
            return NBTTagByte()
        elif tag == TAG_SHORT:
            return NBTTagShort()
        elif tag == TAG_INT:
            return NBTTagInt()
        elif tag == TAG_LONG:
            return NBTTagLong()
        elif tag == TAG_FLOAT:
            return NBTTagFloat()
        elif tag == TAG_DOUBLE:
            return NBTTagDouble()
        elif tag == TAG_BYTE_ARRAY:
            return NBTTagByteArray()
        elif tag == TAG_STRING:
            return NBTTagString()
        elif tag == TAG_LIST:
            return NBTTagList()
        elif tag == TAG_COMPOUND:
            return NBTTagCompound()
        elif tag == TAG_INT_ARRAY:
            return NBTTagIntArray()
        else:
            return None

    # /**
    #  * Creates a clone of the tag.
    #  */
    # public abstract NBTBase copy();

    # /**
    #  * Return whether this compound has no tags.
    #  */
    # public boolean hasNoTags()
    # {
    #     return false;
    # }

    # public boolean equals(Object p_equals_1_)
    # {
    #     if (!(p_equals_1_ instanceof NBTBase))
    #     {
    #         return false;
    #     }
    #     else
    #     {
    #         NBTBase var2 = (NBTBase)p_equals_1_;
    #         return this.getId() == var2.getId();
    #     }
    # }

    # public int hashCode()
    # {
    #     return this.getId();
    # }

    # protected String getString()
    # {
    #     return this.toString();
    # }

    # public abstract static class NBTPrimitive extends NBTBase
    # {
    #     public abstract long getLong();
    #
    #     public abstract int getInt();
    #
    #     public abstract short getShort();
    #
    #     public abstract byte getByte();
    #
    #     public abstract double getDouble();
    #
    #     public abstract float getFloat();
    # }


class NBTTagEnd(NBTBase):
    # void read(DataInput input, int depth, NBTSizeTracker sizeTracker) throws IOException {}

    # /**
    #  * Write the actual data contents of the tag, implemented in NBT extension classes
    #  */
    # void write(DataOutput output) throws IOException {}

    # /**
    #  * Gets the type byte for the tag.
    #  */
    # public byte getId()
    # {
    #     return (byte)0;
    # }

    # public String toString()
    # {
    #     return "END";
    # }

    # /**
    #  * Creates a clone of the tag.
    #  */
    # public NBTBase copy()
    # {
    #     return new NBTTagEnd();
    # }
    pass


class NBTTagByte():
    pass


class NBTTagShort(NBTBase):
    #public class NBTTagShort extends NBTBase.NBTPrimitive

    def __init__(self, data=None):
        if data:
            self.data = data

    # /**
    #  * Write the actual data contents of the tag, implemented in NBT extension classes
    #  */
    # void write(DataOutput output) throws IOException
    # {
    #     output.writeShort(this.data);
    # }

    def read(self, data_input, depth):
        self.data = data_input.read_short()

    # /**
    #  * Gets the type byte for the tag.
    #  */
    # public byte getId()
    # {
    #     return (byte)2;
    # }
    #
    # public String toString()
    # {
    #     return "" + this.data + "s";
    # }
    #
    # /**
    #  * Creates a clone of the tag.
    #  */
    # public NBTBase copy()
    # {
    #     return new NBTTagShort(this.data);
    # }
    #
    # public boolean equals(Object p_equals_1_)
    # {
    #     if (super.equals(p_equals_1_))
    #     {
    #         NBTTagShort var2 = (NBTTagShort)p_equals_1_;
    #         return this.data == var2.data;
    #     }
    #     else
    #     {
    #         return false;
    #     }
    # }
    #
    # public int hashCode()
    # {
    #     return super.hashCode() ^ this.data;
    # }
    #
    # public long getLong()
    # {
    #     return (long)this.data;
    # }
    #
    # public int getInt()
    # {
    #     return this.data;
    # }
    #
    # public short getShort()
    # {
    #     return this.data;
    # }
    #
    # public byte getByte()
    # {
    #     return (byte)(this.data & 255);
    # }
    #
    # public double getDouble()
    # {
    #     return (double)this.data;
    # }
    #
    # public float getFloat()
    # {
    #     return (float)this.data;
    # }
    pass


class NBTTagInt():
    pass


class NBTTagLong():
    pass


class NBTTagFloat():
    pass


class NBTTagDouble():
    pass


class NBTTagByteArray():
    pass


class NBTTagString():
    pass


class NBTTagList(NBTBase):
    def __init__(self):
        self.tag_type = TAG_END
        self.tag_list = []

#     private static final Logger LOGGER = LogManager.getLogger();
#
#     /**
#      * Write the actual data contents of the tag, implemented in NBT extension classes
#      */
#     void write(DataOutput output) throws IOException
#     {
#         if (!this.tagList.isEmpty())
#         {
#             this.tagType = ((NBTBase)this.tagList.get(0)).getId();
#         }
#         else
#         {
#             this.tagType = 0;
#         }
#
#         output.writeByte(this.tagType);
#         output.writeInt(this.tagList.size());
#
#         for (int var2 = 0; var2 < this.tagList.size(); ++var2)
#         {
#             ((NBTBase)this.tagList.get(var2)).write(output);
#         }
#     }

    def read(self, data_input, depth):
        if depth > 512:
            raise RuntimeError('Tried to read NBT tag with too high complexity, depth > 512')
        else:
            self.tag_type = data_input.read_byte()
            self.tag_list.clear()

            for i in range(data_input.read_int()):
                nbt_tag = NBTBase.create_new_by_type(self.tag_type)
                nbt_tag.read(data_input, depth+1)
                self.tag_list.append(nbt_tag)

#
#     /**
#      * Gets the type byte for the tag.
#      */
#     public byte getId()
#     {
#         return (byte)9;
#     }
#
#     public String toString()
#     {
#         String var1 = "[";
#         int var2 = 0;
#
#         for (Iterator var3 = this.tagList.iterator(); var3.hasNext(); ++var2)
#         {
#             NBTBase var4 = (NBTBase)var3.next();
#             var1 = var1 + "" + var2 + ':' + var4 + ',';
#         }
#
#         return var1 + "]";
#     }
#
#     /**
#      * Adds the provided tag to the end of the list. There is no check to verify this tag is of the same type as any
#      * previous tag.
#      */
#     public void appendTag(NBTBase nbt)
#     {
#         if (this.tagType == 0)
#         {
#             this.tagType = nbt.getId();
#         }
#         else if (this.tagType != nbt.getId())
#         {
#             LOGGER.warn("Adding mismatching tag types to tag list");
#             return;
#         }
#
#         this.tagList.add(nbt);
#     }
#
#     /**
#      * Set the given index to the given tag
#      */
#     public void set(int idx, NBTBase nbt)
#     {
#         if (idx >= 0 && idx < this.tagList.size())
#         {
#             if (this.tagType == 0)
#             {
#                 this.tagType = nbt.getId();
#             }
#             else if (this.tagType != nbt.getId())
#             {
#                 LOGGER.warn("Adding mismatching tag types to tag list");
#                 return;
#             }
#
#             this.tagList.set(idx, nbt);
#         }
#         else
#         {
#             LOGGER.warn("index out of bounds to set tag in tag list");
#         }
#     }
#
#     /**
#      * Removes a tag at the given index.
#      */
#     public NBTBase removeTag(int i)
#     {
#         return (NBTBase)this.tagList.remove(i);
#     }
#
#     /**
#      * Return whether this compound has no tags.
#      */
#     public boolean hasNoTags()
#     {
#         return this.tagList.isEmpty();
#     }
#
#     /**
#      * Retrieves the NBTTagCompound at the specified index in the list
#      */
#     public NBTTagCompound getCompoundTagAt(int i)
#     {
#         if (i >= 0 && i < this.tagList.size())
#         {
#             NBTBase var2 = (NBTBase)this.tagList.get(i);
#             return var2.getId() == 10 ? (NBTTagCompound)var2 : new NBTTagCompound();
#         }
#         else
#         {
#             return new NBTTagCompound();
#         }
#     }
#
#     public int[] getIntArray(int i)
#     {
#         if (i >= 0 && i < this.tagList.size())
#         {
#             NBTBase var2 = (NBTBase)this.tagList.get(i);
#             return var2.getId() == 11 ? ((NBTTagIntArray)var2).getIntArray() : new int[0];
#         }
#         else
#         {
#             return new int[0];
#         }
#     }
#
#     public double getDouble(int i)
#     {
#         if (i >= 0 && i < this.tagList.size())
#         {
#             NBTBase var2 = (NBTBase)this.tagList.get(i);
#             return var2.getId() == 6 ? ((NBTTagDouble)var2).getDouble() : 0.0D;
#         }
#         else
#         {
#             return 0.0D;
#         }
#     }
#
#     public float getFloat(int i)
#     {
#         if (i >= 0 && i < this.tagList.size())
#         {
#             NBTBase var2 = (NBTBase)this.tagList.get(i);
#             return var2.getId() == 5 ? ((NBTTagFloat)var2).getFloat() : 0.0F;
#         }
#         else
#         {
#             return 0.0F;
#         }
#     }
#
#     /**
#      * Retrieves the tag String value at the specified index in the list
#      */
#     public String getStringTagAt(int i)
#     {
#         if (i >= 0 && i < this.tagList.size())
#         {
#             NBTBase var2 = (NBTBase)this.tagList.get(i);
#             return var2.getId() == 8 ? var2.getString() : var2.toString();
#         }
#         else
#         {
#             return "";
#         }
#     }
#
#     /**
#      * Get the tag at the given position
#      */
#     public NBTBase get(int idx)
#     {
#         return (NBTBase)(idx >= 0 && idx < this.tagList.size() ? (NBTBase)this.tagList.get(idx) : new NBTTagEnd());
#     }
#
#     /**
#      * Returns the number of tags in the list.
#      */
#     public int tagCount()
#     {
#         return this.tagList.size();
#     }
#
#     /**
#      * Creates a clone of the tag.
#      */
#     public NBTBase copy()
#     {
#         NBTTagList var1 = new NBTTagList();
#         var1.tagType = this.tagType;
#         Iterator var2 = this.tagList.iterator();
#
#         while (var2.hasNext())
#         {
#             NBTBase var3 = (NBTBase)var2.next();
#             NBTBase var4 = var3.copy();
#             var1.tagList.add(var4);
#         }
#
#         return var1;
#     }
#
#     public boolean equals(Object p_equals_1_)
#     {
#         if (super.equals(p_equals_1_))
#         {
#             NBTTagList var2 = (NBTTagList)p_equals_1_;
#
#             if (this.tagType == var2.tagType)
#             {
#                 return this.tagList.equals(var2.tagList);
#             }
#         }
#
#         return false;
#     }
#
#     public int hashCode()
#     {
#         return super.hashCode() ^ this.tagList.hashCode();
#     }
#
#     public int getTagType()
#     {
#         return this.tagType;
#     }


class NBTTagCompound(NBTBase):
    def __init__(self):
        self.tagMap = {}
    # private static final Logger logger = LogManager.getLogger();
    #
    # /**
    #  * The key-value pairs for the tag. Each key is a UTF string, each value is a tag.
    #  */
    # private Map tagMap = Maps.newHashMap();
    #
    # /**
    #  * Write the actual data contents of the tag, implemented in NBT extension classes
    #  */
    # void write(DataOutput output) throws IOException
    # {
    #     Iterator var2 = this.tagMap.keySet().iterator();
    #
    #     while (var2.hasNext())
    #     {
    #         String var3 = (String)var2.next();
    #         NBTBase var4 = (NBTBase)this.tagMap.get(var3);
    #         writeEntry(var3, var4, output);
    #     }
    #
    #     output.writeByte(0);
    # }

    def read(self, data_input, depth):
        # void read(DataInput input, int depth, NBTSizeTracker sizeTracker) throws IOException
        # {
        if depth > 512:
            raise RuntimeError('Tried to read NBT tag with too high complexity, depth > 512')
        else:
            self.tagMap.clear()

            while True:
                nbt_tag_type = self.read_type(data_input)

                if nbt_tag_type == TAG_END:
                    break

                nbt_tag_name = self.read_key(data_input)
                nbt_tag_payload = self.read_nbt(nbt_tag_type, nbt_tag_name, data_input, depth+1)
                self.tagMap[nbt_tag_name] = nbt_tag_payload

    # /**
    #  * Gets a set with the names of the keys in the tag compound.
    #  */
    # public Set getKeySet()
    # {
    #     return this.tagMap.keySet();
    # }
    #
    # /**
    #  * Gets the type byte for the tag.
    #  */
    # public byte getId()
    # {
    #     return (byte)10;
    # }
    #
    # /**
    #  * Stores the given tag into the map with the given string key. This is mostly used to store tag lists.
    #  */
    # public void setTag(String key, NBTBase value)
    # {
    #     this.tagMap.put(key, value);
    # }
    #
    # /**
    #  * Stores a new NBTTagByte with the given byte value into the map with the given string key.
    #  */
    # public void setByte(String key, byte value)
    # {
    #     this.tagMap.put(key, new NBTTagByte(value));
    # }
    #
    # /**
    #  * Stores a new NBTTagShort with the given short value into the map with the given string key.
    #  */
    # public void setShort(String key, short value)
    # {
    #     this.tagMap.put(key, new NBTTagShort(value));
    # }
    #
    # /**
    #  * Stores a new NBTTagInt with the given integer value into the map with the given string key.
    #  */
    # public void setInteger(String key, int value)
    # {
    #     this.tagMap.put(key, new NBTTagInt(value));
    # }
    #
    # /**
    #  * Stores a new NBTTagLong with the given long value into the map with the given string key.
    #  */
    # public void setLong(String key, long value)
    # {
    #     this.tagMap.put(key, new NBTTagLong(value));
    # }
    #
    # /**
    #  * Stores a new NBTTagFloat with the given float value into the map with the given string key.
    #  */
    # public void setFloat(String key, float value)
    # {
    #     this.tagMap.put(key, new NBTTagFloat(value));
    # }
    #
    # /**
    #  * Stores a new NBTTagDouble with the given double value into the map with the given string key.
    #  */
    # public void setDouble(String key, double value)
    # {
    #     this.tagMap.put(key, new NBTTagDouble(value));
    # }
    #
    # /**
    #  * Stores a new NBTTagString with the given string value into the map with the given string key.
    #  */
    # public void setString(String key, String value)
    # {
    #     this.tagMap.put(key, new NBTTagString(value));
    # }
    #
    # /**
    #  * Stores a new NBTTagByteArray with the given array as data into the map with the given string key.
    #  */
    # public void setByteArray(String key, byte[] value)
    # {
    #     this.tagMap.put(key, new NBTTagByteArray(value));
    # }
    #
    # /**
    #  * Stores a new NBTTagIntArray with the given array as data into the map with the given string key.
    #  */
    # public void setIntArray(String key, int[] value)
    # {
    #     this.tagMap.put(key, new NBTTagIntArray(value));
    # }
    #
    # /**
    #  * Stores the given boolean value as a NBTTagByte, storing 1 for true and 0 for false, using the given string key.
    #  */
    # public void setBoolean(String key, boolean value)
    # {
    #     this.setByte(key, (byte)(value ? 1 : 0));
    # }
    #
    # /**
    #  * gets a generic tag with the specified name
    #  */
    # public NBTBase getTag(String key)
    # {
    #     return (NBTBase)this.tagMap.get(key);
    # }
    #
    # /**
    #  * Get the Type-ID for the entry with the given key
    #  */
    # public byte getTagType(String key)
    # {
    #     NBTBase var2 = (NBTBase)this.tagMap.get(key);
    #     return var2 != null ? var2.getId() : 0;
    # }
    #
    # /**
    #  * Returns whether the given string has been previously stored as a key in the map.
    #  */
    # public boolean hasKey(String key)
    # {
    #     return this.tagMap.containsKey(key);
    # }
    #
    # public boolean hasKey(String key, int type)
    # {
    #     byte var3 = this.getTagType(key);
    #
    #     if (var3 == type)
    #     {
    #         return true;
    #     }
    #     else if (type != 99)
    #     {
    #         if (var3 > 0)
    #         {
    #             ;
    #         }
    #
    #         return false;
    #     }
    #     else
    #     {
    #         return var3 == 1 || var3 == 2 || var3 == 3 || var3 == 4 || var3 == 5 || var3 == 6;
    #     }
    # }
    #
    # /**
    #  * Retrieves a byte value using the specified key, or 0 if no such key was stored.
    #  */
    # public byte getByte(String key)
    # {
    #     try
    #     {
    #         return !this.hasKey(key, 99) ? 0 : ((NBTBase.NBTPrimitive)this.tagMap.get(key)).getByte();
    #     }
    #     catch (ClassCastException var3)
    #     {
    #         return (byte)0;
    #     }
    # }
    #
    # /**
    #  * Retrieves a short value using the specified key, or 0 if no such key was stored.
    #  */
    # public short getShort(String key)
    # {
    #     try
    #     {
    #         return !this.hasKey(key, 99) ? 0 : ((NBTBase.NBTPrimitive)this.tagMap.get(key)).getShort();
    #     }
    #     catch (ClassCastException var3)
    #     {
    #         return (short)0;
    #     }
    # }
    #
    # /**
    #  * Retrieves an integer value using the specified key, or 0 if no such key was stored.
    #  */
    # public int getInteger(String key)
    # {
    #     try
    #     {
    #         return !this.hasKey(key, 99) ? 0 : ((NBTBase.NBTPrimitive)this.tagMap.get(key)).getInt();
    #     }
    #     catch (ClassCastException var3)
    #     {
    #         return 0;
    #     }
    # }
    #
    # /**
    #  * Retrieves a long value using the specified key, or 0 if no such key was stored.
    #  */
    # public long getLong(String key)
    # {
    #     try
    #     {
    #         return !this.hasKey(key, 99) ? 0L : ((NBTBase.NBTPrimitive)this.tagMap.get(key)).getLong();
    #     }
    #     catch (ClassCastException var3)
    #     {
    #         return 0L;
    #     }
    # }
    #
    # /**
    #  * Retrieves a float value using the specified key, or 0 if no such key was stored.
    #  */
    # public float getFloat(String key)
    # {
    #     try
    #     {
    #         return !this.hasKey(key, 99) ? 0.0F : ((NBTBase.NBTPrimitive)this.tagMap.get(key)).getFloat();
    #     }
    #     catch (ClassCastException var3)
    #     {
    #         return 0.0F;
    #     }
    # }
    #
    # /**
    #  * Retrieves a double value using the specified key, or 0 if no such key was stored.
    #  */
    # public double getDouble(String key)
    # {
    #     try
    #     {
    #         return !this.hasKey(key, 99) ? 0.0D : ((NBTBase.NBTPrimitive)this.tagMap.get(key)).getDouble();
    #     }
    #     catch (ClassCastException var3)
    #     {
    #         return 0.0D;
    #     }
    # }
    #
    # /**
    #  * Retrieves a string value using the specified key, or an empty string if no such key was stored.
    #  */
    # public String getString(String key)
    # {
    #     try
    #     {
    #         return !this.hasKey(key, 8) ? "" : ((NBTBase)this.tagMap.get(key)).getString();
    #     }
    #     catch (ClassCastException var3)
    #     {
    #         return "";
    #     }
    # }
    #
    # /**
    #  * Retrieves a byte array using the specified key, or a zero-length array if no such key was stored.
    #  */
    # public byte[] getByteArray(String key)
    # {
    #     try
    #     {
    #         return !this.hasKey(key, 7) ? new byte[0] : ((NBTTagByteArray)this.tagMap.get(key)).getByteArray();
    #     }
    #     catch (ClassCastException var3)
    #     {
    #         throw new ReportedException(this.createCrashReport(key, 7, var3));
    #     }
    # }
    #
    # /**
    #  * Retrieves an int array using the specified key, or a zero-length array if no such key was stored.
    #  */
    # public int[] getIntArray(String key)
    # {
    #     try
    #     {
    #         return !this.hasKey(key, 11) ? new int[0] : ((NBTTagIntArray)this.tagMap.get(key)).getIntArray();
    #     }
    #     catch (ClassCastException var3)
    #     {
    #         throw new ReportedException(this.createCrashReport(key, 11, var3));
    #     }
    # }
    #
    # /**
    #  * Retrieves a NBTTagCompound subtag matching the specified key, or a new empty NBTTagCompound if no such key was
    #  * stored.
    #  */
    # public NBTTagCompound getCompoundTag(String key)
    # {
    #     try
    #     {
    #         return !this.hasKey(key, 10) ? new NBTTagCompound() : (NBTTagCompound)this.tagMap.get(key);
    #     }
    #     catch (ClassCastException var3)
    #     {
    #         throw new ReportedException(this.createCrashReport(key, 10, var3));
    #     }
    # }
    #
    # /**
    #  * Gets the NBTTagList object with the given name. Args: name, NBTBase type
    #  */
    # public NBTTagList getTagList(String key, int type)
    # {
    #     try
    #     {
    #         if (this.getTagType(key) != 9)
    #         {
    #             return new NBTTagList();
    #         }
    #         else
    #         {
    #             NBTTagList var3 = (NBTTagList)this.tagMap.get(key);
    #             return var3.tagCount() > 0 && var3.getTagType() != type ? new NBTTagList() : var3;
    #         }
    #     }
    #     catch (ClassCastException var4)
    #     {
    #         throw new ReportedException(this.createCrashReport(key, 9, var4));
    #     }
    # }
    #
    # /**
    #  * Retrieves a boolean value using the specified key, or false if no such key was stored. This uses the getByte
    #  * method.
    #  */
    # public boolean getBoolean(String key)
    # {
    #     return this.getByte(key) != 0;
    # }
    #
    # /**
    #  * Remove the specified tag.
    #  */
    # public void removeTag(String key)
    # {
    #     this.tagMap.remove(key);
    # }
    #
    # public String toString()
    # {
    #     String var1 = "{";
    #     String var3;
    #
    #     for (Iterator var2 = this.tagMap.keySet().iterator(); var2.hasNext(); var1 = var1 + var3 + ':' + this.tagMap.get(var3) + ',')
    #     {
    #         var3 = (String)var2.next();
    #     }
    #
    #     return var1 + "}";
    # }
    #
    # /**
    #  * Return whether this compound has no tags.
    #  */
    # public boolean hasNoTags()
    # {
    #     return this.tagMap.isEmpty();
    # }
    #
    # /**
    #  * Create a crash report which indicates a NBT read error.
    #  */
    # private CrashReport createCrashReport(final String key, final int expectedType, ClassCastException ex)
    # {
    #     CrashReport var4 = CrashReport.makeCrashReport(ex, "Reading NBT data");
    #     CrashReportCategory var5 = var4.makeCategoryDepth("Corrupt NBT tag", 1);
    #     var5.addCrashSectionCallable("Tag type found", new Callable()
    #     {
    #         private static final String __OBFID = "CL_00001216";
    #         public String call()
    #         {
    #             return NBTBase.NBT_TYPES[((NBTBase)NBTTagCompound.this.tagMap.get(key)).getId()];
    #         }
    #     });
    #     var5.addCrashSectionCallable("Tag type expected", new Callable()
    #     {
    #         private static final String __OBFID = "CL_00001217";
    #         public String call()
    #         {
    #             return NBTBase.NBT_TYPES[expectedType];
    #         }
    #     });
    #     var5.addCrashSection("Tag name", key);
    #     return var4;
    # }
    #
    # /**
    #  * Creates a clone of the tag.
    #  */
    # public NBTBase copy()
    # {
    #     NBTTagCompound var1 = new NBTTagCompound();
    #     Iterator var2 = this.tagMap.keySet().iterator();
    #
    #     while (var2.hasNext())
    #     {
    #         String var3 = (String)var2.next();
    #         var1.setTag(var3, ((NBTBase)this.tagMap.get(var3)).copy());
    #     }
    #
    #     return var1;
    # }
    #
    # public boolean equals(Object p_equals_1_)
    # {
    #     if (super.equals(p_equals_1_))
    #     {
    #         NBTTagCompound var2 = (NBTTagCompound)p_equals_1_;
    #         return this.tagMap.entrySet().equals(var2.tagMap.entrySet());
    #     }
    #     else
    #     {
    #         return false;
    #     }
    # }
    #
    # public int hashCode()
    # {
    #     return super.hashCode() ^ this.tagMap.hashCode();
    # }
    #
    # private static void writeEntry(String name, NBTBase data, DataOutput output) throws IOException
    # {
    #     output.writeByte(data.getId());
    #
    #     if (data.getId() != 0)
    #     {
    #         output.writeUTF(name);
    #         data.write(output);
    #     }
    # }
    #

    def read_type(self, data_input):
        return data_input.read_byte()

    def read_key(self, data_input):
        return data_input.read_utf()

    def read_nbt(self, nbt_tag_type, nbt_tag_name, data_input, depth):
        nbt_tag = NBTBase.create_new_by_type(nbt_tag_type)

        try:
            nbt_tag.read(data_input, depth)
            return nbt_tag
        except Exception:
            log.error('Error loading NBT data')
            raise
        # catch (IOException var9)
        # {
        #     CrashReport var7 = CrashReport.makeCrashReport(var9, "Loading NBT data");
        #     CrashReportCategory var8 = var7.makeCategory("NBT Tag");
        #     var8.addCrashSection("Tag name", key);
        #     var8.addCrashSection("Tag type", Byte.valueOf(id));
        #     throw new ReportedException(var7);
        # }

    # /**
    #  * Merges this NBTTagCompound with the given compound. Any sub-compounds are merged using the same methods, other
    #  * types of tags are overwritten from the given compound.
    #  */
    # public void merge(NBTTagCompound other)
    # {
    #     Iterator var2 = other.tagMap.keySet().iterator();
    #
    #     while (var2.hasNext())
    #     {
    #         String var3 = (String)var2.next();
    #         NBTBase var4 = (NBTBase)other.tagMap.get(var3);
    #
    #         if (var4.getId() == 10)
    #         {
    #             if (this.hasKey(var3, 10))
    #             {
    #                 NBTTagCompound var5 = this.getCompoundTag(var3);
    #                 var5.merge((NBTTagCompound)var4);
    #             }
    #             else
    #             {
    #                 this.setTag(var3, var4.copy());
    #             }
    #         }
    #         else
    #         {
    #             this.setTag(var3, var4.copy());
    #         }
    #     }
    # }


class NBTTagIntArray():
    pass


def read_compressed(data):
    '''
    Read NBT data from a GZip compressed data stream and return the root TAG_Compound.

    Argument: data, type: bytes
    Return type: NBTTagCompound
    '''

    # Try to decompress gzip data
    try:
        data_input = DataInput(gzip.decompress(data))
    except Exception as e:
        log.error('Unable to decompress data stream. ({0}: {1})'.format(e.__class__.__name__, e))
        return None

    nbt_tag_type = data_input.read_byte()

    if nbt_tag_type == TAG_END:
        return NBTTagEnd()
    else:
        data_input.read_utf()
        nbt_data = NBTBase.create_new_by_type(nbt_tag_type)

        try:
            #nbt_data.read(data_input, 0, NBTSizeTracker.INFINITE)
            nbt_data.read(data_input, 0)
            return nbt_data
        except Exception:
            log.error('Error loading NBT data.')
            raise
    #         catch (IOException var8)
    #         {
    #             CrashReport var6 = CrashReport.makeCrashReport(var8, "Loading NBT data");
    #             CrashReportCategory var7 = var6.makeCategory("NBT Tag");
    #             var7.addCrashSection("Tag name", "[UNNAMED TAG]");
    #             var7.addCrashSection("Tag type", Byte.valueOf(var3));
    #             throw new ReportedException(var6);
    #         }


#     if isinstance(data, str):
#         data = data.encode('utf-8')
#
#     if not len(data):
#         raise RuntimeError('NBT data is empty.')
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
