import curses

class VARGO_Textpad:
    def __init__(self, textpad_win, width):
        self.textpad_win = textpad_win
        self.width = width
        
        self.text = ""
    
    def add_chr(self, c):
        if len(self.text) < self.width - 7 and c > 31 and c < 127:
            self.text += chr(c)
    
    def del_last_chr(self):
        if len(self.text) > 0:
            self.text = self.text[:-1]
    
    def render(self):
        self.textpad_win.erase()
        
        self.textpad_win.bkgd(' ', curses.color_pair(2))
        
        # ┌────────────────────────────────────────────────────────────────┐        
        self.textpad_win.addstr(0, 1, u'\u250c' + u'\u2500' * (self.width - 4) + u'\u2510', curses.color_pair(8))
        
        # │                                                                                 │ 
        self.textpad_win.addstr(1, 1, u'\u2502' + ' ' * (self.width - 4) + u'\u2502', curses.color_pair(8))
        
        # └─────────────────────────────────────────────────────────────────────────────────┘
        self.textpad_win.addstr(2, 1, u'\u2514' + u'\u2500' * (self.width - 4) + u'\u2518', curses.color_pair(8))
        
        self.textpad_win.addstr(1, 3, "> " + self.text.ljust(self.width - 7), curses.color_pair(2))
        
        self.textpad_win.noutrefresh()
    