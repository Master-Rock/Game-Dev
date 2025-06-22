import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame as pg
import random 
import multiprocessing as mp
import time
 #test

pg.init()





#region Game
class Game:
    def __init__(self,manager)->None:
        self.inventory = manager.dict({})
        self.free_machines = manager.dict({})
        self.total_machines = manager.dict({})
        
        
        self.durabilities = manager.dict({"Wood Pickaxe":10,
                                          "Wood Axe":10,
                                          "Stone Pickaxe":30,
                                          "Stone Axe":30,
                                          "Grinder":30})
        


    def get_tools(self)->dict:
        tools = ["Wood Pickaxe",
                 "Wood Axe",
                 "Stone Pickaxe",
                 "Stone Axe",
                 "Grinder"]
        
        result ={}
        for t in tools:
            if t in self.inventory:
                if self.inventory[t] > 0:
                    result[t] = self.inventory[t]
        return result


    def get_raw_materials(self)->dict:
        raw_materials = ["Wood",
                         "Stone",
                         "Coal",
                         "Copper",
                         "Tin",
                         "Iron"]
        values = {}
        for r in raw_materials:
            if r in self.inventory:
                values[r] = self.inventory[r]

        return values



    #region Gathering
    def chop(self)->None:
        if "Wood" in self.inventory:
            self.inventory["Wood"] += 1
        else:
            self.inventory["Wood"] = 1

    def hand_chop(self)->None:
        self.chop()

    def wood_chop(self)->None:
        if "Wood Axe" in self.inventory:
            if self.inventory["Wood Axe"] >=1:
                self.inventory["Wood Axe"] -=1
                self.chop()
                self.chop()
    
    def stone_chop(self)->None:
        if "Stone Axe" in self.inventory:
            if self.inventory["Stone Axe"] >=1:
                self.inventory["Stone Axe"] -=1
                self.chop()
                self.chop()
                self.chop()
                self.chop()


    def mine(self)->None:
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

        elif r<0.8:
            if "Copper" in self.inventory:
                self.inventory["Copper"]+=1
            else:
                self.inventory["Copper"]=1
        elif r<0.9:
            if "Tin" in self.inventory:
                self.inventory["Tin"]+=1
            else:
                self.inventory["Tin"]=1
        else:
            if "Iron" in self.inventory:
                self.inventory["Iron"]+=1
            else:
                self.inventory["Iron"]=1

    def wood_mine(self)->None:
            if "Wood Pickaxe" in self.inventory:
                if self.inventory["Wood Pickaxe"] >= 1:
                    self.inventory["Wood Pickaxe"] -= 1
                    self.mine()

    def stone_mine(self)->None:
            if "Stone Pickaxe" in self.inventory:
                if self.inventory["Stone Pickaxe"] >= 1:
                    self.inventory["Stone Pickaxe"] -=1
                    self.mine()
                    self.mine()





#endregion


#endregion





#region Recipe
class Recipe:
    def __init__(self,category:str, name:str,inputs:dict,outputs:dict) -> None:
        self.category = category
        self.name = name
        self.inputs = inputs
        self.outputs = outputs
        self.unlocked = False
    
    def craft(self,game:Game) -> None:
        craft = True
        for i in self.inputs.keys():
            if i not in game.inventory:
                craft = False
            elif game.inventory[i] <self.inputs[i]:
                craft = False
            
        if craft:
            for i in self.inputs.keys():
                game.inventory[i] -= self.inputs[i]
            for i in self.outputs.keys():
                if i in game.inventory:
                    game.inventory[i] += self.outputs[i]
                else:
                    game.inventory[i] = self.outputs[i]

    def check(self,game:Game) -> bool:
        if not self.unlocked:
            self.unlocked = True
            for i in self.inputs.keys():
                if i in game.inventory:
                    if game.inventory[i]<self.inputs[i]:
                        self.unlocked = False
                        return False
                else:
                    self.unlocked = False
                    return False
            return True
        return True

#endregion






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

#region UI measurements
x_header = 10
y_header = 10

x_subtitle = 20

x_normal = 10


#endregion

#region Screen setings
framerate = 60
surface = pg.display.set_mode([300,450])
clock =pg.time.Clock()

background = black

big_font = pg.font.Font("freesansbold.ttf",16)
subheader_font = pg.font.Font("freesansbold.ttf",13)
line_font = pg.font.Font("freesansbold.ttf",13)
timer = pg.time.Clock()
#endregion


#region UI functions
def draw_button(x_coord,y_coord,text,color):
    #x_coord = 10
    #y_coord = 50
    width = 80
    height = 30
    #color = blue
    margin = 2
    
    task =pg.draw.rect(surface,color,[x_coord,y_coord,width,height])
    pg.draw.rect(surface,black,[x_coord+margin,y_coord+margin,width-2*margin,height-2*margin])
    value_text = big_font.render(str(text),True, white)
    surface.blit(value_text,(x_coord+margin,y_coord+8))
    return task

#endregion





#region Tabs





#region Gathering tab
def Gathering_tab(game):
    pg.display.set_caption("Gathering Page")
    y_list_space = 15

    inventory_tab_running = True
    while inventory_tab_running:
        pg.time.Clock().tick(framerate)
        surface.fill(background)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                inventory_tab_running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                if hand_wood.collidepoint(event.pos):
                    game.hand_chop()
                if "Wood Pickaxe" in game.inventory:
                    if wood_mine.collidepoint(event.pos):
                        game.wood_mine()
                if "Wood Axe" in game.inventory:
                    if wood_chop.collidepoint(event.pos):
                        game.wood_chop()
                if "Stone Pickaxe" in game.inventory:
                    if stone_mine.collidepoint(event.pos):
                        game.stone_mine()
                if "Stone Axe" in game.inventory:
                    if stone_chop.collidepoint(event.pos):
                        game.stone_chop()



        #Header
        y=y_header
        header = big_font.render("Gather",True,white,black)
        surface.blit(header,(x_header,y))

        #subheading hand
        y+=20
        hand_subheading = subheader_font.render("Hand",True,white,black)
        surface.blit(hand_subheading,(x_subtitle,y))


        y_button_spacing = 40
        x1 = 10
        y += 20
        hand_wood = draw_button(x1,y,"Wood",blue)

        #subheading wood
        if "Wood Pickaxe" in game.inventory or "Wood Axe" in game.inventory:
            y+=30
            wood_subheading = subheader_font.render("Wood tools",True,white,black)
            surface.blit(wood_subheading,(x_subtitle,y))
        if "Wood Pickaxe" in game.inventory:
            y += y_button_spacing
            wood_mine = draw_button(x1,y,"Mine",green)
        if "Wood Axe" in game.inventory:
            y += y_button_spacing
            wood_chop = draw_button(x1,y,"Chop",green)


        #subheading Stone
        if "Stone Pickaxe" in game.inventory or "Stone Axe" in game.inventory:
            y+=30
            stone_subheading = subheader_font.render("Stone tools",True,white,black)
            surface.blit(stone_subheading,(x_subtitle,y))
        if "Stone Pickaxe" in game.inventory:
            y += y_button_spacing
            stone_mine = draw_button(x1,y,"Mine",green)
        if "Stone Axe" in game.inventory:
            y += y_button_spacing
            stone_chop = draw_button(x1,y,"Chop",green)





        pg.display.update()


        


    pg.quit()



#endregion





#region Inventory tab
def Inventory_tab(game):

    pg.display.set_caption("Inventory Page")
    y_list_space = 15
    

    inventory_tab_running = True
    while inventory_tab_running:
        pg.time.Clock().tick(framerate)
        surface.fill(background)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                inventory_tab_running = False

        #Header
        y=y_header
        header = big_font.render("Inventory",True,white,black)
        surface.blit(header,(x_header,y))

        #Subeheading Tools
        if "Wood Pickaxe" in game.inventory or "Wood Axe" in game.inventory:
            y+=20
            subtitle1 =subheader_font.render("Tools",True,white,black)
            surface.blit(subtitle1,(x_subtitle,y))
            
            #Tools
            tools = game.get_tools()

            for tool in tools:
                
                value = tools[tool]
                if value > 0:
                    y+= y_list_space
                    text =  str(value)+"-"+tool+" durability"
                    line = line_font.render(text,True,white,black)
                    surface.blit(line,(x_normal,y))


        #Subheading Raw Materials
        y+=20
        subtitle1 = subheader_font.render("Raw materials",True,white,black)
        surface.blit(subtitle1,(x_subtitle,y))

        #Raw Materials
        raw_materials = game.get_raw_materials()
        y += 10
        for material in raw_materials:
            y+= y_list_space
            value = raw_materials[material]
            text =  str(value)+"-"+material
            line = line_font.render(text,True,white,black)
            surface.blit(line,(x_normal,y))

        




        pg.display.update()


        


    pg.quit()






#endregion



class Item:
    def __init__(self):
        self.name = "hello"
        self.amount = 0

    def add(self,n):
        self.amount += n
#region Crafting tab


locked_recipes = []
unlocked_recipes = []
categories = []

wood_pick = Recipe("Wood tools","Pickaxe",{"Wood":5},{"Wood Pickaxe":10})
locked_recipes += [wood_pick,]

wood_axe = Recipe("Wood tools","Axe",{"Wood":5},{"Wood Axe":10})
locked_recipes += [wood_axe,]

stone_pick = Recipe("Stone tools","Pickaxe",{"Wood":3,"Stone":3},{"Stone Pickaxe":30})
locked_recipes += [stone_pick,]

stone_axe = Recipe("Stone tools","Axe",{"Wood":3,"Stone":3},{"Stone Axe":30})
locked_recipes += [stone_axe,]

grinder = Recipe("Stone tools","Grinder",{"Stone":10},{"Grinder":30})
locked_recipes += [grinder,]

furnace = Recipe("Machines","Furnace",{"Stone":10},{"Furnace":1})
locked_recipes += [furnace,]
    

def Crafting_tab(game:Game)->None:
    pg.display.set_caption("Crafting Page")
    y_list_space = 15

    #region Crafting recipes
    
    global locked_recipes
    global unlocked_recipes
    global categories
    
    
    #endregion

    

    inventory_tab_running = True
    while inventory_tab_running:
        pg.time.Clock().tick(framerate)
        surface.fill(background)

        #Checks
        for recipe in locked_recipes:
            unlocked = recipe.check(game)
            if unlocked:
                locked_recipes.remove(recipe)
                if recipe.category not in categories:
                    categories += [recipe.category,]
                unlocked_recipes += [recipe,]
            

        
        
        #Header
        y=y_header
        header = big_font.render("Craft",True,white,black)
        surface.blit(header,(x_header,y))


        #Display
        buttons = []
        for category in categories:
            y+=20
            subheader = subheader_font.render(category,True,white,black)
            surface.blit(subheader,(x_subtitle,y))
            for recipe in unlocked_recipes:
                if recipe.category == category:
                    y+=30
                    buttons += [(draw_button(x_normal,y,recipe.name,green),recipe),]






        #Interactivity
        for event in pg.event.get():
            if event.type == pg.QUIT:
                inventory_tab_running = False
            if event.type == pg.MOUSEBUTTONDOWN:

                for button in buttons:
                    if button[0].collidepoint(event.pos):
                        button[1].craft(game)
                    

        pg.display.update()


    pg.quit()

#endregion




#endregion

#endregion
    
    


#region Main    
def Main(game):
    
    processes = []
    
    running = True
    furnace_timers = []
    furnace_items = []

    while running:
        pg.time.Clock().tick(framerate)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                for process in processes:
                    process.terminate()
            if event.type == pg.MOUSEBUTTONDOWN:
                if inventory_button.collidepoint(event.pos):
                    processes += [mp.Process(target=Inventory_tab,args=(game,)),]
                    processes[-1].start() 
                if gathering_button.collidepoint(event.pos):
                    processes += [mp.Process(target=Gathering_tab,args=(game,)),]
                    processes[-1].start() 
                if crafting_button.collidepoint(event.pos):
                    processes += [mp.Process(target=Crafting_tab,args=(game,)),]
                    processes[-1].start() 
                         
        
        
        pg.display.set_caption("Main Page")
        
        
        y=y_header
        header = big_font.render("Main",True,white,black)
        surface.blit(header,(x_header,y))

        x1 = 10
        y1 = 50
        y2 = 100
        y3 = 150
        inventory_button = draw_button(x1,y1,"Inventory",orange)
        gathering_button = draw_button(x1,y2,"Gather",blue)
        crafting_button = draw_button(x1,y3,"Crafting",red)
        
        #furnace_timers,furnace_items = game.furnace(furnace_timers,furnace_items)
        
        pg.display.update()
    pg.quit()
    return
#endregion     


window_num = 2
if __name__ == '__main__':
    
    manager = mp.Manager() 
    game = Game(manager)
    Main(game)
    
    #processes = []
    # for _ in range(window_num):
    #     processes += [mp.Process(target=run,args=(game,)),]
        
    # for process in processes:
    #     process.start()
        
    # for process in processes:
    #     process.join()