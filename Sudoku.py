import pygame as pg
import pandas as pd


pg.init()


#region color library
white = (255,255,255)
black = (0,0,0)
gray = (128,128,128)

#endregion

#draw variables
thin_line = 4
thick_line = 8
square_side = 30


#region game settings
n = 3
#n = input("n")
window_size = n*n*square_side+thick_line*(n-1)+thin_line*n*(n-1)
print(window_size)
screen = pg.display.set_mode([window_size,window_size])
pg.display.set_caption("Sudoku")
background = black
framerate = 60
font = pg.font.Font("freesansbold.ttf",square_side)
timer = pg.time.Clock()

def draw_board(values):
    squares = []
    for Line in range(3):
        for Column in range(3):
            for line in range(3):
                for column in range(3):
                    x_coord = Line*(n*square_side+(n-1)*thin_line+(n-2)*thick_line)+line*(square_side+thin_line)
                    y_coord = Column*(n*square_side+(n-1)*thin_line+(n-2)*thick_line)+column*(square_side+thin_line)
                    squares += pg.draw.rect(screen,white,[x_coord,y_coord,square_side,square_side])
    
    for Line in range(3):
        for Column in range(3):
            for line in range(3):
                for column in range(3):
                    x_coord = Line*(n*square_side+(n-1)*thin_line+(n-2)*thick_line)+line*(square_side+thin_line)
                    y_coord = Column*(n*square_side+(n-1)*thin_line+(n-2)*thick_line)+column*(square_side+thin_line)
                    value_text = font.render(str(values[column+3*Column+9*line+27*Line]),True, black)
                    screen.blit(value_text,(x_coord+(square_side/5),y_coord+(square_side/15)))
    
    return squares            





#endregion



# region game variables

#endregion










running = True
while running:
    timer.tick(framerate)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        
    screen.fill(background)
    draw_board([0,]*81)

    
    

    pg.display.flip()