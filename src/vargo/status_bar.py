import curses

class VARGO_Statusbar:
    def __init__(self, statusbarwin, width) -> None:
        self.statusbarwin = statusbarwin
        self.width = width
        
        self.color_pair = curses.color_pair(2)
        
        self.message = ""
    
    def render_message(self, message, warning: bool = False):
        self.message = message[:self.width - 4]
        
        if warning:
            self.color_pair = curses.color_pair(22)
        else:
            self.color_pair = curses.color_pair(2)
        
        self.render()
    
    def render(self):
        self.statusbarwin.erase()
        
        self.statusbarwin.bkgd(' ', self.color_pair)
        
        self.statusbarwin.addstr(0, 3, self.message, self.color_pair)
        
        self.statusbarwin.noutrefresh()