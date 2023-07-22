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
from adafruit_bitmap_font import bitmap_font  # pylint: disable=wrong-import-position
from bitmaptools import draw_line
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

    """

    def __init__(
        self,
        originx,
        originy,
        width=480,
        height=320,
        table: list = None,
        font_file=None,
    ) -> None:
        super().__init__(x=0, y=0, scale=1)

        self._origin_x = originx
        self._origin_y = originy
        self._width = width
        self._height = height
        self._table = table
        self._padding = 3
        self._plotbitmap = displayio.Bitmap(width, height, 20)

        plot_palette = displayio.Palette(20)
        plot_palette.make_transparent(0)
        plot_palette[1] = 0xFFFFFF
        plot_palette[2] = 0xFF0000
        plot_palette[3] = 0x00FF00
        plot_palette[4] = 0x0000FF
        plot_palette[5] = 0xFFFF00
        plot_palette[6] = 0x00FFFF
        plot_palette[7] = 0x123456
        plot_palette[8] = 0x654321
        plot_palette[9] = 0x000000

        self._canvas = displayio.TileGrid(
            self._plotbitmap, pixel_shader=plot_palette, x=0, y=0
        )
        self.append(
            displayio.TileGrid(self._plotbitmap, pixel_shader=plot_palette, x=0, y=0)
        )

        self._font_to_use = bitmap_font.load_font(font_file)
        width, height, _, self._dy = self._font_to_use.get_bounding_box()

        self.create_label_objects()

    def create_borders(self, originx, originy, text_lenght, text_height, color_index):
        """
        Create borders for the table
        """
        draw_line(
            self._plotbitmap,
            originx - self._padding,
            originy + self._dy - self._padding,
            originx + text_lenght + self._padding,
            originy + self._dy - self._padding,
            color_index,
        )

        draw_line(
            self._plotbitmap,
            originx - self._padding,
            originy + self._dy - self._padding,
            originx - self._padding,
            originy + self._dy + text_height,
            color_index,
        )

        draw_line(
            self._plotbitmap,
            originx - self._padding,
            originy + self._dy + text_height,
            originx + text_lenght + self._padding,
            originy + self._dy + text_height,
            color_index,
        )

        draw_line(
            self._plotbitmap,
            originx + text_lenght + self._padding,
            originy + self._dy - self._padding,
            originx + text_lenght + self._padding,
            originy + self._dy + text_height,
            color_index,
        )

    def create_label_objects(self, color_index=2):
        """
        Create label objects
        """
        deltay = 0

        for row in self._table:
            deltax = 0
            if len(row) > 1:
                for cell_text in row:
                    text = bitmap_label.Label(self._font_to_use, text=cell_text)
                    text.x = self._origin_x + deltax
                    text.y = self._origin_y + deltay

                    self.create_borders(
                        self._origin_x + deltax,
                        self._origin_y + deltay,
                        text.bitmap.width,
                        text.bitmap.height,
                        color_index,
                    )
                    self.append(text)
                    deltax = deltax + self._padding * 2 + text.bitmap.width
                deltay = deltay + self._padding * 2 + self._dy + text.bitmap.height
