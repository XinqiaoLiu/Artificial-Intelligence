# search.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Michael Abir (abir2@illinois.edu) on 08/28/2018

"""
This is the main entry point for MP1. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""
# Search should return the path.
# The path should be a list of tuples in the form (row, col) that correspond
# to the positions of the path taken by your search algorithm.
# maze is a Maze object based on the maze from the file specified by input filename
# searchMethod is the search method specified by --method flag (bfs,dfs,astar,astar_multi,extra)
import queue



def search(maze, searchMethod):
    return {
        "bfs": bfs,
        "dfs": dfs,
        "astar": astar,
        "astar_multi": astar_multi,
        "extra": extra,
    }.get(searchMethod)(maze)


def bfs(maze):
    """
    Runs BFS for part 1 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    q = []
    st = maze.getStart()
    q.append(st)
    v = set()
    path = []
    dem = maze.getDimensions()
    n = dem[0]
    m = dem[1]
    map = [[(0,0)]*m for _ in range(n)]
    v.add(st)

    while q:
        cur = q.pop(0)
        n = maze.getNeighbors(cur[0],cur[1])
        for i in n:
            if i in v:
                continue
            v.add(i)
            a = i[0]
            b = i[1]
            map[a][b] = cur
            q.append(i)


          #print(i)
            if maze.isObjective(i[0],i[1]):
                while True:
                    if(i==st):
                        path.insert(0,st)
                        break
                    path.insert(0,i)
                    prev = map[i[0]][i[1]]

                    i = prev

                return path

    return []


def dfs(maze):
    """
    Runs DFS for part 1 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    s = []
    st = maze.getStart()
    s.insert(0,st)
    v = set()
    path = []
    dem = maze.getDimensions()
    n = dem[0]
    m = dem[1]
    map = [[(0,0)]*m for _ in range(n)]
    v.add(st)
    while s:

        cur = s.pop(0)
        n = maze.getNeighbors(cur[0],cur[1])
        for i in n:
            if i in v:
                continue
            v.add(i)
            map[i[0]][i[1]] = cur
            s.insert(0,i)
            if maze.isObjective(i[0],i[1]):
                while True:
                    if(i==st):
                        path.insert(0,st)
                        break
                    path.insert(0,i)
                    i = map[i[0]][i[1]]
                return path
    return []


def astar(maze):
    """
    Runs A star for part 1 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    pq = queue.PriorityQueue()
    st = maze.getStart()
    dest = maze.getObjectives()[0]
    v = dict()
    path = []
    dem = maze.getDimensions()
    n = dem[0]
    m = dem[1]
    map = [[(0,0)]*m for _ in range(n)]
    v[st] = mdist(st,dest)
    pq.put((mdist(st,dest),st))

    while not pq.empty():
        curinfo = pq.get()

        curdist = curinfo[0]

        cur = curinfo[1]

        if cur==dest:
            while True:
                if(cur==st):
                    path.insert(0,cur)
                    return path
                path.insert(0,cur)
                cur = map[cur[0]][cur[1]]
            return path
        for i in maze.getNeighbors(cur[0],cur[1]):

            idist = mdist(i,dest)+1+curdist-mdist(cur,dest)
            if i in v:
                if idist>=v[i]:
                    continue
                else:
                    v[i] = idist
                    map[i[0]][i[1]] = cur
                    pq.put((idist,i))
            else:
                v[i] = idist
                pq.put((idist,i))
                map[i[0]][i[1]] = cur
    return []
def mdist(s,g):
    return abs(s[0]-g[0])+abs(s[1]-g[1])
def astar_multi(maze):
    """
    Runs A star for part 2 of the assignment in the case where there are
    multiple objectives.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    
    return []


def extra(maze):
    """
    Runs extra credit suggestion.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    return []
