import math
import json
import time
import pygame
from sys import exit
def get_intersections(x0, y0, r0, x1, y1, r1):
    # circle 1: (x0, y0), radius r0
    # circle 2: (x1, y1), radius r1

    d=math.sqrt((x1-x0)**2 + (y1-y0)**2)

    # non intersecting
    if d > r0 + r1 :
        return None
    # One circle within other
    if d < abs(r0-r1):
        return None
    # coincident circles
    if d == 0 and r0 == r1:
        return None
    else:
        a=(r0**2-r1**2+d**2)/(2*d)
        h=math.sqrt(r0**2-a**2)
        x2=x0+a*(x1-x0)/d   
        y2=y0+a*(y1-y0)/d   
        x3=x2+h*(y1-y0)/d     
        y3=y2-h*(x1-x0)/d 

        x4=x2-h*(y1-y0)/d
        y4=y2+h*(x1-x0)/d

        return (x3, y3, x4, y4)
def triangulate(a,b,c):
    with open('points.json') as json_file:
        try:
            data = json.load(json_file)
            
            data["1"]["d"] = math.pow(10,(-56.4-a)/31.8905)
            data["2"]["d"] = math.pow(10,(-56.4-b)/31.8905)
            data["3"]["d"] = math.pow(10,(-56.4-c)/31.8905)
            
            temp = get_intersections(data["1"]["x"],data["1"]["y"],data["1"]["d"],data["2"]["x"],data["2"]["y"],data["2"]["d"])
            avg12 = [0.5*(temp[0]+temp[2]), 0.5*(temp[1]+temp[3])]

            temp = get_intersections(data["1"]["x"],data["1"]["y"],data["1"]["d"],data["3"]["x"],data["3"]["y"],data["3"]["d"])
            avg13 = [0.5*(temp[0]+temp[2]), 0.5*(temp[1]+temp[3])]

            temp = get_intersections(data["2"]["x"],data["2"]["y"],data["2"]["d"],data["3"]["x"],data["3"]["y"],data["3"]["d"])
            avg23 = [0.5*(temp[0]+temp[2]), 0.5*(temp[1]+temp[3])]

            avg = [(avg12[0]+avg13[0]+avg23[0])/3, (avg12[1]+avg13[1]+avg23[1])/3]
            #print(avg)
            return avg
        except TypeError:
            print("Invalid Coordinate (No Possible Coordinate)")
            return -1

x_offset = 100
y_offset = 100
pygame.init()
screen = pygame.display.set_mode((700, 450))
while True:
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
    pygame.draw.rect(screen, (255,255,255), pygame.Rect(x_offset,y_offset,500,250))
    x = triangulate(-120,-120,-120)
    if x == -1:
        pygame.display.flip()
        continue
    print(x)
    pygame.draw.rect(screen, (0,128,255), pygame.Rect((x[0]*10)+x_offset,(x[1]*10)+y_offset,20,20))
    pygame.display.flip()

