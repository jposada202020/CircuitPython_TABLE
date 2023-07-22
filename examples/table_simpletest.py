# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

import board
from table import Table

my_table = Table(
    50,
    50,
    480,
    320,
    [("---------", "---------", "---------", "---------")],
    [("Heya", "I am", "Jose!", "YAY!"), ("Hello", "I am", "Blinka", "YAY!")],
    "fonts/LeagueSpartan-Bold-16.bdf",
)

display = board.DISPLAY
display.show(my_table)
