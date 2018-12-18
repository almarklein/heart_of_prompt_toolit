import sys
import time

# from prompt_toolkit.output.windows10 import Windows10_Output as TerminalApplication
# from prompt_toolkit.output.win32 import Win32Output as TheOutput

from guirminal import TerminalApplication


tapp = TerminalApplication(sys.__stdout__)

tapp.set_title("Hello!")
tapp.enter_alternate_screen()
tapp.erase_screen()
# tapp.set_cursor_visible(False)
tapp.flush()

time.sleep(1)


# tapp.set_attributes("red", 24)  -> what should go in here?

for i in range(20):
    tapp.cursor_goto(3+i, 5)
    tapp.write("HI there € ▁▂▃▄▅▆▇█")
    tapp.write("= ¦ - г г ¬ ¬ ¬ L L L - - - ¦ ¦")
    
tapp.flush()

time.sleep(2)
tapp.bell()
time.sleep(1)

# Reset
tapp.quit_alternate_screen()
# tapp.set_cursor_visible(True)
tapp.flush()
