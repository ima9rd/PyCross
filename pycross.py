import random
import tkinter as tk
import time
import datetime


# PyCross!
DIMENSIONS = [10, 10]
RESOLUTION = [600, 600]
PADDING = 100
OUTLINE = 5

def generate_board():
    global board
    board = []
    for y in range(DIMENSIONS[1]):
        row_temp = []
        for x in range(DIMENSIONS[0]):
            row_temp.append(random.randint(0,1))
        board.append([1 if x==1 else None for x in row_temp])

def check_board(entries, canvas):
    global board
    entry_row, entry_col = describe_board(entries, canvas)
    board_row, board_col = describe_board(board)
    if entry_row != board_row or entry_col != board_col:
        return False
    return True

def generate_desc(value_list):
    vals = []
    i = 0
    for n in value_list:
        if not n:
            if i > 0:
                vals.append(i)
                i = 0
        else:
            i += 1
    if i > 0:
        vals.append(i)
    return vals

def describe_board(board, canvas=None):
    row_desc = []
    for row in board:
        row_temp = []
        if canvas:
            for cell in row:
                if cell:
                    if canvas.itemcget(cell, 'fill') == 'blue':
                        row_temp.append(1)
                    else:
                        row_temp.append(None)
                else:
                    row_temp.append(None)
        else:
            row_temp = row
        row_desc.append(generate_desc(row_temp))
    column_desc = []
    for i in range(DIMENSIONS[0]):
        tmp = []
        for n in range(DIMENSIONS[1]):
            if canvas:
                contents = board[n][i]
                if contents:
                    cell = canvas.itemcget(contents, 'fill')
                    if cell == 'blue':
                        val = 1
                    else:
                        val = 0
                else:
                    val = 0
            else:
                val = board[n][i]
            tmp.append(val)
        column_desc.append(generate_desc(tmp))
        tmp = []
    return row_desc, column_desc

def init_game(canvas):
    canvas.bind("<Button-1>", callback)
    canvas.bind("<Button-3>", callback)
    canvas.bind_all("<F5>", game_over_screen)
    canvas.delete('all')
    global board, tiles, start_time

    valid = False
    while not valid:
        generate_board()
        for row in board:
            if 1 in row:
                valid = True
    row_desc, column_desc = describe_board(board)
    tiles = [[None for _ in range(DIMENSIONS[1])] for _ in range(DIMENSIONS[0])]
    row_height = (RESOLUTION[1]-PADDING)/DIMENSIONS[1]
    for i, val in enumerate(row_desc):
        string = '    '.join([str(i) for i in val])
        canvas.create_text(PADDING/2, (PADDING + row_height*i + int(row_height/2)), text=string)
    row_width = (RESOLUTION[0]-PADDING)/DIMENSIONS[0]
    for i, val in enumerate(column_desc):
        string = '\n'.join([str(i) for i in val])
        canvas.create_text((PADDING + (row_width*i) + row_width/2), PADDING/2, text=string)
    canvas.create_rectangle(PADDING, PADDING, RESOLUTION[0], RESOLUTION[1])
    for i in range(DIMENSIONS[0]):
        for n in range(DIMENSIONS[1]):
            canvas.create_rectangle((i*row_width)+PADDING, (n*row_height)+PADDING, ((i+1)*row_width)+PADDING, ((n+1)*row_height)+PADDING, activewidth=1.5, fill='white')
    for i in range(int(DIMENSIONS[0]/5)+1):
        canvas.create_line(PADDING, (i*5*row_height)+PADDING, RESOLUTION[0], (i*5*row_height)+PADDING, width=1.5)
    if DIMENSIONS[0] // 5 > 0:
        canvas.create_line(PADDING, RESOLUTION[1], RESOLUTION[0], RESOLUTION[1], width=1.5)
    if DIMENSIONS[1] // 5 > 0:
        canvas.create_line(RESOLUTION[0], PADDING, RESOLUTION[0], RESOLUTION[1], width=1.5)
    for i in range(int(DIMENSIONS[1]/5)+1):
        canvas.create_line(PADDING + i*5*row_width, PADDING, PADDING + i*5*row_width, RESOLUTION[1], width=1.5)
    start_time = time.time()

def game_over(canvas):
    canvas.delete('all')
    global start_time
    canvas.create_text(RESOLUTION[0]/2, RESOLUTION[1]/2, text='You won! Total Time: {} - Click anywhere to begin a new game.'.format(datetime.timedelta(seconds=(time.time() - start_time))))
    canvas.bind("<Button-1>", game_over_screen)
    canvas.bind("<Button-3>", game_over_screen)

# Create a grid of None to store the references to the tiles

def game_over_screen(event):
    init_game(c)


def callback(event):
    # Get rectangle diameters
    global board, tiles
    col_width = (c.winfo_width() - 14 - PADDING)/DIMENSIONS[0]
    row_height = (c.winfo_height() - 14 - PADDING)/DIMENSIONS[1]
    # Calculate column and row number
    col = int((event.x-PADDING)//col_width)
    row = int((event.y-PADDING)//row_height)
    if event.x < PADDING + OUTLINE or event.y < PADDING + OUTLINE or col > DIMENSIONS[0]-1 or row > DIMENSIONS[1]-1:
        pass
    else:
        if event.num == 3:
            color = 'black'
        else:
            color = 'blue' 
        # If the tile is not filled, create a rectangle
        if not tiles[row][col]:
            tiles[row][col] = c.create_rectangle((col*col_width)+PADDING+OUTLINE, (row*row_height)+PADDING+OUTLINE, ((col+1)*col_width)+PADDING-OUTLINE, ((row+1)*row_height)+PADDING-OUTLINE, fill=color, state='disabled')
        # If the tile is filled, delete the rectangle and clear the reference
        else:
            c.delete(tiles[row][col])
            tiles[row][col] = None
        if check_board(tiles, c):
            game_over(c)


if __name__ == '__main__':
    # Create the window, a canvas and the mouse click event binding
    root = tk.Tk()
    c = tk.Canvas(root, width=RESOLUTION[0], height=RESOLUTION[1], borderwidth=5, background='white')
    global board, tiles, start_time
    init_game(c)
    c.pack()
    root.mainloop()
