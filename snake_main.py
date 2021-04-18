#!path/Scripts/python.exe

# Libraries and source
import pygame as py
import random
import sys
import stages


# Usefull functions
def find(mainlist, item):
    if len(mainlist) == 0:
        return 0
    
    for i in mainlist:
        if item == i:
            return 1
    return 0

def color_generator():
    c = []
    for i in range(5):
        a = random.randint(0,255)
        b = random.randint(0,255)
        d = random.randint(0,255)
        c += [(a,b,d)]
    return c
# find function returns 1 when find the item into mainlist

# Constants and main pygame desk
# _co -> color
c = color_generator()

py.init()

speed_const = 8
#change this
stage_co = c[0] #(255, 255, 0)
back_co = c[1] #(0, 180, 0)
app_co = c[2] #(255, 255, 255)
head_co = c[3] #(204, 51, 0)
tail_co = c[4] #(255, 153, 102)
full_size = [500,550]
game_size = [500,500]
stage_lim = [10, 20, 30, 40]


speed = speed_const#don't change this
way_next_stage = [[150, 0], [160, 0], [170, 0]]


screen = py.display.set_mode(full_size)
py.display.set_caption("funny snake")
clock = py.time.Clock()
font = py.font.Font('freesansbold.ttf', 22)

# Main Snake class
class Snake:
    def __init__(self, a=[[20,10],[10, 10]], side='r', leng=0, stage=0):
        self.leng2 = 1
        self.a = a
        self.side = side
        self.leng = leng
        self.app_pos = [90, 90]
        self.mainbool = True
        self.size = [10,10]
        self.stage = stage
        self.wall = self.find_stage()
        self.for_stage = True
        self.stage_lim = stage_lim.copy()
        self.write("STATUS:", (15,10), stage_co, back_co)

    def find_stage(self):
        if self.stage == 0:
            return []
        elif self.stage == 1:
            return stages.stage1(tuple(game_size))
        elif self.stage == 2:
            return stages.stage2(tuple(game_size))
        elif self.stage == 3:
            return stages.stage3(tuple(game_size))
        else:
            return stages.random_2(tuple(game_size))

    def draw_rect(self, real, color):
        pos = [real[0], real[1] + full_size[1]-game_size[1]]
        py.draw.rect(screen, color, py.Rect(pos[0]+1, pos[1]+1, self.size[0]-1, self.size[1]-1))
        py.draw.lines(screen, back_co, True, (pos, (pos[0]+10,pos[1]), (pos[0]+10,pos[1]+10), (pos[0],pos[1]+10), (pos)))

    def draw_wall(self):
        wall = self.wall
        for i in wall:
            self.draw_rect(i, stage_co)

        
    def speedChange(self):
        global speed, tail_co
        a=random.randint(0,255)
        b=random.randint(0,255)
        d=random.randint(0,255)
        tail_co = (a,b,d)
        if self.leng%15 == 0:
            speed += 1


    def draw_app(self):
        apple = [random.randrange(0, game_size[0] - 10, 10), random.randrange(0, game_size[1] - 10, 10)]
        if find(self.a, apple)==0 and find(self.wall, apple)==0:
            self.draw_rect(self.app_pos, back_co)
            self.app_pos = apple
            self.draw_rect(self.app_pos, app_co)
            self.leng += 1
            self.leng2 += 1
            text = "SCORE: "+str(self.leng)+" "
            self.write(text, (330, 10), stage_co, back_co)
            self.speedChange()
        else:
            self.draw_app()


    def draw_snake(self, ind=0):
        if ind==2:
            self.draw_rect(self.a[0], tail_co)
        else:
            self.draw_rect(self.a[0], head_co)
        self.draw_rect(self.a[1], tail_co)
        if ind == 0 or ind == 2:
            self.draw_rect(self.a[-1], back_co)
            self.a.pop()

    def stage_end_start(self, poslist):
        for i in poslist:
            self.draw_rect(i, back_co)
            self.wall.remove(i)
            
    def new_stage(self):
        if len(self.stage_lim)>0:
            self.stage_lim.pop(0)
        self.stage += 1
        screen.fill(back_co)
        self.wall = self.find_stage()
        self.draw_wall()
        self.draw_app()
        self.write("STATUS:", (15,10), stage_co, back_co)
        self.leng2 = 1
        self.a = [[20,10],[10,10]]
        global speed
        self.mainbool = True
        return True

    def endGame(self):
        self.write(" end game ", (110, 10), stage_co, back_co)
        self.leng2 = 1
        self.side = 'r'
        self.leng = 0
        self.app_pos = [90, 90]
        self.mainbool = True
        self.size = [10, 10]
        self.stage = 1
        self.wall = self.find_stage()
        self.for_stage = True
        self.stage_lim = stage_lim.copy()
        return False

    def end_stage(self):
        if len(self.a)==1:
            return None
        self.draw_rect(self.a[0], tail_co)
        self.draw_rect(self.a[-1], back_co)
        self.a.pop()
        return True

    def write(self, text, pos, fontcol, backcol):
        textSurface = font.render(text, True, fontcol, backcol)
        screen.blit(textSurface, pos)

    def check(self, b):
        c = []
        if self.stage != 0 and len(self.wall) > 0:
            wall = self.wall
            if find(wall, b) == 1:
                c += [True]
        c += [b[0]<0 or b[1]<0]
        c += [b[0]>=game_size[0]]
        c += [b[1]>=game_size[1]]
        c += [find(self.a, b)==1]
        if find(c, True)==1:
            return True
        return False

    def update2(self, go):
        b = self.a[0].copy()

        if find(way_next_stage, b) == 1:
            return self.end_stage()

        if go == "r":
            b[0] += 10
        elif go == "l":
            b[0] -= 10
        elif go == "u":
            b[1] -= 10
        elif go == "d":
            b[1] += 10
        else:
            pass  # that else doesn't work. For a safety reasons only

        if self.check(b):
            self.mainbool = self.endGame()
        else:
            pass

        if find(way_next_stage, b)==1:
            self.for_stage = not self.for_stage

        if self.for_stage:
            self.a.insert(0, b)
        else:
            pass


        if b == self.app_pos:
            self.app_pos = [90,90]
            self.leng+=1
            self.draw_snake(ind=1)
            self.stage_end_start(way_next_stage)
            text = "SCORE: "+str(self.leng)+" "
            self.write(text, (330, 10), stage_co, back_co)
        else:
            self.draw_snake()


        return self.mainbool


    def update(self, go):
        self.write(" continue ", (110,10), stage_co, back_co)
        if len(self.stage_lim) == 1:
            self.stage_lim += [self.stage_lim[0]+10]
            
        if self.leng >= self.stage_lim[0]:
            return self.update2(go)

        b = self.a[0].copy()
        if go == "r":
            b[0] += 10
        elif go == "l":
            b[0] -= 10
        elif go == "u":
            b[1] -= 10
        elif go == "d":
            b[1] += 10
        else:
            pass    #that else doesn't work. For a safety reasons only

        if self.check(b):
            self.mainbool = self.endGame()
        else:
            pass

        self.a.insert(0, b)
        if b == self.app_pos:
            self.draw_app()
            self.draw_snake(ind=1)
        elif self.leng2 < self.leng:
            self.draw_snake(ind=1)
            self.leng2 += 1
        else:
            self.draw_snake()
        return self.mainbool


def newGame(position):
    global go, cont, speed
    go, cont, speed = 'r', True, speed_const
    screen.fill(back_co)
    snake = Snake(a=position, leng=0, stage=1)
    snake.draw_wall()
    snake.draw_app()
    return snake
    

# Main loop
snake = newGame([[20,10],[10,10]])
cont2 = True
check_button = True

while True:
    for event in py.event.get():
        if event.type == py.QUIT:
            py.quit()
            sys.exit()
        elif event.type == py.KEYDOWN:
            if cont == False and event.key == py.K_q:
                del(snake)
                snake = newGame([[20,10],[10,10]])
            elif cont and event.key == py.K_TAB:
                cont2 = not cont2
            elif cont2:
                if (event.key == py.K_UP or event.key == py.K_w) and go != 'd' and check_button:
                    go = 'u'
                    check_button = False
                elif (event.key == py.K_DOWN or event.key == py.K_s) and go != 'u' and check_button:
                    go = 'd'
                    check_button = False
                elif (event.key == py.K_LEFT or event.key == py.K_a) and go != 'r' and check_button:
                    go = 'l'
                    check_button = False
                elif (event.key == py.K_RIGHT or event.key == py.K_d) and go != 'l' and check_button:
                    go = 'r'
                    check_button = False
                else:
                    pass
    if cont == False:continue
    elif cont == None:
        cont = snake.new_stage()
        go = 'r'
    elif cont2 == False:
        snake.write(" paused   ", (110,10), stage_co, back_co)
        py.display.update()
        continue
    cont = snake.update(go)
    check_button = True
    
    py.display.update()
    clock.tick(speed)
