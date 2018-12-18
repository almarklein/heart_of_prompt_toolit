import sys

from .output.vt100 import Vt100Output
from .output.win32 import Win32Output, is_conemu_ansi, is_win_vt100_enabled


output_methods = ['ask_for_cpr', 'bell', 'cursor_goto', 'cursor_move',
    'enter_alternate_screen', 'erase_down', 'erase_right', 'erase_screen',
    'flush', 'get_size', 'quit_alternate_screen', 'set_attributes',
    'set_autowrap', 'set_cursor_visible', 'set_mouse_support', 'set_title',
    'write']

methods_always_win32 = ('get_size',  # must use win32 version
                        'set_mouse_support',  # must use win32 version
                        # 'get_rows_below_cursor_position',  # win32 only
                        # 'scroll_buffer_to_prompt',  # win32 only
                        # 'set_bracketed_paste'  # wont work, even with vt100
                        # note that flush get special care on Windows 10
                        )


class TerminalApplication:
    
    def __init__(self, stdout=None):
        self._input = 1
        self._select_output(stdout)
    
    def _select_output(self, stdout=None):
        stdout = stdout or sys.__stdout__
    
        if sys.platform.startswith('win'):
            self._win32out = Win32Output(stdout)
            self._vt100out = Vt100Output(stdout)
            
            if is_win_vt100_enabled():
                for name in output_methods:
                    if name in methods_always_win32:
                        setattr(self, "_output_" + name, getattr(self._win32out, name))
                    else:
                        setattr(self, "_output_" + name, getattr(self._vt100out, name))
                self._output_flush = self._win32out.make_vt100_wrapping_flush(self._vt100out.flush)
            elif is_conemu_ansi():
                for name in output_methods:
                    if name in methods_always_win32:
                        setattr(self, "_output_" + name, getattr(self._win32out, name))
                    else:
                        setattr(self, "_output_" + name, getattr(self._vt100out, name))
                    
            else:
                for name in output_methods:
                    setattr(self, "_output_" + name, getattr(self._win32out, name))
            
        else:
            self._vt100out = Vt100Output(stdout)
            for name in output_methods:
                setattr(self, "_output_" + name, getattr(self._vt100out, name))
    
    ## From either input or output
    
    
    ## From input
    
    
    ## From output
    
    # fileno  stdout.fileno()
    
    def get_encoding(self):
        """
        Return the encoding for this output, e.g. 'utf-8'.
        (This is used mainly to know which characters are supported by the
        output the data, so that the UI can provide alternatives, when
        required.)
        """
        return self._output.encoding  # self.stdout.encoding
    
    def get_size(self):
        return self._output_get_size()
    
    # todo: set_alt_screen?
    def enter_alternate_screen(self):
        """ Go to the alternate screen buffer. (For full screen applications). """
        self._output_enter_alternate_screen()
        
    def quit_alternate_screen(self):
        """ Leave the alternate screen buffer.
        """ 
        self._output_quit_alternate_screen()
    
    def set_title(self, title):
        """ Set the terminal title. """
        self._output_set_title(title)

    def set_mouse_support(self, value):
        """ Enable or disable mouse. """
        self._output_set_mouse_support(value)

    def set_autowrap(self, value):  # todo: Unix only, or via vt100?
        """ Enable or disable auto line wrapping. """
        self._output_set_autowrap(value)
    
    def set_cursor_visible(self, value):  # todo: windows only, or via vt100?
        """ Set whether the cursor is visible.
        """
        self._output_set_cursor_visible(value)
    
    ##

    def set_attributes(self, attrs, color_depth):
        """ Set new color and styling attributes. Set to None to reset.
        """
        self._output_set_attributes(attrs, color_depth)

    def cursor_goto(self, row=0, column=0):
        """ Put cursor to given position. """
        self._output_cursor_goto(row, column)

    def cursor_move(self, row=0, column=0):
        """ Move cursor from the current position. Use negative values to go left/up."""
        self._output_cursor_move(row, column)
    
    def erase_screen(self):
        """ Erases the screen with the background colour and moves the cursor to
        home.
        """
        self._output_erase_screen()
    
    def erase_right(self):
        """
        Erases from the current cursor position to the end of the current line.
        """
        self._output_erase_right()
    
    def erase_down(self):
        """
        Erases the screen from the current line down to the bottom of the
        screen.
        """
        self._output_erase_down()
   
    def write(self, text):
        """ Write text (Terminal escape sequences will be removed/escaped.)
        """
        self._output_write(text)
    
    def flush(self):
        """ Flush any pending output.
        """
        self._output_flush()
   
    def bell(self):  # todo: windows only?
        """ Sound bell. """
        self._output_bell()
    
    def ask_for_cpr(self):  # todo: do?
        """
        Asks for a cursor position report (CPR).
        (VT100 only.)
        """
        self._output_ask_for_cpr()
