# search.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Jongdeog Lee (jlee700@illinois.edu) on 09/12/2018

"""
This file contains search functions.
"""
# Search should return the path and the number of states explored.
# The path should be a list of tuples in the form (alpha, beta, gamma) that correspond
# to the positions of the path taken by your search algorithm.
# Number of states explored should be a number.
# maze is a Maze object based on the maze from the file specified by input filename
# searchMethod is the search method specified by --method flag (bfs,dfs,greedy,astar)
# You may need to slight change your previous search functions in MP1 since this is 3-d maze
from util import *
def search(maze, searchMethod):
    return {
        "bfs": bfs,
        "dfs": dfs,
        "greedy": greedy,
        "astar": astar,
    }.get(searchMethod, [])(maze)

def bfs(maze):
    # TODO: Write your code here
    alpha = maze.offsets[0]
    beta = maze.offsets[1]
    gamma = maze.offsets[2]
    q = []
    st = angleToIdx(maze.getStart(),maze.offsets,maze.granularity)
    #print(st)
    q.append(st)
    v = set()
    path = []
    dem = maze.getDimensions()
    #print(dem)
    n = dem[0]
    m = dem[1]
    h = dem[2]
    map = [[[(0,0,0)]*h for _ in range(m)] for _ in range(n)]
    v.add(st)
    while q:
        cur = q.pop(0)
        cur_angle = idxToAngle(cur,maze.offsets,maze.granularity)
        n = maze.getNeighbors(cur_angle[0],cur_angle[1],cur_angle[2])
        for i in n:
            if angleToIdx(i,maze.offsets,maze.granularity) in v:
                continue
            v.add(angleToIdx(i,maze.offsets,maze.granularity))
            a = angleToIdx(i,maze.offsets,maze.granularity)[0]
            b = angleToIdx(i,maze.offsets,maze.granularity)[1]
            c = angleToIdx(i,maze.offsets,maze.granularity)[2]
            map[a][b][c] = cur
            q.append(angleToIdx(i,maze.offsets,maze.granularity))
            if maze.isObjective(i[0],i[1],i[2]):
                while True:
                    if(i==maze.getStart()):
                        path.insert(0,i)
                        break
                    path.insert(0,i)
                    prev = map[angleToIdx(i,maze.offsets,maze.granularity)[0]][angleToIdx(i,maze.offsets,maze.granularity)[1]][angleToIdx(i,maze.offsets,maze.granularity)[2]]

                    i = idxToAngle(prev,maze.offsets,maze.granularity)

                return path,len(v)
    return [], 0

def dfs(maze):
    # TODO: Write your code here
    return [], 0

def greedy(maze):
    # TODO: Write your code here
    return [], 0

def astar(maze):
    # TODO: Write your code here
    return [], 0
