import curses

# Local module imports
from .utils import split, INF
from .utils import matrix_slice, matrix_to_string, compute_sizes

# Global screen pointer
SCREEN = None


class Cell(object):
    def __init__(self, character=' ', fg=None, bg=None):
        self._character = character
        self._fg = fg
        self._bg = bg
        self._updated = True

    @property
    def character(self):
        return self._character

    @character.setter
    def character(self, value):
        self._character = value

    @property
    def foreground(self):
        return self._fg

    @foreground.setter
    def foreground(self, value):
        self._fg = value

    @property
    def background(self):
        return self._bg

    @background.setter
    def background(self, value):
        self._bg = value

    def set(self, character, fg=None, bg=None):
        if self.character != character:
            self.character = character
            self._updated = True
        if fg:
            self.foreground = fg
            self._updated = True
        if bg:
            self.background = bg
            self._updated = True
        return self._updated

    def draw(self, row, col):
        if self._updated:
            if SCREEN:
                # display the character in the terminal
                SCREEN.addstr(row, col, self._character)
            self._updated = False


def gen_matrix(num_rows, num_cols):
    return [[Cell() for c in range(num_cols)] for r in range(num_rows)]


def string_to_matrix(string):
    string = string.split('\n')
    num_rows = len(string)
    num_cols = len(string[0])
    M = gen_matrix(num_rows, num_cols)
    for r, R in enumerate(M):
        for c, C in enumerate(R):
            C.set(string[r][c])
    return M


def resize_matrix(matrix, height, width):
    # Note that most terminals are much wider than they are tall
    # therefore it is more efficient to do height adjustments first
    current_height = len(matrix)
    current_width = 0 if not matrix else len(matrix[0])
    height_d = height - current_height
    width_d = width - current_width
    if height_d > 0:
        # add on from the bottom
        [matrix.append([Cell() for _ in range(current_width)])
         for _ in range(height_d)]
    elif height_d < 0:
        # shrink from the bottom
        [matrix.pop() for _ in range(0-height_d)]
    current_height = height
    
    if width_d > 0:
        # add on from the side
        [[row.append(Cell()) for _ in range(width_d)]
         for row in matrix]
    elif width_d < 0:
        # shrink from the side
        [[row.pop() for _ in range(0-width_d)] for row in matrix]
    current_width = width


class OutlineType(object):
    No = 0
    Box = 1
    HorizontalBounds = 2
    VerticalBounds = 3
    HorizontalBoundBox = 4
    VerticalBoundBox = 5


class Box(object):
    def __init__(self, height=0, width=0, parent_box=None, matrix=None,
                 weight=1, max_size=INF, min_size=0, outline=OutlineType.No):
        self.matrix = None
        self.parent_box = parent_box
        self.weight = weight
        self.max_size = max_size
        self.min_size = min_size
        self.matrix = matrix
        self.outline = outline
        if not self.matrix:
            self.matrix = gen_matrix(height, width)
        self.children = []

    def _draw_outline_corners(self):
        if len(self.matrix) > 0 and len(self.matrix[0]) > 0:
            self.matrix[0][0].set('┌')
            self.matrix[0][self.width-1].set('┐')
            self.matrix[self.height-1][0].set('└')
            self.matrix[self.height-1][self.width-1].set('┘')

    def _draw_outline_top_bottom(self, character='─'):
        if len(self.matrix) > 0 and len(self.matrix[0]) > 0:
            [c.set(character) for c in self.matrix[0][1:-1]]
            [c.set(character) for c in self.matrix[self.height-1][1:-1]]

    def _draw_outline_right_left(self, character='│'):
        if len(self.matrix) > 0 and len(self.matrix[0]) > 0:
            [r[0].set(character) for r in self.matrix[1:-1]]
            [r[self.width-1].set(character) for r in self.matrix[1:-1]]

    def _outline_offsets(self):
        if self.outline == OutlineType.No:
            return self.height, self.width, 0, 0
        elif self.outline in {OutlineType.Box,
                              OutlineType.HorizontalBoundBox,
                              OutlineType.VerticalBoundBox}:
            return self.height - 2, self.width - 2, 1, 1
        elif self.outline == OutlineType.HorizontalBounds:
            return self.height, self.width - 2, 1, 0
        elif self.outline == OutlineType.VerticalBounds:
            return self.height - 2, self.width, 0, 1

    @property
    def num_rows(self):
        return len(self.matrix)

    @property
    def num_cols(self):
        return 0 if not self.matrix else len(self.matrix[0])

    @property
    def height(self):
        return self.num_rows

    @property
    def width(self):
        return self.num_cols

    def set_matrix(self, matrix):
        self.matrix = matrix

    def add_child(self, child):
        self.children.append(child)
        child.parent_box = self
        self.resize(self.height, self.width)
        return self

    def resize(self, new_height, new_width):
        # if this is the base box, resize to screen size
        if self.parent_box is None and SCREEN:
            height, width = SCREEN.getmaxyx()
            width -= 1
        else:
            height = new_height if new_height is not None else self.height
            width = new_width if new_width is not None else self.width
        # if this is the base box, resize the matrix
        if self.parent_box is None:
            resize_matrix(self.matrix, height, width)
        self.set_matrix(matrix_slice(self.matrix, 0, height, 0, width))

    def draw(self):
        # draw the outline
        if self.outline == OutlineType.Box:
            self._draw_outline_corners()
            self._draw_outline_right_left()
            self._draw_outline_top_bottom()
        elif self.outline in {OutlineType.HorizontalBounds,
                              OutlineType.HorizontalBoundBox}:
            self._draw_outline_corners()
            self._draw_outline_right_left()
            self._draw_outline_top_bottom(' ')
        elif self.outline in {OutlineType.VerticalBounds,
                              OutlineType.VerticalBoundBox}:
            self._draw_outline_corners()
            self._draw_outline_top_bottom()
            self._draw_outline_right_left(' ')
        [c.draw() for c in self.children]
        # if this is the base box, refresh
        if self.parent_box is None and SCREEN:
            # render each cell
            [[cell.draw(r, c) for c, cell in enumerate(row)]
             for r, row in enumerate(self.matrix)]
            SCREEN.refresh()

    def __str__(self):
        return matrix_to_string(self.matrix)


class Filler(Box):
    def __init__(self, character, height=0, width=0,
                 parent_box=None, matrix=None,
                 weight=1, max_size=INF, min_size=0):
        Box.__init__(self, height, width, parent_box, matrix, weight,
                     max_size, min_size)
        self.character = character

    def resize(self, new_height, new_width):
        Box.resize(self, new_height, new_width)
        self.draw()

    def draw(self):
        Box.draw(self)
        for r in range(self.num_rows):
            for c in range(self.num_cols):
                self.matrix[r][c].set(self.character)

    
class VerticalBox(Box):
    def resize(self, new_height=None, new_width=None):
        Box.resize(self, new_height, new_width)
        # control for outlines
        height, width, h_offset, v_offset = self._outline_offsets()
        # compute the new sizes for the children elements
        heights = compute_sizes([(0, c.weight, c.min_size, c.max_size)
                                 for c in self.children], height)
        sizes = [(int(h[0]), width) for h in heights]
        # update their matrices
        for i, c in enumerate(self.children):
            h, w = sizes[i]
            c.set_matrix(matrix_slice(self.matrix, v_offset, h,
                                      h_offset, w))
            v_offset += h
            # call their own resize functions
            c.resize(new_height=h, new_width=w)
        self.draw()
    

class HorizontalBox(Box):
    def resize(self, new_height=None, new_width=None):
        Box.resize(self, new_height, new_width)
        # control for outlines
        height, width, h_offset, v_offset = self._outline_offsets()
        # compute the new sizes for the children elements
        widths = compute_sizes([(0, c.weight, c.min_size, c.max_size)
                                for c in self.children], width)
        sizes = [(height, int(w[0])) for w in widths]
        # update their matrices
        for i, c in enumerate(self.children):
            h, w = sizes[i]
            c.set_matrix(matrix_slice(self.matrix, v_offset, h, h_offset, w))
            h_offset += w
            # call their own resize functions
            c.resize(new_height=h, new_width=w)
        self.draw()


def start(mainframe: Box, run_callback=None):
    # make the cursor invisible
    def wrapped_main(stdscr):
        global SCREEN
        SCREEN = stdscr
        curses.curs_set(0)
        # Clear screen
        SCREEN.clear()
        r, c = SCREEN.getmaxyx()
        mainframe.resize(r, c-1)
        if run_callback is not None:
            run_callback()
    curses.wrapper(wrapped_main)


def screen_to_string():
    if not SCREEN:
        return ''
    else:
        result = []
        h, w = SCREEN.getmaxyx()
        for r in range(h):
            result.append([])
            for c in range(w-1):
                result[-1].append(chr(SCREEN.inch(r, c)))
        return '\n'.join([''.join([c for c in line]) for line in result])


class MsgLog(Box):
    """An automatically scrolling message box similar to a terminal"""
    def __init__(self, history_max=200, height=0, width=0, parent_box=None,
                 matrix=None, weight=1, max_size=INF, min_size=0,
                 outline=OutlineType.No):
        Box.__init__(self, height, width, parent_box, matrix, weight,
                     max_size, min_size, outline=outline)
        self.history_max = history_max
        self.message_history = []
        
    def add_message(self, msg):
        if len(self.message_history) >= self.history_max:
            self.message_history.pop(0)
        self.message_history.append(msg)
        self.draw()

    def _print_line(self, h_offset, v_offset, line, width):
        row = self.matrix[v_offset]
        [row[i+h_offset].set(ch) for i, ch in enumerate(line) if i < width]
        [row[i].set(' ')
         for i in range(len(line) + h_offset, width + h_offset)]

    def draw(self):
        Box.draw(self)
        height, width, h_offset, v_offset = self._outline_offsets()
        display = []
        for msg in reversed(self.message_history):
            display[0:0] = split(msg, width)
            for _ in range(len(display) - height):
                display.pop(0)
            if len(display) == height:
                break
        [display.append(' ' * width) for _ in range(height - len(display))]
        for i, line in enumerate(display):
            self._print_line(h_offset, i+v_offset, line, width)

