# geometry.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Jongdeog Lee (jlee700@illinois.edu) on 09/12/2018

"""
This file contains geometry functions that relate with Part1 in MP2.
"""

import math
import numpy as np
from const import *

def computeCoordinate(start, length, angle):
    """Compute the end cooridinate based on the given start position, length and angle.

        Args:
            start (tuple): base of the arm link. (x-coordinate, y-coordinate)
            length (int): length of the arm link
            angle (int): degree of the arm link from x-axis to couter-clockwise

        Return:
            End position of the arm link, (x-coordinate, y-coordinate)
    """

    return (start[0]+length*math.cos((angle/180)*math.pi),start[1]-length*math.sin((angle/180)*math.pi))
    pass

def doesArmTouchObstacles(armPos, obstacles):
    """Determine whether the given arm links touch obstacles

        Args:
            armPos (list): start and end position of all arm links [(start, end)]
            obstacles (list): x-, y- coordinate and radius of obstacles [(x, y, r)]

        Return:
            True if touched. False it not.
    """
    for i in range(len(armPos)):
        start = armPos[i][0]
        end = armPos[i][1]
        if end[0]==start[0]:
            k = 1
        else:
            k = (end[1]-start[1])/(end[0]-start[0])
        b = start[1]-k*start[0]

        if k==0:
            k_inv = 1
        elif k==1:
            k_inv = 0
        else:
            k_inv = -1/k
        for j in range(len(obstacles)):
            ob = obstacles[j]
            if((start[0]-ob[0])*(start[0]-ob[0])+(start[1]-ob[1])*(start[1]-ob[1]) <= ob[2]*ob[2]):
                return True
            if((end[0]-ob[0])*(end[0]-ob[0])+(end[1]-ob[1])*(end[1]-ob[1]) <= ob[2]*ob[2]):
                return True
            ob_b = ob[1]-k_inv*ob[0]
            interx = (ob_b-b)/(k-k_inv)
            intery = interx*k+b
            r_sq = (interx-ob[0])*(interx-ob[0])+(intery-ob[1])*(intery-ob[1])
            if r_sq <=ob[2]*ob[2]:
                if (((interx>=end[0])and(interx<=start[0])) or ((interx<=end[0])and(interx>=start[0]))):
                    return True

    return False


def doesArmTouchGoals(armEnd, goals):
    """Determine whether the given arm links touch goals

        Args:
            armEnd (tuple): the arm tick position, (x-coordinate, y-coordinate)
            goals (list): x-, y- coordinate and radius of goals [(x, y, r)]

        Return:
            True if touched. False it not.
    """
    for i in range(len(goals)):
        g = goals[i]
        r_sq = (g[0]-armEnd[0])*(g[0]-armEnd[0])+(g[1]-armEnd[1])*(g[1]-armEnd[1])
        if g[2]*g[2] >= r_sq:
            return True
    return False


def isArmWithinWindow(armPos, window):
    """Determine whether the given arm stays in the window

        Args:
            armPos (list): start and end position of all arm links [(start, end)]
            window (tuple): (width, height) of the window

        Return:
            True if all parts are in the window. False it not.
    """
    for i in range(len(armPos)):
        start = armPos[i][0]
        end = armPos[i][1]


        if(start[0]<0 or start[0]>window[0] or start[1]<0 or start[1]>window[1] or end[0]<0 or end[0]>window[0] or end[1]<0 or end[1]>window[1]):
            return False

    return True
