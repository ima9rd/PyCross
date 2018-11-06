import random
# PyCross!
DIMENSIONS = [10, 10]
RESOLUTION = [600, 600]

def generate_board():
    board = []
    for y in range(DIMENSIONS[1]):
        row_temp = []
        for x in range(DIMENSIONS[0]):
            row_temp.append(random.randint(0,1))
        board.append([1 if x==1 else None for x in row_temp])
    return board


def check_board(entries, canvas):
    for row_idx, row in enumerate(board):
        for val_idx, val in enumerate(row):
            if entries[row_idx][val_idx]:
                color = canvas.itemcget(entries[row_idx][val_idx], 'fill')
            else:
                color = ''
            if (val and not color == 'blue') or (not val and color == 'blue'):
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


board = generate_board()

row_desc = []
for row in board:
    row_desc.append(generate_desc(row))
column_desc = []
for i in range(DIMENSIONS[0]):
    tmp = []
    for n in range(DIMENSIONS[1]):
        tmp.append(board[n][i])
    column_desc.append(generate_desc(tmp))
    tmp = []


import tkinter as tk

# Create a grid of None to store the references to the tiles
tiles = [[None for _ in range(DIMENSIONS[1])] for _ in range(DIMENSIONS[0])]
padding = 100
outline = 5
def callback(event):
    # Get rectangle diameters
    col_width = (c.winfo_width() - 14 - padding)/DIMENSIONS[0]
    row_height = (c.winfo_height() - 14 - padding)/DIMENSIONS[1]
    # Calculate column and row number
    col = int((event.x-padding)//col_width)
    row = int((event.y-padding)//row_height)
    if event.x < padding + outline or event.y < padding + outline or col > 9 or row > 9:
        pass
    else:
        if event.num == 3:
            color = 'black'
        else:
            color = 'blue' 
        # If the tile is not filled, create a rectangle
        if not tiles[row][col]:
            tiles[row][col] = c.create_rectangle((col*col_width)+padding+outline, (row*row_height)+padding+outline, ((col+1)*col_width)+padding-outline, ((row+1)*row_height)+padding-outline, fill=color)
        # If the tile is filled, delete the rectangle and clear the reference
        else:
            c.delete(tiles[row][col])
            tiles[row][col] = None
        if check_board(tiles, c):
            c.quit()

# Create the window, a canvas and the mouse click event binding
root = tk.Tk()
c = tk.Canvas(root, width=RESOLUTION[0], height=RESOLUTION[1], borderwidth=5, background='white')
c.pack()
row_height = (RESOLUTION[1]-padding)/DIMENSIONS[1]
for i, val in enumerate(row_desc):
    string = '    '.join([str(i) for i in val])
    c.create_text(padding/2, (padding + row_height*i + int(row_height/2)), text=string)

row_width = (RESOLUTION[0]-padding)/DIMENSIONS[0]

for i, val in enumerate(column_desc):
    string = '\n'.join([str(i) for i in val])
    c.create_text((padding + (row_width*i) + row_width/2), padding/2, text=string)
c.create_rectangle(padding, padding, RESOLUTION[0], RESOLUTION[1])
for i in range(DIMENSIONS[0]):
    for n in range(DIMENSIONS[1]):
        c.create_rectangle((i*row_width)+padding, (n*row_height)+padding, ((i+1)*row_width)+padding, ((n+1)*row_height)+padding)
c.pack()
c.bind("<Button-1>", callback)
c.bind("<Button-3>", callback)

root.mainloop()
