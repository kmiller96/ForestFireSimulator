import curses
from time import time
import sys

from forest_fire.board import Board


class TerminalGUI:

    def __init__(self, engines):
        self.board = None
        self.engines = engines
    
    def start(self):
        @curses.wrapper
        def main(stdscr):
            stdscr.clear()
            stdscr.nodelay(True)
            stdscr.border()

            ydim, xdim = stdscr.getmaxyx()
            self.board = Board(xdim-2, ydim-2)

            while True:
                c = stdscr.getch()
                if c == ord("q"):
                    sys.exit(0)
                else:
                    for engine in self.engines:
                        engine.step(self.board)
                    
                    for (x, y), cell in self.board.enumerate():
                        stdscr.addstr(y+1, x+1, str(cell))
                    
                    stdscr.refresh()

            return
        return
    