#!path/Scripts/python.exe
import random

def stage1(size=(500,500)):
    a, b, c, d = [], [], [], []
    for i in range(0,size[0], 10):
        a += [[i,0]]
        b += [[i,size[1]-10]]
    for j in range(10,size[1]-10, 10):
        c += [[0, j]]
        d += [[size[0]-10, j]]
    return a+b+c+d


def stage2(size=(500,500)):
    a = stage1(size)
    b1,b2,b3,b4,c1,c2,c3,c4 = [],[],[],[],[],[],[],[]
    for i in range(10, size[0]-10, 10):
        if 40<i<140:
            b1 += [[i, 40]]# x top left
            b2 += [[size[0]-10-i, 40]]#x top right
            b3 += [[i, size[0]-10-40]]#x down left
            b4 += [[size[0]-i-10, size[0]-10-40]]#x down right
            c1 += [[40, i+20]]#y top left
            c2 += [[40, size[0]-i-40]]#y down left
            c3 += [[size[0]-10-40, i+20]]#y top right
            c4 += [[size[0]-10-40, size[0]-i-40]]#y down right

    return a+b1+b2+b3+b4+c1+c2+c3+c4

def stage3(size=(500,500)):
    a = stage1(size)
    b, c, d = [], [], []
    for i in range(0, size[0], 10):
        if i>50:
            b += [[i, int(size[0]/40)*30]]
        if i<size[0]-50:
            d += [[i, int(size[0]/40)*10]]
        if int((size[0]/20)) > i/10 or int((size[0]/20))+10 < i/10:
            c += [[i, int(size[0]/20)*10]]
    return a+b+c+d

def random_2(size = (500, 500)):
    a = stage1(size)
    check = True
    summ_wall=[random.randint(3,5),random.randint(2,5)]
    x_limit = [20]+[(size[0]/10//summ_wall[0]*10)*i for i in range(1,summ_wall[0]+1)]
    y_limit = [20]+[(size[0]/10//summ_wall[1]*10)*i for i in range(1,summ_wall[1]+1)]
    wall_lim = []
    for i in range(1, len(y_limit)):
        for j in range(1, len(x_limit)):
            start = [x_limit[j-1], y_limit[i-1]]
            stop = [x_limit[j], y_limit[i]]
            wall_lim += [[start,stop]]

    for i in wall_lim:
        if check:
            check = not check
            continue
        one_wall = []
        wall_side = random.randint(0,1) # 0->horizontal 1->vertical
        n = (i[1][0]-i[0][0])//10 if wall_side==0 else (i[1][1]-i[0][1])//10
        wall_leng = random.randint(n-6, n-3)
        if wall_side == 0: #if horizontal x changes
            start_point = [random.randrange(i[0][0], i[1][0]-wall_leng*10-20, 10),
                           random.randrange(i[0][1], i[1][1]-10, 10)]
        else: # if vertical y changes
            start_point = [random.randrange(i[0][0], i[1][0]-20, 10),
                           random.randrange(i[0][1], i[1][1]-wall_leng*10-20, 10)]
        for i in range(wall_leng):
            one_wall += [start_point]
            start_point = [start_point[0]+10, start_point[1]] if wall_side==0 else [start_point[0], start_point[1]+10]
        a += one_wall
    return a


def random_(size=(500,500)):
    a = stage1(size)
    b = [] # to save all walls
    sum_wall = random.randint(7,15)
    for i in range(sum_wall):
        c = [] # empty list to save one wall
        len_wall = random.randint(5, 20)
        side = random.randint(0,1) # 1->vertical 0->horizontal
        if side == 0: #if horizontal
            start = [random.randrange(10, size[0]-(len_wall*10), 10),
                     random.randrange(10, size[0]-10, 10)]
        else:
            start = [random.randrange(10, size[0]-10, 10),
                     random.randrange(10, size[0]-(len_wall*10), 10)]
            
        for i in range(len_wall):
            c += [start.copy()]
            if side==0:
                start[0] += 10
            else:
                start[1] += 10
        b += c
    return a+b


def test(pos, size=(500,500)):
    import pygame as py
    green = (255, 0, 0)
    screen = py.display.set_mode(size)
    py.display.set_caption("Test Mode")
    for i in pos:
        py.draw.rect(screen, green, py.Rect(i, [10,10]))
    py.display.flip()
    

if __name__ == '__main__':
    a = random_2()
    test(a)
