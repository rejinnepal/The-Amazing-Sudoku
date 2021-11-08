'''
These are the settings the user can adjust in the game. For the entire functionality of the game, these values are adjusted the same throughout the game. This setting.py file has colour values, height and width of the pygame window, size of a box, and the testing_board 
'''



'''
These are the colours that are used in the game. You can look at the meaning of each colour in the my_readme file.
'''
COLOUR_WHITE = (255, 255, 255)
COLOUR_BLACK = (0, 0, 0)
COLOUR_PINK = (159, 43, 104)
COLOUR_PURPLE = (128, 0, 128)
COLOUR_CYAN = (0, 255, 255)
COLOUR_YELLOW = (255, 255, 0)
COLOUR_DARKRED = (139, 0, 0)
COLOUR_SKYPINK = (255, 100, 200)
FIXED_COLOUR = (187, 183, 198)
INCORRECT_COLOUR = (207, 198, 153)
HIGHLIGHTER = (189, 189, 189)




'''
These are the size (length and the height of the sudoku box)
'''
WIDTH = 601
HEIGHT = 601



'''
These are the positions and sizes of the square boxes in the sudoku game. 
'''
# This is the x-coordinate and y-coordinate of the sudoku box in the pygame window.
LOCATION = (80, 120) 

# This is the size of individual size.
SIZE = 50

# This is the size within which the user can click inside the box.
# L_SIZE = SIZE * 9 (The number of column)
L_SIZE = 450 


