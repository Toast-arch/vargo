import curses

def render_table(tablewin, table_size: int, width: int, title: str, table_index_bar: list, table_content, scroll_index: int, selected_line: int):
    tablewin.erase()
    
    tablewin.bkgd(' ', curses.color_pair(2))
    
    attribute_slot_len = (width - 12 - len(table_index_bar[-1])) // (len(table_index_bar) - 1)
    
    render_table_surround(tablewin, table_size, width, title, len(table_content) if table_content is not None else 0)
    
    render_column_names(tablewin, width, table_index_bar, attribute_slot_len)
    
    render_scroll_arrow(tablewin, 1, len(table_index_bar[0]) + 4, scroll_index != 0, table_size - 3 < len(table_content) and scroll_index < len(table_content) - table_size + 3)
    
    render_content(tablewin, table_size, width, attribute_slot_len, table_content, scroll_index, selected_line)
    
    tablewin.noutrefresh()

def render_table_surround(tablewin, height, width, title: str, element_count: int):    
    # ┌───────────────────────────── Title [12] ───────────────────────────────────┐        
    tablewin.addstr(0, 1, u'\u250c' + u'\u2500' * (width - 4) + u'\u2510', curses.color_pair(8))
    
    full_title =  " {} [{}] ".format(title, element_count)
    tablewin.addstr(0, (width - len(full_title)) // 2, full_title, curses.color_pair(7))
    
    # │                                                                                 │ 
    for i in range(1, height - 1):
        tablewin.addstr(i, 1, u'\u2502', curses.color_pair(8))
        tablewin.addstr(i, width - 2, u'\u2502', curses.color_pair(8))
    
    # └─────────────────────────────────────────────────────────────────────────────────┘
    tablewin.addstr(height - 1, 1, u'\u2514' + u'\u2500' * (width - 4) + u'\u2518', curses.color_pair(8))

    tablewin.noutrefresh()

def render_column_names(tablewin, width, table_index_bar: list, attribute_slot_len):
    tablewin.addstr(1, 1, u'\u2502' + ' ' * (width - 4) + u'\u2502', curses.color_pair(8))
        
    i = 0
    for index_name in table_index_bar:
        tablewin.addstr(1, attribute_slot_len * i + 3, index_name)
        i += 1

    tablewin.noutrefresh()
    
def render_scroll_arrow(tablewin, pos_y, pos_x, more_up, more_down):
    arrows_str = ' '
    
    if more_up and more_down:
        arrows_str = '↕'
    elif more_up:
        arrows_str = '↑'
    elif more_down:
        arrows_str = '↓'
    
    tablewin.addstr(pos_y, pos_x, arrows_str, curses.color_pair(2))
    
    tablewin.noutrefresh()

def render_content(tablewin, table_size, width, attribute_slot_len, table_content, scroll_index, selected_line):
    if table_content is None:
        return
    
    render_applications(tablewin, table_size, width, attribute_slot_len, table_content, scroll_index, selected_line)

def render_applications(tablewin, table_size, width, attribute_slot_len, application_list: list, scroll_index, selected_line):
    line_index = 0
    
    if application_list is None or application_list == [] or type(application_list) is not list:
        return
    
    for application in application_list:
        line_index += 1
        
        if line_index - scroll_index > table_size - 3:
            break
        
        if line_index - 1 < scroll_index:
            continue
        
        color_pair_index = 10
        
        if selected_line == line_index - scroll_index:
            color_pair_index += 10
        
        color_pair = curses.color_pair(color_pair_index)
        
        # Print spaces
        tablewin.addstr(line_index + 1 - scroll_index, 3, ' '.ljust(width - 6), color_pair)
        
        values = [
            "" if 'namespace' not in application else application['namespace'],
            "" if 'name' not in application else application['name'],
            "" if 'sync' not in application else application['sync'],
            "" if 'health' not in application else application['health'],
        ]
        
        i = 0
        for value in values:
            tablewin.addstr(line_index + 1 - scroll_index, attribute_slot_len * i + 3, value if len(value) < attribute_slot_len else value[:attribute_slot_len - 4] + '...', color_pair)
            i += 1
        
        tablewin.noutrefresh()