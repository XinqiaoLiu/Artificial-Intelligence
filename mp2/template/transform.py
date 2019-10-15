
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
    beta = angles[1]
    row = (alpha[1]-alpha[0])/granularity+1
    col = (beta[1]-beta[0])/granularity+1
    #print(obstacles)
    #print(alpha,beta)
    #print(idxToAngle((40,29),[alpha[0],beta[0]],granularity))
    start = angleToIdx(arm.getArmAngle(),[alpha[0],beta[0]],granularity)
    map = [[SPACE_CHAR]*int(col) for _ in range(int(row))]
    ob_g = []
    for o in obstacles:
        ob_g.append(o)
    for g in goals:
        ob_g.append(g)
    i = alpha[0]

    while i<=alpha[1]:
        j = beta[0]
        while j<=beta[1]:
            arm.setArmAngle((i,j))
            #if i==100 and j==-92:
            #    print(arm.getArmPos())
            if doesArmTouchGoals(arm.getEnd(), goals):
                idx = angleToIdx([i,j],[alpha[0],beta[0]],granularity)
                map[idx[0]][idx[1]] = OBJECTIVE_CHAR
            elif doesArmTouchObstacles(arm.getArmPos(),ob_g):
                idx = angleToIdx([i,j],[alpha[0],beta[0]],granularity)
                map[idx[0]][idx[1]] = WALL_CHAR

            elif isArmWithinWindow(arm.getArmPos(), window)==False :
                idx = angleToIdx([i,j],[alpha[0],beta[0]],granularity)
                map[idx[0]][idx[1]] = WALL_CHAR


            j+=granularity
        i+=granularity
    map[start[0]][start[1]] = START_CHAR

    f = open('inputmap.txt','w')
    for i in range(int(row)):
        for j in range(int(col)):
            f.write(map[i][j])
        f.write('\n')
    f.close()

    return Maze(map,[alpha[0],beta[0]],granularity)



    pass
