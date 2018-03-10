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
        self.draw()

    def draw(self):
        HorizontalBox.draw(self)


class LabeledProgressBar(HorizontalBox):
    def __init__(self, title, message=None, width=0, parent_box=None,
                 matrix=None, weight=1, max_size=INF, min_size=0, outline=OutlineType.No):
        self.title = title
        self.message = message
        self.percentage = 0
        HorizontalBox.__init__(self, height=3, width=width, parent_box=parent_box,
                               matrix=matrix, weight=weight, max_size=max_size, min_size=min_size,
                               outline=OutlineType.HorizontalBounds)

    def update(self, percentage=None, title=None, message=None):
        self.title = title if title is not None else self.title
        self.message = message if message is not None else self.message
        self.percentage = percentage if percentage is not None else self.percentage
        self.draw()

    def stretch(self, new_width=None):
        HorizontalBox.resize(self, new_width=new_width)

    def _gen_progress_bar(self, width):
        bar_length = width - 6
        filled = int(self.percentage / 100.0 * bar_length)
        filled = filled if filled < 100 else 100
        filler = bar_length - filled
        return '[' + ('█' * filled) + (' ' * filler) + '{:3d}%]'.format(self.percentage)

    def _gen_message_bar(self, width):
        msg_max = width
        if not self.message:
            return ' ' * msg_max
        return self.message[:msg_max] + ' ' * (msg_max - len(self.message))

    def _gen_title_bar(self, width):
        msg_max = width - 2
        if not self.title:
            return '[]' + '─' * msg_max
        return '[' + self.title[:msg_max] + ']' + '─' * (msg_max - len(self.title))

    def draw(self):
        Box.draw(self)
        height, width, h_offset, v_offset = self._outline_offsets()
        title_row = self.matrix[v_offset]
        message_row = self.matrix[v_offset + 1]
        progress_row = self.matrix[height - 1]
        [progress_row[i+h_offset].set(c)
         for i, c in enumerate(self._gen_progress_bar(width)) if i+h_offset < len(progress_row)]
        [message_row[i+h_offset].set(c)
         for i, c in enumerate(self._gen_message_bar(width)) if i+h_offset < len(message_row)]
        [title_row[i+h_offset].set(c)
         for i, c in enumerate(self._gen_title_bar(width)) if i+h_offset < len(title_row)]

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
