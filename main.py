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

import sys
import mcschematic
import tkinter
import tkinter.filedialog

import nbt


def main():
    tkinter.Tk().withdraw()
    open_file_dialog_options = {'filetypes': [('Minecraft Schematic Files', '.schematic'), ('All Files', '.*')]}
    filename = tkinter.filedialog.askopenfilename(**open_file_dialog_options)

    schematic_data = mcschematic.load_schematic(filename)

    return 0


if __name__ == '__main__':
    sys.exit(main())