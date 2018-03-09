from .core import HorizontalBox, OutlineType, Box
from .utils import INF


class StringFiller(Box):
    def __init__(self, string, height=0, width=0,
                 parent_box=None, matrix=None,
                 weight=1, max_size=INF, min_size=0):
        Box.__init__(self, height, width, parent_box, matrix, weight,
                     max_size, min_size)
        self.set(string)

    def set(self, new_string):
        self._string = new_string.split('\n') if new_string is not None \
                       else self._string

    def resize(self, new_height, new_width):
        Box.resize(self, new_height, new_width)
        self.draw()

    def update(self, new_string=None):
        self.set(new_string)

    def draw(self):
        Box.draw(self)
        for row_idx in range(self.num_rows):
            for col_idx in range(self.num_cols):
                if row_idx < len(self._string) and col_idx < len(self._string[row_idx]):
                    self.matrix[row_idx][col_idx].set(self._string[row_idx][col_idx])
                else:
                    self.matrix[row_idx][col_idx].set(' ')


class StrBox(HorizontalBox):
    """A widget that displays a given string"""
    def __init__(self, string, height=0, width=0, parent_box=None,
                 matrix=None, weight=1, max_size=INF, min_size=0,
                 outline=OutlineType.No):
        HorizontalBox.__init__(self, height, width, parent_box, matrix, weight,
                               max_size, min_size, outline=outline)
        self.string_filler = StringFiller(string)
        self.add_child(self.string_filler)

    def update(self, new_string=None):
        self.string_filler.set(new_string)
        self.draw

    def draw(self):
        HorizontalBox.draw(self)


# class TreePrinterNode(object):
#     def __init__(self, string):
#         self.string = string
#         self.children = OrderedDict()
#
#     def add_child(self, )
#
#
# class TreePrinter(object):
#     """A class for storing tree information and displaying it as a string"""
#     def __init__(self):
