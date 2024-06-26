import os
import sys
import curses

import argparse

from vargo.vargo import Vargo

def main(argv):
    parser = argparse.ArgumentParser()
    
    parser.prog = "vargo"
    parser.description = "Python visual interface to manage argocd from the terminal"
    
    parser.add_argument("--debug", action="store_true")
    
    args, unknownargs = parser.parse_known_args(argv)
    
    os.environ['TERM'] = 'xterm-256color'

    os.environ.setdefault('ESCDELAY','100') # in mS; default: 1000
    
    curses.wrapper(Vargo, args.debug)
    
    return 0

def run():
    return main(sys.argv[1:])

if __name__ == "__main__":
    run()
