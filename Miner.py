import pygame as pg
import random 
import multiprocessing as mp
import time
 #test

pg.init()


class Game:
    def __init__(self,manager):
        self.inventory = manager.dict({"Wood":0})
        self.tools = manager.dict({})
        self.free_machines = manager.dict({})
        self.total_machines = manager.dict({})
        self.durabilities = manager.dict({"Wood Pickaxe":10,
                             "Stone Pickaxe":30,
                             "Grinder":30})
        



    #region Recipes
    #region Gathering
    def hand_chop(self):
        if "Wood" in self.inventory:
            self.inventory["Wood"] += 1
        else:
            self.inventory["Wood"] = 1

    def mine(self):
        r = random.random()

        if r<0.5:
            if "Stone" in self.inventory:
                self.inventory["Stone"]+=1
            else:
                self.inventory["Stone"]=1
        elif r<0.7:
            
            if "Coal" in self.inventory:
                self.inventory["Coal"]+=1
            else:
                self.inventory["Coal"]=1
            coal +=1
        elif r<0.8:
            if "Copper" in self.inventory:
                self.inventory["Copper"]+=1
            else:
                self.inventory["Cooper"]=1
            copper +=1
        elif r<0.9:
            if "Tin" in self.inventory:
                self.inventory["Tin"]+=1
            else:
                self.inventory["Tin"]=1
            tin +=1
        else:
            if "Iron" in self.inventory:
                self.inventory["Iron"]+=1
            else:
                self.inventory["Iron"]=1

    def wood_mine(self):
            if "Wood Pickaxe" in self.tools:
                if self.tools["Wood Pickaxe"] >= 1:
                    self.tools["Wood Pickaxe"] -= 1
                    self.mine(self)

    def stone_mine(self):
            if "Stone Pickaxe" in self.tools:
                if self.tools["Stone Pickaxe"] >= 1:
                    self.tools["Stone Pickaxe"] -=1
                    self.mine()
                    self.mine()



    #endregion

    #region Crafting

    def craft_wood_pick(self):
        if "Wood" not in self.inventory:
            return
        if self.inventory["Wood"] >=5:
            self.inventory["Wood"] -=5
            if "Wood Pickaxe" in self.tools:
                self.tools["Wood Pickaxe"] += self.durabilities["Wood Pickaxe"]
            else:
                self.tools["Wood Pickaxe"] = self.durabilities["Wood Pickaxe"]

    def craft_stone_pick(self):
        if "Wood" not in self.inventory or "Stone" not in self.inventory:
            return
        if self.inventory["Wood"] >=5 and self.inventory["Stone"] >=5:
            self.inventory["Wood"] -=5
            self.inventory["Stone"] -=5
            if "Stone Pickaxe" in self.tools:
                self.tools["Stone Pickaxe"] += self.durabilities["Stone Pickaxe"]
            else:
                self.tools["Stone Pickaxe"] = self.durabilities["Stone Pickaxe"]



    def craft_grinder(self):
        if "Stone" not in self.inventory:
            return
        
        if self.inventory["Stone"] >= 10:
            self.inventory["Stone"] -= 10
            if "Grinder" in self.tools:
                self.tools["Grinder"] += self.durabilities["Grinder"]
            else:
                self.tools["Grinder"] = self.durabilities["Grinder"]
                

    def craft_furnace(self):
        if "Stone" in self.inventory:
            if self.inventory["Stone"] >= 10:
                self.inventory["Stone"] -= 10
                if "Furnace" in self.total_machines:
                    self.free_machines["Furnace"] += 1
                    self.total_machines["Furnace"] += 1
                else:
                    self.free_machines["Furnace"] = 1
                    self.total_machines["Furnace"] = 1



    #endregion

    #region Grinder recipes

    #endregion

    #region Furnace recipes
    def furnace(self,timers,items):
        if "Furnace" not in self.total_machines:
            return 0,0
        timers = [t-1 for t in timers]
        for n,t in enumerate(timers):
            if t == 0:
                timers.pop(n)
                item = items.pop(n)
                self.free_machines["Furnace"] += 1
                if item in self.inventory:
                    self.inventory[item] += 1
                else:
                    self.inventory[item] = 1



    #endregion
    #endregion


    
def run(game):
    

    #region UI
    #region color library
    red = (255,0,0)
    green = (0,255,0)
    blue = (0,0,255)
    white = (255,255,255)
    black = (0,0,0)
    purple = (127,0,255)
    orange = (255,165,0)
    #endregion

    #region Screen
    framerate = 60
    surface = pg.display.set_mode([300,450])
    clock =pg.time.Clock()
    
    background = black
    
    font = pg.font.Font("freesansbold.ttf",16)
    timer = pg.time.Clock()
    #endregion
    
    def draw_button(game,y_coord):
        x_coord = 10
        #y_coord = 50
        width = 45
        height = 30
        color = blue
        margin = 2
        
        task =pg.draw.rect(surface,color,[x_coord,y_coord,width,height])
        pg.draw.rect(surface,black,[x_coord+margin,y_coord+margin,width-2*margin,height-2*margin])
        value_text = font.render(str(game.inventory["Wood"]),True, white)
        surface.blit(value_text,(x_coord+margin,y_coord+8))
        return task


    #endregion
    
    
    
    running = True
    furnace_timers = []
    furnace_items = []
    while running:
        pg.time.Clock().tick(framerate)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                if task1.collidepoint(event.pos):
                    game.hand_chop()
                if task2.collidepoint(event.pos):
                    mp.Process(target=run,args=(game,)).start()      
        
        
        if __name__ == '__main__':
            pg.display.set_caption("Main Game")
        else:
            pg.display.set_caption("Sub Game")
        
        y1 = 50
        y2 = 100
        task1 = draw_button(game,y1)
        task2 = draw_button(game,y2)
        
        furnace_timers,furnace_items = game.furnace(furnace_timers,furnace_items)
        
        pg.display.update()
    pg.quit()
    return
        


window_num = 2
if __name__ == '__main__':
    
    manager = mp.Manager() 
    game = Game(manager)
    run(game)
    
    #processes = []
    # for _ in range(window_num):
    #     processes += [mp.Process(target=run,args=(game,)),]
        
    # for process in processes:
    #     process.start()
        
    # for process in processes:
    #     process.join()
            
            


