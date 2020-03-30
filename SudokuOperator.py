"""
@author: Ollie
"""

from SudokuGUI import *

''' Main function to run through program '''
def main():
    game = gui()
    pygame.init()
    game.setup()   
    while True: 
        for event in pygame.event.get():
            if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.update()
            game.button_click()        
main()
