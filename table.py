# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT
"""
`table`
================================================================================

CircuitPython Library to create tables


* Author(s): Jose D. Montoya


"""

import displayio
from bitmaptools import draw_line
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import bitmap_label


__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/jposada202020/CircuitPython_TABLE.git"


class Table(displayio.Group):
    """
    Create a table with the given parameters.

    :param int originx: The x origin of the table.
    :param int originy: The y origin of the table.
    :param int width: The width of the table.
    :param int height: The height of the table.
    :param list table: The table to be displayed.
    :param str font_file: The font file to be used.
    :param int color: Line color. Defaults to 0xFFFFFF
    :param int text_color: Text color. Defaults to 0x123456

    """

    def __init__(
        self,
        originx: int,
        originy: int,
        width: int = 200,
        height: int = 200,
        structure: list = None,
        table: list = None,
        font_file=None,
        border_color: int = 0xFFFFFF,
        text_color: int = 0x123456,
    ) -> None:
        super().__init__(x=originx, y=originy, scale=1)
        self._padding = 3
        self._plotbitmap = displayio.Bitmap(
            width + 2 * self._padding, height + 2 * self._padding, 10
        )
        self._table = table
        self._text_color = text_color

        self._colum_size = [0]
        self._row_size = [0]

        self._font_to_use = bitmap_font.load_font(font_file)
        widtht, heightt, _, self._dy = self._font_to_use.get_bounding_box()

        self._origin_x = 0
        self._origin_y = 0

        self._get_structure(structure)

        self._width = widtht
        self._height = heightt

        plot_palette = displayio.Palette(10)
        plot_palette.make_transparent(0)
        plot_palette[1] = 0xFFFFFF
        plot_palette[2] = border_color
        plot_palette[3] = 0x00FF00
        plot_palette[4] = 0x0000FF
        plot_palette[5] = 0xFFFF00
        plot_palette[6] = 0x00FFFF
        plot_palette[7] = 0x123456
        plot_palette[8] = 0x654321
        plot_palette[9] = 0x000000

        self.append(
            displayio.TileGrid(self._plotbitmap, pixel_shader=plot_palette, x=0, y=0)
        )

        self.create_label_objects()
        self.create_borders()

    def _get_structure(self, structure) -> None:
        """
        Get the structure of the table

        """

        texth = bitmap_label.Label(self._font_to_use, text="-")
        textv = bitmap_label.Label(self._font_to_use, text="Y")

        distanceh = 0
        distancev = 0

        for row in structure:
            if len(structure[0]) == 1:
                self._colum_size.append(
                    self._origin_x + distanceh + len(row[0]) * texth.width
                )
                break
            for element in row:
                start = self._origin_x + distanceh + len(element) * texth.width

                self._colum_size.append(start)
                distanceh = distanceh + len(element) * texth.width + self._padding

        for row in self._table:
            start = self._origin_y + distancev + textv.height
            self._row_size.append(start)
            distancev = distancev + textv.height + self._padding

    def create_borders(self, color_index=2):
        """
        Create borders for the table


        """

        for distance in self._colum_size:
            draw_line(
                self._plotbitmap,
                distance,
                self._origin_y,
                distance,
                self._row_size[-1],
                color_index,
            )

        for distance in self._row_size:
            draw_line(
                self._plotbitmap,
                self._origin_x,
                distance,
                self._colum_size[-1],
                distance,
                color_index,
            )

    def create_label_objects(self):
        """
        Create label objects
        """

        if len(self._colum_size) == 2:
            for j, row in enumerate(self._table):
                text = bitmap_label.Label(
                    self._font_to_use, text=row, color=self._text_color
                )
                text.x = self._colum_size[0] + self._padding
                text.y = self._row_size[j] + self._padding - self._dy

                self.append(text)

        else:
            for j, row in enumerate(self._table):
                for i, cell_text in enumerate(row):
                    text = bitmap_label.Label(
                        self._font_to_use, text=cell_text, color=self._text_color
                    )
                    text.x = self._colum_size[i] + self._padding
                    text.y = self._row_size[j] - self._dy + self._padding

                    self.append(text)
