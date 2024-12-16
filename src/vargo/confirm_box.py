import curses

class VARGO_ConfirmBox:
    def __init__(self, table_win, width, title, message_lines = []):
        self.table_win = table_win
        self.width = width
        
        self.title = title
        self.message_lines = message_lines

        self.ok_selected = False
    
    def right(self):
        self.ok_selected = True
    
    def left(self):
        self.ok_selected = False
    
    def render(self):
        max_lines = 0 if self.message_lines is None or self.message_lines == [] else len(max(self.message_lines, key=len)) + 4
        box_width = max(55, max_lines)
        
        # ┌────────────────────────────────────────────────────────────────┐        
        self.table_win.addstr(4, (self.width - box_width - 2) // 2, u'\u250c' + u'\u2500' * box_width + u'\u2510', curses.color_pair(8))
        
        for i in range(4 + len(self.message_lines)):
            # │                                                                                 │ 
            self.table_win.addstr(i + 5, (self.width - box_width - 2) // 2, u'\u2502' + ' ' * box_width + u'\u2502', curses.color_pair(8))
        
        self.table_win.addstr(5, (self.width - len(self.title) - 2) // 2, self.title, curses.color_pair(2))
        
        i = 0
        for line in self.message_lines:
            i += 1
            self.table_win.addstr(5 + i, (self.width - box_width - 2) // 2 + 3, line, curses.color_pair(2))
        
        self.table_win.addstr(7 + len(self.message_lines), (self.width - 7 - 2) // 2, "Confirm", curses.color_pair(8))
        self.table_win.addstr(8 + len(self.message_lines), (self.width - 8 - 2) // 2 - 10, "[Cancel]", curses.color_pair(8) if self.ok_selected else curses.color_pair(9))
        self.table_win.addstr(8 + len(self.message_lines), (self.width - 2) // 2 + 10, "[OK]", curses.color_pair(9) if self.ok_selected else curses.color_pair(8))
        
        # └─────────────────────────────────────────────────────────────────────────────────┘
        self.table_win.addstr(9 + len(self.message_lines), (self.width - box_width - 2) // 2, u'\u2514' + u'\u2500' * box_width + u'\u2518', curses.color_pair(8))
        
        self.table_win.noutrefresh()