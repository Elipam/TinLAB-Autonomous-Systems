# -*- coding: utf-8 -*-
"""
Created on Thu May 30 13:48:09 2024

@author: spanj
"""
current_positions = {'A':(0,0), 'B':(0,1), 'C':(0,2), 'D':(1,0)}
goal_positions = {'A':(3,3), 'B':(6,6), 'C':(3,6), 'D':(6,3)}
possible_moves = [(1,0), (0,1), (-1,0), (0,-1), (0,0)]

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def make_grid(width, height):
    return [[0 for _ in range(width)] for _ in range(height)]

def print_grid(grid):
    print(F"+{len(grid[0])*'-'*2+'-'}+")
    for row in grid:
        print('|', end='')
        for element in row:
            print(F" {element}", end='')
        print(' |')
    print(F"+{len(grid[0])*'-'*2+'-'}+")
    
def algorithm(startGrid, goalGrid):
    nextGrid = make_grid(len(startGrid[0]), len(startGrid))
    for key, value in current_positions.items():
        row, col = value
        if value == goal_positions[key]:
            nextGrid[col][row] = key
            continue
        min_heuristic = float('inf')
        best_move = None
        for move in possible_moves:
            next_row, next_col = row + move[0], col + move[1]
            if not (0 <= next_row < len(nextGrid) and 0 <= next_col < len(nextGrid[0])):
                continue
            if nextGrid[next_col][next_row] != 0:
                continue
            h = heuristic((next_row, next_col), goal_positions[key])
            if h < min_heuristic:
                min_heuristic = h
                best_move = move
        if best_move:
            next_row, next_col = row + best_move[0], col + best_move[1]
            nextGrid[next_col][next_row] = key
            current_positions[key] = (next_row, next_col)
    
    print_grid(nextGrid)
    if nextGrid == goalGrid:
        return
    algorithm(nextGrid, goalGrid)            
    
if __name__ == '__main__':
    width, height = 10, 10
    start = make_grid(width, height)
    goal = make_grid(width, height)
    
    paths = {}
    for key, value in current_positions.items():
        row, col = value
        start[col][row] = key
        row, col = goal_positions[key]
        goal[col][row] = key
    
    
    print_grid(start)
    print_grid(goal)
    algorithm(start, goal)
    
    
    