import curses
import json
import time

from .statics import APPLICATIONS_INDEX_BAR, VARGO_CONF_PATH
from .statics import VARGO_TABLE_STATUS_APPLICATIONS, TEXTPAD_OFF, TEXTPAD_CMD, TEXTPAD_EDIT, TEXTPAD_FILTER
from .statics import KEY_DOWN, KEY_ENTER, KEY_Q, KEY_UP, KEY_LEFT, KEY_RIGHT, KEY_A, KEY_BACKSLASH, KEY_BACKSPACE, KEY_COLON, KEY_ESCAPE, KEY_F, KEY_P, KEY_R, KEY_SHIFT_R, KEY_G, KEY_SHIFT_G, KEY_H, KEY_SHIFT_P, KEY_E
from .statics import curses_init_color_pairs

from .header import render_loading_logo, render_header
from .textpad import VARGO_Textpad
from .table import render_table
from .status_bar import VARGO_Statusbar
from .confirm_box import VARGO_ConfirmBox

class Vargo:
    def __init__(self, stdscr, debug: bool = False):
        self.debug = debug
        
        self.stdscr = stdscr
        
        # INIT CURSES
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        self.stdscr.keypad(1)
        
        curses_init_color_pairs()
        
        # INIT Vargo
        self.vargo_conf = {}
        # self.get_vargo_conf()
        
        # Clearing the screen is mandatory
        self.stdscr.refresh()
        
        # INIT VARIABLES
        self.ip = "todo"
        self.port = "todo"
                
        self.height, self.width = stdscr.getmaxyx()
        
        self.header_size = 6
        
        self.table_size = self.height - self.header_size - 1
        
        self.textpad_mode = TEXTPAD_OFF
        self.status = VARGO_TABLE_STATUS_APPLICATIONS
        
        self.confirm_on = False
        self.confirm_cmd = None        
        
        self.table_title = ""
        self.table_title_save = ""
        self.table_index_bar = []
        self.table_content = []
        self.table_content_save = None
        
        self.regex_filter_text = None
        
        self.status_message = ""
        self.special_message = None
        
        self.scroll_index = 0
        
        self.selected_line = 1
        
        # INIT WINDOWS
        self.headerwin = curses.newwin(self.header_size, self.width, 0, 0)
        self.textpadwin = None
        self.tablewin = curses.newwin(self.table_size, self.width, self.header_size, 0)
        
        self.textpad: VARGO_Textpad = None
        self.statusbar = VARGO_Statusbar(curses.newwin(1, self.width, self.height - 1, 0), self.width)
        
        self.confirmbox: VARGO_ConfirmBox = None
        
        # SET TABLE TO APPLICATIONS
        self.table_title = "Applications"
        self.table_index_bar = APPLICATIONS_INDEX_BAR
        self.table_content = []
        
        # FIRST RENDERS
        render_loading_logo(stdscr, self.width)
        stdscr.noutrefresh()
        curses.doupdate()
        
        time.sleep(0.5)
        
        render_header(self.headerwin, self.header_size, self.width, self.ip, self.port, self.status, self.special_message)
        render_table(self.tablewin, self.table_size, self.width, self.table_title, self.table_index_bar, self.table_content, self.scroll_index, self.selected_line)
        self.statusbar.render()
        
        # FIRST DOUPDATE        
        curses.doupdate()
        
        self.run_vargo()
    
    def run_vargo(self):
        while True:
            key = self.stdscr.getch()
            
            if self.textpad_mode is not TEXTPAD_OFF:
                if key == KEY_ESCAPE:
                    self.turn_off_keypad()
                elif key == KEY_ENTER:
                    if self.apply_command(self.textpad.text):
                        break
                elif key == KEY_BACKSPACE:
                    self.textpad.del_last_chr()
                    self.textpad.render()
                else:
                    self.textpad.add_chr(key)
                    self.textpad.render()
            elif key == KEY_COLON and self.textpad is None:
                self.turn_on_keypad(TEXTPAD_CMD)
            elif key == KEY_BACKSLASH and self.textpad is None:
                self.turn_on_keypad(TEXTPAD_FILTER)
            else:
                continue
            
            render_table(self.tablewin, self.table_size, self.width, self.table_title, self.table_index_bar, self.table_content, self.scroll_index, self.selected_line)
            
            if self.confirm_on and self.confirmbox is not None:
                self.confirmbox.render()
            
            curses.doupdate()
        
        # STOP CURSES
        self.stdscr.keypad(False)
        curses.nocbreak()
        curses.echo()
        curses.endwin()
        
        return 0
    
    def scroll_up(self):
        self.selected_line -= 1
        if self.selected_line < 1:
            self.selected_line = 1
            self.scroll_index -= 1
            if self.scroll_index < 0:
                self.scroll_index = 0
    
    def scroll_down(self):
        if self.selected_line < self.table_size - 3 and self.selected_line < len(self.table_content):
            self.selected_line += 1
        elif self.selected_line == self.table_size - 3 and self.table_size - 3 < len(self.table_content) and self.scroll_index < len(self.table_content) - self.table_size + 3:
            self.scroll_index += 1
    
    def scroll_to_top(self):
        self.scroll_index = 0
        self.selected_line = 1
    
    def scroll_to_bottom(self):
        self.selected_line = min(self.table_size - 3, len(self.table_content))
        if self.table_size - 3 < len(self.table_content):
            self.scroll_index = len(self.table_content) - self.table_size + 3
    
    def turn_on_keypad(self, textpad_mode):
        self.textpad_mode = textpad_mode
        
        self.table_size -= 3
        
        del self.tablewin
        self.tablewin = curses.newwin(self.table_size, self.width, self.header_size + 3, 0)
        
        self.textpadwin = curses.newwin(3, self.width, self.header_size, 0)
        self.textpad = VARGO_Textpad(self.textpadwin, self.width)
        
        self.textpad.render()
    
    def apply_command(self, cmd) -> bool:
        if cmd == 'q':
            return True
        
        self.turn_off_keypad()
        return False
    
    def turn_off_keypad(self):        
        self.table_size += 3
                        
        del self.textpadwin
        
        del self.textpad
        self.textpad = None
        
        self.textpad_mode = TEXTPAD_OFF
        
        del self.tablewin
        self.tablewin = curses.newwin(self.table_size, self.width, self.header_size, 0)
    
    def turn_on_filter(self, filter_text):
        self.turn_off_filter()
        
        # Apply filter
        self.regex_filter_text = filter_text
        
        self.selected_line = 1
        self.scroll_index = 0
        
        # Add filter to title
        self.table_title_save = self.table_title
        self.table_title += f" /{self.regex_filter_text}"
        
        if self.status == VARGO_TABLE_STATUS_APPLICATIONS:
            filtered_content = []
            
            for application in self.table_content:
                if self.regex_filter_text in application['name']:
                    filtered_content.append(application)
            
            self.table_content_save = self.table_content
            self.table_content = filtered_content
    
    def turn_off_filter(self):
        self.table_title = self.table_title_save
        
        if self.table_content_save is not None:
            self.table_content = self.table_content_save
            self.table_content_save = None
        
        self.regex_filter_text = None
    
    def turn_on_confirm_box(self, confirm_cmd, title, message_lines = []):
        self.confirmbox = VARGO_ConfirmBox(self.tablewin, self.width, title, message_lines)
        self.confirm_on = True
        
        self.confirm_cmd = confirm_cmd
    
    def apply_confirm(self, confirmed: bool):
        if confirmed:
            pass
        
        self.confirm_cmd = None

    def get_vargo_conf(self):
        with open(VARGO_CONF_PATH, 'r') as fd:
            self.vargo_conf = json.load(fd)

    def write_vargo_conf(self):
        with open(VARGO_CONF_PATH, 'w') as fd:
            json.dump(self.vargo_conf, fd, indent=4)

def keyboard_worker(stdscr, command_to_render_queue):
    while True:
        key = stdscr.getch()
        
        command_to_render_queue.put(("KEYBOARD", key))

def debug_message(stdscr, message):    
    stdscr.addstr(3, 0, ' ' + message + (' ' * 10))
    stdscr.noutrefresh()
    curses.doupdate()

def debug_message2(stdscr, message):    
    stdscr.addstr(4, 0, ' ' + message + (' ' * 10))
    stdscr.noutrefresh()
    curses.doupdate()