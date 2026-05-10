import board
print(board.board_id)
print([x for x in dir(board) if x.startswith(("D","IO","GP"))])
