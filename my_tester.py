'''
These are the testing boards to check the game. 
'''

'''
This is the empty sudoku box. 0 represents the empty box.
'''
EMPTY_SUDOKU = []
for m in range(0, 9):
  mid_value = []
  for n in range(0, 9):
    mid_value.append(0)
  EMPTY_SUDOKU.append(mid_value)



'''
This is a sample sudoku board where 0 represents the empty box. 
'''
TO_CHECK = [[0, 0, 0, 0, 8, 0, 3, 0, 7], [9, 7, 5, 4, 0, 0, 0, 0, 6], [8, 6, 3, 0, 0, 9, 0, 5, 1], [0, 0, 0, 0, 9, 4, 0, 7, 0], [0, 0, 8, 0, 1, 2, 0, 0, 0], [1, 3, 4, 6, 0, 5, 8, 0, 0], [0, 0, 7, 2, 5, 0, 0, 0, 0], [0, 0, 6, 9, 4, 0, 7, 0, 0], [4, 0, 9, 0, 0, 0, 0, 0, 8]]


'''
This is the completed game of the sudoku game of above sudoku board.
'''
TO_CHECK_WITH =  [[2, 4, 1, 5, 8, 6, 3, 9, 7], [9, 7, 5, 4, 3, 1, 2, 8, 6], [8, 6, 3, 7, 2, 9, 4, 5, 1], [6, 5, 2, 8, 9, 4, 1, 7, 3], [7, 9, 8, 3, 1, 2, 6, 4, 5], [1, 3, 4, 6, 7, 5, 8, 2, 9], [3, 1, 7, 2, 5, 8, 9, 6, 4], [5, 8, 6, 9, 4, 3, 7, 1, 2], [4, 2, 9, 1, 6, 7, 5, 3, 8]]