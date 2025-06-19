import pygame as pg

#print(pg.font.get_fonts())
pg.init()


#color library
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
white = (255,255,255)
black = (0,0,0)
purple = (127,0,255)
orange = (255,165,0)



screen = pg.display.set_mode([300,450])
pg.display.set_caption("Incremental Game")
background = black
framerate = 60
font = pg.font.Font("freesansbold.ttf",16)
timer = pg.time.Clock()


#region game variables
score = 0

green_value = 1
red_value = 2
blue_value = 3
orange_value = 4
purple_value = 5

draw_green = False
draw_red = False
draw_blue = False
draw_orange = False
draw_purple = False

green_length = 0
red_length = 0
blue_length = 0
orange_length = 0
purple_length = 0

green_speed = 5
red_speed = 4
blue_speed = 3
orange_speed = 2
purple_speed = 1
#endregion

#draw variables
first_bar_y = 50
bar_space = 50



def draw_task(color, y_coord, value, draw, length, speed):
    global score
    if draw and length <200:
        length += speed
    elif length >= 200:
        draw = False
        length = 0
        score += value
    task = pg.draw.circle(screen,color,(30,y_coord),20,5)
    pg.draw.rect(screen,color,[70,y_coord-15,200,30])
    pg.draw.rect(screen,black,[75,y_coord-10,190,20])
    pg.draw.rect(screen,color,[70,y_coord-15,length,30])
    value_text = font.render(str(value),True, white)
    screen.blit(value_text,(26,y_coord-8))
    return task, length, draw



running = True
while running:
    timer.tick(framerate)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.MOUSEBUTTONDOWN:
            if task1.collidepoint(event.pos):
                draw_green = True
            if task2.collidepoint(event.pos):
                draw_red = True
            if task3.collidepoint(event.pos):
                draw_blue = True
            if task4.collidepoint(event.pos):
                draw_orange = True
            if task5.collidepoint(event.pos):
                draw_purple = True
    screen.fill(background)

    #drawing only
    task1,green_length,draw_green = draw_task(green,first_bar_y,green_value,draw_green,green_length,green_speed)
    task2,red_length,draw_red = draw_task(red,first_bar_y+(bar_space *1),red_value,draw_red,red_length,red_speed)
    task3,blue_length,draw_blue = draw_task(blue,first_bar_y+(bar_space *2),blue_value,draw_blue,blue_length,blue_speed)
    task4,orange_length,draw_orange = draw_task(orange,first_bar_y+(bar_space *3),orange_value,draw_orange,orange_length,orange_speed)
    task5,purple_length,draw_purple = draw_task(purple,first_bar_y+(bar_space *4),purple_value,draw_purple,purple_length,purple_speed)

    display_score = font.render("Money: $"+str(round(score,2)),True,white,black)
    screen.blit(display_score,(10,5))

    pg.display.flip()

pg.quit()