
# transform.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Jongdeog Lee (jlee700@illinois.edu) on 09/12/2018

"""
This file contains the transform function that converts the robot arm map
to the maze.
"""
import copy
from arm import Arm
from maze import Maze
from search import *
from geometry import *
from const import *
from util import *

def transformToMaze(arm, goals, obstacles, window, granularity):
    """This function transforms the given 2D map to the maze in MP1.

        Args:
            arm (Arm): arm instance
            goals (list): [(x, y, r)] of goals
            obstacles (list): [(x, y, r)] of obstacles
            window (tuple): (width, height) of the window
            granularity (int): unit of increasing/decreasing degree for angles

        Return:
            Maze: the maze instance generated based on input arguments.

    """


    angles = arm.getArmLimit()
    alpha = angles[0]
    if(len(angles)>1):
        beta = angles[1]
    else:
        beta = [0,0]
    if(len(angles)>2):
        gamma = angles[2]
    else:
        gamma = [0,0]
    row = (alpha[1]-alpha[0])/granularity+1
    col = (beta[1]-beta[0])/granularity+1
    height = (gamma[1]-gamma[0])/granularity+1

    start = angleToIdx(arm.getArmAngle(),[alpha[0],beta[0],gamma[0]],granularity)
    if(len(start)<3):
        start = [start[0],0,0]
    map = [[[SPACE_CHAR]*int(height) for _ in range(int(col))] for _ in range(int(row))]
    ob_g = []
    for o in obstacles:
        ob_g.append(o)
    for g in goals:
        ob_g.append(g)
    i = alpha[0]

    while i<=alpha[1]:
        j = beta[0]
        while j<=beta[1]:
            k = gamma[0]
            while(k<=gamma[1]):
                arm.setArmAngle((i,j,k))

                if doesArmTouchGoals(arm.getEnd(), goals):
                    idx = angleToIdx([i,j,k],[alpha[0],beta[0],gamma[0]],granularity)
                    map[idx[0]][idx[1]][idx[2]] = OBJECTIVE_CHAR
                elif doesArmTouchObstacles(arm.getArmPos(),ob_g):
                    idx = angleToIdx([i,j,k],[alpha[0],beta[0],gamma[0]],granularity)
                    map[idx[0]][idx[1]][idx[2]] = WALL_CHAR

                elif isArmWithinWindow(arm.getArmPos(), window)==False :
                    idx = angleToIdx([i,j,k],[alpha[0],beta[0],gamma[0]],granularity)
                    map[idx[0]][idx[1]][idx[2]] = WALL_CHAR
                k+=granularity

            j+=granularity
        i+=granularity
    print(start)
    map[start[0]][start[1]][start[2]] = START_CHAR

    f = open('inputmap.txt','w')
    for i in range(int(row)):
        for j in range(int(col)):
            for k in range(int(height)):
                f.write(map[i][j][k])
            f.write('\n')
        f.write('\n')
    f.close()

    return Maze(map,[alpha[0],beta[0],gamma[0]],granularity)



    pass
