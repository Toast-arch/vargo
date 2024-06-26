import curses

from .statics import VARGO_VERSION, VARGO_APPLICATIONS_KEYBIND_HELP, VARGO_LOGO

def render_header(headerwin, header_size, width, info_ip, info_port, vargo_status, special_message: str = None):
    headerwin.erase()
    
    headerwin.bkgd(' ', curses.color_pair(2))
    
    render_information(headerwin, info_ip, info_port)
    
    render_logo(headerwin, width)
    
    keybind_help_list = VARGO_APPLICATIONS_KEYBIND_HELP
    
    render_keybind_help(headerwin, header_size, width, keybind_help_list)
    
    if special_message is not None:
        render_special_message(headerwin, header_size, width, special_message)
    
    headerwin.noutrefresh()
    
def render_information(headerwin, info_ip, info_port):
    # Turning on attributes for title
    headerwin.attron(curses.color_pair(1))
    headerwin.attron(curses.A_BOLD)

    # Rending title information
    headerwin.addstr(0, 1, "ArgoCD IP: ")
    headerwin.addstr(1, 1, "ArgoCD Port: ")
    headerwin.addstr(2, 1, "Vargo Version: ")

    headerwin.addstr(0, 16, info_ip, curses.color_pair(2))
    headerwin.addstr(1, 16, info_port, curses.color_pair(2))
    headerwin.addstr(2, 16, VARGO_VERSION, curses.color_pair(2))
    
    # Turning off attributes for title
    headerwin.attroff(curses.color_pair(1))
    headerwin.attroff(curses.A_BOLD)

def render_keybind_help(headerwin, header_size, width, keybind_help_list):
    # Render keybind sheet
    for i in range(min(header_size - 1, len(keybind_help_list))):
        headerwin.addstr(i, width // 2 - len(keybind_help_list[i][0]) - 3 - 5, "<{}>".format(keybind_help_list[i][0]), curses.color_pair(4))
        headerwin.addstr(i, width // 2 - 5, keybind_help_list[i][1], curses.color_pair(6))

def render_logo(headerwin, width):
    # Turning on attributes for title
    headerwin.attron(curses.color_pair(1))
    headerwin.attron(curses.A_BOLD)

    # Getting title length
    max_title_length = len(max(VARGO_LOGO.split('\n'), key=len))

    # Rendering title
    for i in range(6):
        headerwin.addstr(i, width - max_title_length - 1, VARGO_LOGO.split('\n')[i])
    
    # Turning off attributes for title
    headerwin.attroff(curses.color_pair(1))
    headerwin.attroff(curses.A_BOLD)

def render_loading_logo(stdscr, width):
    # Turning on attributes for title
    stdscr.attron(curses.color_pair(1))
    stdscr.attron(curses.A_BOLD)

    # Getting title length
    max_title_length = len(max(VARGO_LOGO.split('\n'), key=len))

    # Rendering title
    for i in range(6):
        stdscr.addstr(i + 2, (width - max_title_length) // 2, VARGO_LOGO.split('\n')[i])
    
    # Turning off attributes for title
    stdscr.attroff(curses.color_pair(1))
    stdscr.attroff(curses.A_BOLD)

def render_special_message(stdscr, header_size, width, special_message):
    # Turning on attributes for special
    stdscr.attron(curses.color_pair(5))
    stdscr.attron(curses.A_BOLD)
    
    stdscr.addstr(header_size - 2, (width - len(special_message)) // 2, special_message)
    
    # Turning off attributes for special
    stdscr.attroff(curses.color_pair(5))
    stdscr.attroff(curses.A_BOLD)