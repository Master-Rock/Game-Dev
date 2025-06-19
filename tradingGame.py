import pygame as pg
import pandas as pd


pg.init()


#region color library
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
white = (255,255,255)
black = (0,0,0)
purple = (127,0,255)
orange = (255,165,0)
#endregion


#region game settings
screen = pg.display.set_mode([300,450])
pg.display.set_caption("Trading Game")
background = black
framerate = 60
font = pg.font.Font("freesansbold.ttf",16)
timer = pg.time.Clock()
#endregion



# region game variables
money = 50
columns = ['Port','Gold','Iron','Sugar','Cloth']
data = [['Weight',30,20,10,5],
        ['A',50,30,20,5],
        ['B',55,28,18,10],
        ['C',45,33,17,8]]
df = pd.DataFrame(data,columns=columns)


inventory = pd.DataFrame([[1,0,0,0,0]],columns=columns)
#endregion



#draw variables
first_bar_y = 80
bar_space = 40
buy_rect_x = 45
buy_rect_y = 30
buy_rect_marg = 2

def draw_trade_rectangle(color, y_coord, buy_rect):
    if buy_rect:
        x_coord = 155
        text = "Buy"
    else:
        x_coord = 70
        text = "Sell"
    
    task =pg.draw.rect(screen,color,[x_coord,y_coord,buy_rect_x,buy_rect_y])
    pg.draw.rect(screen,black,[x_coord+buy_rect_marg,y_coord+buy_rect_marg,buy_rect_x-2*buy_rect_marg,buy_rect_y-2*buy_rect_marg])
    value_text = font.render(str(text),True, white)
    screen.blit(value_text,(x_coord+buy_rect_marg,y_coord+8))
    return task




running = True
while running:
    timer.tick(framerate)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.MOUSEBUTTONDOWN:
            for n in range(len(buys)):
                if buys[n].collidepoint(event.pos):
                    if money>=df.iloc[int(inventory['Port'].iloc[0])].iloc[n+1]:
                        money -=df.iloc[int(inventory['Port'].iloc[0])].iloc[n+1]
                        inventory.iloc[0].iloc[n+1] +=1
                if sells[n].collidepoint(event.pos):
                    if inventory.iloc[0].iloc[n+1] >= 1:
                        money +=df.iloc[int(inventory['Port'].iloc[0])].iloc[n+1]
                        inventory.iloc[0].iloc[n+1] -=1
            if sail.collidepoint(event.pos):
                if inventory.iloc[0].iloc[0] == 3:
                    inventory.iloc[0].iloc[0] = 1
                else:
                    inventory.iloc[0].iloc[0] +=1
    screen.fill(background)

    #drawing only
    buys = []
    sells = []
    for n,good in enumerate(columns[1:]):
        y_coord = first_bar_y+n*bar_space
        
        buys +=[draw_trade_rectangle(white,y_coord,True),]
        
        value_text = font.render(str(df.iloc[int(inventory['Port'].iloc[0])].iloc[n+1])+'$',True, white)
        screen.blit(value_text,(120+buy_rect_marg,y_coord+8))
        
        sells +=[draw_trade_rectangle(white,y_coord,False),]
        
        good_text = font.render(str(good),True, white)
        screen.blit(good_text,(10+buy_rect_marg,y_coord+8))
        
        inventory_text = font.render(str(good),True, white)
        screen.blit(inventory_text,(10+buy_rect_marg,y_coord+210))
        
        inventory_text = font.render(str(inventory[good].iloc[0]),True, white)
        screen.blit(inventory_text,(100+buy_rect_marg,y_coord+210))
        
    
        
    display_score = font.render("Money: $"+str(round(money,2)),True,white,black)
    screen.blit(display_score,(10,5))
    
    display_port = font.render("Port: "+str(df.iloc[inventory.iloc[0].iloc[0]][0]),True,white,black)
    screen.blit(display_port,(10,45))
    
    sail =pg.draw.rect(screen,white,[140-5,45-8,buy_rect_x,buy_rect_y])
    pg.draw.rect(screen,black,[140-5+buy_rect_marg,45+buy_rect_marg-8,buy_rect_x-2*buy_rect_marg,buy_rect_y-2*buy_rect_marg])
    value_text = font.render("Sail",True, white)
    screen.blit(value_text,(140,45))
    
    inv_h_text = font.render("Inventory:",True, white,black)
    screen.blit(inv_h_text,(10,250)) 
    
    
    
    

    pg.display.flip()

pg.quit()