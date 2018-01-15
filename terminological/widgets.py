from .core import Box, OutlineType


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
